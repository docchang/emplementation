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

import wsgiref.handlers
import urllib
import urllib2

from google.appengine.api import users, urlfetch
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
#from google.appengine.ext.webapp.util import run_wsgi_app
 
from django.utils import simplejson

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class RPXTokenHandler(webapp.RequestHandler):    
    def post(self):
        token = self.request.get('token')
        url = 'https://rpxnow.com/api/v2/auth_info'
        api_params  = {'format': 'json',
                'apiKey': '1c9f759408fd2a2bb6eb3d76321e018e805fd5c3',
                'token':  token}
        
        http_response = urllib2.urlopen(url, urllib.urlencode(api_params))

        # read the json response
        auth_info_json = http_response.read()

        # Step 3) process the json response
        auth_info = json.loads(auth_info_json)

        # Step 4) use the response to sign the user in
        if auth_info['stat'] == 'ok':
            profile = auth_info['profile']
   
            # 'identifier' will always be in the payload
            # this is the unique idenfifier that you use to sign the user
            # in to your site
            identifier = profile['identifier']
   
            # these fields MAY be in the profile, but are not guaranteed. it
            # depends on the provider and their implementation.
            name = profile.get('displayName')
            email = profile.get('email')
            
            user = {'identifier':   json['profile']['identifier'],
                    'name':         json['profile']['displayName'],
                    'nickname':     json['profile']['preferredUsername'],
                    'email':        json['profile']['email']}
            self.log_user_in(user)


    # actually sign the user in.  this implementation depends highly on your
    # platform, and is up to you.
    sign_in_user(identifier, name, email, profile_pic_url)
   
else:
    print 'An error occured: ' + auth_info['err']['msg']

        if json['stat'] == 'ok':
            user = {'identifier':   json['profile']['identifier'],
                    'name':         json['profile']['displayName'],
                    'nickname':     json['profile']['preferredUsername'],
                    'email':        json['profile']['email']}
            self.log_user_in(user)
            self.redirect('/')
        else:
            self.redirect('/error')
     
    def log_user_in(self, user):
        users.get_current_user = users.User(email = user.email, 
                                            federated_identity = user.identifier)

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #dURL = "/"

        if user:  # signed in already
            self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>]' % (
              user.nickname(),
              users.create_logout_url(self.request.uri) ))
        else:     # let user choose authenticator
            self.response.out.write('<a class="rpxnow" onclick="return false;" href="https://emplementation.rpxnow.com/openid/v2/signin?token_url=http%3A%2F%2Flocalhost:8082%2Frpx_response"> Sign In </a>')

#            self.response.out.write('Hello world! Sign in at: ')
#            pName = "Facebook"
#            pURL = "https://e75d3daf6e7141c1bd0be6a0d33c4d85.anyopenid.com/op"
#            self.response.out.write('[<a href="%s">%s</a>]' % 
#				(users.create_login_url(dest_url=dURL, federated_identity=pURL), pName))
    #===========================================================================
    # 
    # else:
    #  self.response.out.write('Hello world! Sign in at: ')
    #  for p in openIdProviders:
    #    p_name = p.split('.')[0] # take "AOL" from "AOL.com"
    #    p_url = p.lower()        # "AOL.com" -> "aol.com"
    #    self.response.out.write('[<a href="%s">%s</a>]' % (users.create_login_url(dest_url=dURL, federated_identity=p_url), p_name))
    #    
    #===========================================================================
        greetings = Greeting.all().order('-date').fetch(20)
        value = {'user':        user,
                 'greetings':   greetings,
                 'logout':		users.create_logout_url(self.request.uri)}
        
        self.response.out.write(template.render('main.html', value))
        return

class Guestbook(webapp.RequestHandler):
    def post(self):	
        greeting = Greeting()
        user = users.get_current_user()
        
        if user:
            greeting.author = user
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/sign', Guestbook),
    ('/rpx_response', RPXTokenHandler),
], debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
