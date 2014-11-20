# import httplib2
# import logging
import os
# import pickle

# from apiclient import discovery
# from oauth2client import appengine
# from oauth2client import client

import webapp2

import servers
import random

class MainHandler(webapp2.RequestHandler):
  # @decorator.oauth_aware
  def get(self):
    # variables = {
    #     'url': decorator.authorize_url(),
    #     'has_credentials': decorator.has_credentials()
    #     }
    self.response.write('this is from webapp2 ftw')

class CreateServerHandler(webapp2.RequestHandler):
  # @decorator.oauth_aware
  def get(self):
    print servers.create_instance(
      'created-via-appengine-%d' % random.randint(0, 100000),
      poll=False)
    self.response.write('success maybe?')
    # if decorator.has_credentials():
    #   print servers.create_instance('created_via_appengine', poll=False)
    #   self.response.write('success maybe?')
    # else:
    #   self.response.write('no oauth credentials available!')

routes = [
  ('/api', MainHandler),
  ('/api/create', CreateServerHandler),
  # (decorator.callback_path, decorator.callback_handler()),
]

app = webapp2.WSGIApplication(routes, debug=True)

# NOTE: validate server name is valid firebase key and compute engine instance name
