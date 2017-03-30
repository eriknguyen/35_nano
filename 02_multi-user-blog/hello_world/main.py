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

import webapp2
import cgi

form = """
<form method="post">

  What is your birthday?<br>

  <label for="">Month
    <input type="text" name="month" value="%(month)s">
  </label>

  <label for="">Day 
    <input type="text" name="day" value="%(day)s">
  </label>

  <label for="">Year
    <input type="text" name="year" value="%(year)s">
  </label>

  <div style="color: red;">%(error)s</div>

  <br>
  <br>
  <input type="submit">
</form>
"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

# month_abbvs = {'jun': 'June', 'nov': 'November', 'dec': 'December', 'jul': 'July', 'sep': 'September', 'jan': 'January', 'apr': 'April', 'mar': 'March', 'oct': 'October', 'feb': 'February', 'aug': 'August', 'may': 'May'}

month_abbvs = dict((m[:3].lower(),m) for m in months)


# def valid_month(month):
#     if month and (month.capitalize() in months):
#         return month.capitalize()

def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)


def valid_day(day):
    if day and day.isdigit():
        d = int(day)
        if d > 0 and d <=31:
            return int(day)


def valid_year(year):
    if year and year.isdigit():
        yr = int(year)
        if yr >= 1900 and yr <= 2020:
            return yr


# def escape_html(s):
#     for (i, o) in (("&", "&amp;"), (">", "&gt;"), ("<", "&lt;"), ('"', '&quot;')):
#         s = s.replace(i, o)
#     return s

def escape_html(s):
    return cgi.escape(s, quote=True)


class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {
            "error": error,
            "month": escape_html(month),
            "day": escape_html(day),
            "year": escape_html(year)
        })
    
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (day and month and year):
            self.write_form("That doesn't look valid to me, friend.",
            user_month, user_day, user_year)
            # self.response.out.write('Thanks! Form submitted :)')            
        else:
            self.redirect('/thanks')


# class TestHandler(webapp2.RequestHandler):
#     def post(self):
#         # q = self.request.get('q')
#         # self.response.out.write(q)
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write(self.request)


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)
