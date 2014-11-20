# import httplib2
# import logging
import os
# import pickle

# from apiclient import discovery
# from oauth2client import appengine
# from oauth2client import client

import webapp2

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# TODO: make these compute (not gplus)
# service = discovery.build("compute", "v1", http=http)
# decorator = appengine.oauth2decorator_from_clientsecrets(
#     CLIENT_SECRETS,
#     scope='https://www.googleapis.com/auth/plus.me',
#     message='Go get a client_secrets.json via service acct')

class MainHandler(webapp2.RequestHandler):
  # @decorator.oauth_aware
  def get(self):
    # variables = {
    #     'url': decorator.authorize_url(),
    #     'has_credentials': decorator.has_credentials()
    #     }
    self.response.write('this is from webapp2 ftw')

class another_handler(webapp2.RequestHandler):
  def get(self):
    self.response.write('another route')

routes = [
  ('/api', MainHandler),
  # (decorator.callback_path, decorator.callback_handler()),
]

app = webapp2.WSGIApplication(routes, debug=True)
