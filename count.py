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
import jinja2
import json
import os
import webapp2

from google.appengine.ext import ndb


jinjaEnv = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),
        'templates')))

class Counter(ndb.Model):
    name = ndb.StringProperty(required=True)
    count = ndb.IntegerProperty(default=0)

    @classmethod
    def getCounter(cls):
        counters = cls.query().fetch(1)
        if not counters:
            counter = Counter(name='main')
            counter.put()
        else:
            counter = counters[0]

        return counter

    @classmethod
    def getCount(cls):
        counter = Counter.getCounter()
        return counter.count

    @classmethod
    def incrementCount(cls):
        counter = Counter.getCounter()
        counter.count += 1
        counter.put()
        return counter.count

class MainHandler(webapp2.RequestHandler):
    def get(self):
        count = Counter.getCount()
        template = jinjaEnv.get_template('count.html')
        self.response.write(template.render({'count': count}))

class CountHandler(webapp2.RequestHandler):
    def get(self):
        # Send the current count.
        count = Counter.getCount()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'count': count}))


    def post(self):
        # Increment the count, and respond with the new count.
        count = Counter.incrementCount()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'count': count}))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/count', CountHandler)
], debug=True)
