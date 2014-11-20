#!/usr/bin/env python

import logging
import sys
import argparse
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.tools import run_flow

from apiclient.discovery import build

import config

# New instance properties
DEFAULT_MACHINE_TYPE = 'n1-standard-1'
DEFAULT_NETWORK = 'default'
DEFAULT_IMAGE = 'debian-7-wheezy-v20140828'
DEFAULT_ZONE = 'us-central1-a'
API_VERSION = 'v1'
GCE_URL = 'https://www.googleapis.com/compute/%s/projects/' % (API_VERSION)
PROJECT_ID = 'di-game-server'
CLIENT_SECRETS = 'client_secrets.json'
OAUTH2_STORAGE = 'oauth2.dat' # FIXME: will this need to be refreshed??? Might break later
GCE_SCOPE = 'https://www.googleapis.com/auth/compute'

def create_instance(new_instance_name, disk_name, poll=False):
  logging.basicConfig(level=logging.INFO)

  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])

  # No flags passed for now
  flags = parser.parse_args([])

  # Perform OAuth 2.0 authorization.
  flow = flow_from_clientsecrets(CLIENT_SECRETS, scope=GCE_SCOPE)
  # FIXME: this will not write out new credentials to oauth2.dat
  # add a flag/check to test if running locally (can't write to file
  # on appengine).
  storage = Storage(OAUTH2_STORAGE)
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, flags)
  http = httplib2.Http()
  auth_http = credentials.authorize(http)

  # Build the service
  gce_service = build('compute', API_VERSION)
  project_url = '%s%s' % (GCE_URL, PROJECT_ID)

  # List instances
  request = gce_service.instances().list(project=PROJECT_ID, filter=None, zone=DEFAULT_ZONE)
  response = request.execute(http=auth_http)
  if response and 'items' in response:
    instances = response['items']
    for instance in instances:
      print instance['name']
  else:
    print 'No instances to list.'

  # Construct URLs
  image_url = '%s%s/global/images/%s' % (
         GCE_URL, 'debian-cloud', DEFAULT_IMAGE)
  machine_type_url = '%s/zones/%s/machineTypes/%s' % (
        project_url, DEFAULT_ZONE, DEFAULT_MACHINE_TYPE)
  network_url = '%s/global/networks/%s' % (project_url, DEFAULT_NETWORK)

  request_body = config.create_request(new_instance_name, disk_name)
  print 'The request body is:', request_body
  # Create the instance
  request = gce_service.instances().insert(
       project=PROJECT_ID,
       body=request_body,
       zone=DEFAULT_ZONE)
  response = request.execute(http=auth_http)

  print response

  if poll:
    response = _blocking_call(gce_service, auth_http, response)

  return response

def _blocking_call(gce_service, auth_http, response):
  """Blocks until the operation status is done for the given operation."""

  status = response['status']
  while status != 'DONE' and response:
    operation_id = response['name']

    # Identify if this is a per-zone resource
    if 'zone' in response:
      zone_name = response['zone'].split('/')[-1]
      request = gce_service.zoneOperations().get(
          project=PROJECT_ID,
          operation=operation_id,
          zone=zone_name)
    else:
      request = gce_service.globalOperations().get(
           project=PROJECT_ID, operation=operation_id)

    response = request.execute(http=auth_http)
    if response:
      status = response['status']
  return response

if __name__ == '__main__':
  print create_instance('a-test-instance', poll=True)
