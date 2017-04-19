# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import jinja2
import webapp2
import re
import random, string
import hashlib
import hmac
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

USER_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_REGEX = re.compile(r"^.{3,20}$")
EMAIL_REGEX = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def validate_name(username):
    return USER_REGEX.match(username)


def validate_password(password):
    return PASSWORD_REGEX.match(password)


def validate_email(email):
    if not email:
        return True
    return EMAIL_REGEX.match(email)


SECRET = 'imsosecret'


def hash_str(s):
    # return hashlib.md5(s.encode()).hexdigest()
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    if make_pw_hash(name, pw, salt) == h:
        return True


class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    salt = db.StringProperty(required=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class RegisterHandler(Handler):
    def get(self):
        data = {}
        self.render('register.html', data=data)

    def post(self):
        print("receive post from form")
        user_name = self.request.get("username")
        user_pwd = self.request.get("password")
        verified_pwd = self.request.get("verify")
        user_email = self.request.get("email") or ""

        data = {
            'name_value': user_name,
            'email_value': user_email
        }

        any_error = False

        if not validate_name(user_name):
            print("name error")
            data.update({'name_err': 'Name error'})
            any_error = True
        # else:
        #     query_str = "SELECT * FROM User WHERE username = '%s'" % user_name
        #     check_user = db.GqlQuery(query_str)
        #     print("check_user")
        #     print(query_str)
        #     print(check_user)
        #     print(check_user.username)
        #     print(check_user.password)
        #     print("end check_user")
        #     # need other way to check if record existed
        #     if check_user:
        #         data.update({
        #             'name_err': 'Username already existed'
        #             })
        #         any_error = True
        if not validate_password(user_pwd):
            print("password error")
            data.update({'pwd_err': 'Password error'})
            any_error = True
        elif user_pwd != verified_pwd:
            print("password not match")
            data.update({'vpassword_err': 'Password not match'})
            any_error = True
        if not validate_email(user_email):
            print("email invalid")
            data.update({'email_err': 'Invalid email'})
            any_error = True

        if any_error:
            self.render('register.html', data=data)
        else:
            # store new user
            salt = make_salt()
            new_user = User(username=user_name,
                password=make_pw_hash(user_name, user_pwd, salt),
                salt=salt)
            new_user.put()
            print("user saved", new_user.username)

            # redirect to welcome page
            new_cookie_val = make_secure_val(str(user_name))
            self.response.headers.add_header('Set-Cookie', 'user_id=%s' % new_cookie_val)
            self.redirect('/welcome')


class SigninHandler(Handler):
    def get(self):
        data = {}
        self.render('signin.html', data=data)

    def post(self):
        data = {}
        self.write("yay")


class WelcomeHandler(Handler):
    def get(self):
        user_cookie_str = self.request.cookies.get('user_id')
        if user_cookie_str:
            cookie_val = check_secure_val(user_cookie_str)
            print("cookie_val = ", cookie_val)
            if cookie_val:
                print("check_secure_val passed")
                username = cookie_val
                print("cookie_val is", username)
                self.render("welcome.html", username=username)
            else:
                print("check_secure_val failed")
                self.redirect('/signup')
        else:
            print("no cookie val")
            self.redirect('/signup')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/signup', handler=RegisterHandler, name='signup'),
    webapp2.Route(r'/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route(r'/signin', handler=SigninHandler, name='signin')
], debug=True)
