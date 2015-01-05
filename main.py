#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import os
import json
import webapp2
import logging

from google.appengine.ext.webapp import template

from krossgata import regex_search2, perm_search
from utils import to_unicode_or_bust


class MainHandler(webapp2.RequestHandler):
    def get(self):

        path = os.path.join(os.path.dirname(__file__), 'templates','index.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        which = self.request.get('which')
        perms = self.request.get('perms', None)
        regex = self.request.get('regex', None)
        d = {}
        if which == 'regex':
            regex = ''.join([r'\s', to_unicode_or_bust(regex), r'\s'])
            rmatches = regex_search2(regex)
            d.update(regex=rmatches)
        if which == 'perms':
            pmatches = perm_search(perms)
            d.update(perms=pmatches)
        self.response.out.write(json.dumps(d))

app = webapp2.WSGIApplication(
    [
        ('/', MainHandler),
    ], 
    debug=True)