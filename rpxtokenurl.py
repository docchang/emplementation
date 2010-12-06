import urllib


from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from django.utils import simplejson

class RPXTokenHandler(webapp.RequestHandler):
    
    def post(self):
        token = self.request.get('token')
        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {'format': 'json',
                'apiKey': '',
                'token':  token}
        
        r = urlfetch.fetch(url=url,
                           payload=urllib.urlencode(args),
                           method=urlfetch.POST,
                           headers={'Content-Type':'application/x-www-form-urlencoded'})
        
        json = simplejson.loads(r.content)

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
        users.get_current_user = users.User(email=user.email,
                                            federated_identity=user.identifier)
