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


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

USER_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_REGEX = re.compile(r"^.{3,20}$")
EMAIL_REGEX = re.compile(r"^[\S]+@[\S]+.[\S]+$")


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


def validate_name(username):
    return USER_REGEX.match(username)


def validate_password(password):
    return PASSWORD_REGEX.match(password)


def validate_email(email):
    if not email:
        return True
    return EMAIL_REGEX.match(email)


class MainPage(Handler):
    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html", items=items)


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
            self.redirect('/welcome?username=' + user_name)


class ThankyouHandler(Handler):
    def get(self):
        username = self.request.get('username')
        self.render("welcome.html", username=username)


app = webapp2.WSGIApplication([
    ('/signup', RegisterHandler),
    ('/welcome', ThankyouHandler)
], debug=True)
