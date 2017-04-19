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
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render("blogs.html", blogs=blogs)



class NewBlogHandler(Handler):
    def get(self):
        self.render("newblog.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            new_blog = Blog(subject=subject, content=content)
            new_blog.put()
            blog_id = new_blog.key().id()
            print("blog saved: ", blog_id, int(blog_id))

            uri = webapp2.uri_for('blog', blog_id=int(blog_id))
            self.redirect(uri)

        else:
            error = "We need both subject and content"
            self.render("newblog.html", error=error, subject=subject, content=content)


class BlogHandler(Handler):
    def get(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        blog_data = {
            'subject': blog.subject,
            'content': blog.content
        }
        self.render("blog.html", blog=blog_data)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/blog', handler=MainPage, name='blogs'),
    webapp2.Route(r'/blog/newpost', handler=NewBlogHandler, name='new-blog'),
    webapp2.Route(r'/blog/<blog_id:\d+>', handler=BlogHandler, name='blog')
], debug=True)
