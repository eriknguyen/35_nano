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

form_html = """
<form method="post">
    <textarea name="text" id="" cols="30" rows="10">%(text)s</textarea>
    <div style="color: red;">%(error)s</div>
    <button>Submit</button>
</form>
"""

alphabets = "abcdefghijklmnopqrstuvwxyz"


class MainPage(webapp2.RequestHandler):
    def write_form(self, text="", error=""):
        self.response.out.write(form_html % {
            'text': cgi.escape(text, quote=True),
            'error': error
        })

    def get(self):
        self.write_form()

    def post(self):
        text_input = self.request.get("text")

        if not (text_input):
            self.write_form(
                text_input, "That doesn't look valid to me, friend.")
        else:
            output = ""
            for char in text_input:
                if char.lower() in alphabets:
                    i = alphabets.index(char.lower())
                    if i < 13:
                        o = i + 13
                    else:
                        o = i - 13
                    out_char = alphabets[o:o + 1]
                    if char in alphabets:
                        output += out_char
                    else:
                        output += out_char.upper()
                else:
                    output += char

            self.write_form(output, "That's correct input, friend.")


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
