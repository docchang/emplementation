import urllib
import urllib2

from google.appengine.ext import db, webapp
from django.utils import simplejson

def GetApiKey():
    fileLocation = 'api.txt'               
    try:
        f = open(fileLocation, 'r')
        apiKey = f.readline()
    except:
        apiKey = ''
    
    f.close()
    return apiKey

class User(db.Model):
    identifier = db.StringProperty()
    name = db.StringProperty()
    givenName = db.StringProperty()
    familyName = db.StringProperty()
    displayName = db.StringProperty()
    preferredUsername = db.StringProperty()
    verifiedEmail = db.StringProperty()

class RPXTokenHandler(webapp.RequestHandler):    
    def get (self):
        url = '/'
        self.redirect(url)    
    
    def post(self):
        #Extract the token from your environment
        token = self.request.get('token')
        
        # auth_info expects an HTTP Post with the following paramters:
        api_params = {
            'token':  token,             
            'apiKey': GetApiKey(),
            'format': 'json',
        }
        
        # make the api call
        url = 'https://rpxnow.com/api/v2/auth_info'
        http_response = urllib2.urlopen(url, urllib.urlencode(api_params))
        
        #read the json response
        auth_info_json = http_response.read()
        
        #process the json response NOTE: simplejson instead of regular json
        auth_info = simplejson.loads(auth_info_json)
        
        if auth_info['stat'] == 'ok':
            profile = auth_info['profile']
            
            #initialize user to User object
            user = User()
            
            #retrive the identifier
            user.identifier = profile['identifier']
            user.displayName = profile['displayName']
            user.preferredUsername = profile['preferredUsername']
            try:
                user.verifiedEmail = profile['verifiedEmail']
            except:
                user.verifiedEmail = None
            try:
                user.name = profile['name']['formatted']
            except:
                user.name = None
            try:
                user.givenName = profile['name']['givenName']
            except:
                user.givenName = None
            try:
                user.familyName = profile['name']['familyName']
            except:
                user.familyName = None
            
            #write to datastore
            user.put()
            
            #redirect back
            self.redirect('/')
        else:
            self.redirect('/error')
