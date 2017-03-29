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

form = """
<form method="post">

  What is your birthday?<br>

  <label for="">Month
    <input type="text" name="month">
  </label>

  <label for="">Day 
    <input type="text" name="day">
  </label>

  <label for="">Year
    <input type="text" name="year">
  </label>
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


class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(form)

    def post(self):
        user_month = valid_month(self.request.get('month'))
        user_day = valid_day(self.request.get('day'))
        user_year = valid_year(self.request.get('year'))
        if not (user_day and user_month and user_year):
            self.response.out.write(form)
            # self.response.out.write('Thanks! Form submitted :)')            
        else:
            self.response.out.write('Thanks! Form submitted :)')


# class TestHandler(webapp2.RequestHandler):
#     def post(self):
#         # q = self.request.get('q')
#         # self.response.out.write(q)
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write(self.request)


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
