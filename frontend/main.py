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
  """Sanity check handler"""
  def get(self):
    param = self.request.get('param', default_value="no_value_provided")
    self.response.write('api routes in webapp2: ' + param)

def is_valid_server_name(name):
  return True # TODO: alphanumeric with dashes (see the gce regex)

class CreateServerHandler(webapp2.RequestHandler):
  """Creates a new server instance"""
  # TODO: this should really be a POST...
  def get(self):
    server_name = self.request.get('server', default_value='default-server-name')
    if not is_valid_server_name(server_name):
      pass # TODO: return an error

    # TODO: validate server name is valid firebase key and compute engine instance name
    servers.create_instance(
      server_name,
      self.request.get('disk', default_value='boot-pool-3'),
      poll=False)
    self.response.write('create request was sent')

routes = [
  ('/api', MainHandler),
  ('/api/create', CreateServerHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
