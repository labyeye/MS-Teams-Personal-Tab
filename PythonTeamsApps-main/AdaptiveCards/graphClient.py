import requests
import os
import sys
import base64
from microsoftgraph.client import Client

this = sys.modules[__name__]
this.cache = None

graph_url = 'https://graph.microsoft.com/v1.0'


class GraphClient():
    def __init__(self, token):
      if ((token == None) or (token.strip() == "")):
        raise Exception("SimpleGraphClient: Invalid token received.")

      self._token = token
      if this.cache is None:
        this.cache = dict()

      self.graphClient = Client(os.environ.get("MicrosoftAppId"), os.environ.get("MicrosoftAppPassword"))

    def getuserprofile(self):
      user = requests.get(
        '{0}/me'.format(graph_url),
        headers={
          'Authorization': 'Bearer {0}'.format(self._token)
        })
      return user.json()

    def getuserphoto(self, user_id):
      if user_id not in this.cache:
        photo_response = requests.get(
          '{0}/me/photo/$value'.format(graph_url),
          headers={
          'Authorization': 'Bearer {0}'.format(self._token)
          }, stream=True)

        photo = photo_response.raw.read()
        this.cache[user_id] = base64.b64encode(photo).decode('utf-8')
        return this.cache[user_id]
