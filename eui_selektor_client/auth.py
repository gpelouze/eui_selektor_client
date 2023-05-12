import os

import requests
import requests.auth


class HTTPAuthClient:

    def __init__(self, credentials_id: str):
        self.credentials_id = credentials_id
        self.__http_auth = self._get_http_auth()

    def _get_http_auth(self):
        """ Get a HTTPBasicAuth object with credentials from environment """
        username = os.getenv('EUI_SELEKTOR_USERNAME')
        password = os.getenv('EUI_SELEKTOR_PASSWORD')
        if not (username and password):
            raise ValueError(
                'Could not retrieve credentials. '
                'Please set environment variables '
                '$EUI_SELEKTOR_USERNAME and $EUI_SELEKTOR_PASSWORD.'
                )
        return requests.auth.HTTPBasicAuth(username, password)

    def query(self, url, params=None):
        """ Send an HTTP query and return response. """
        auth = self.__http_auth
        with requests.get(url, params=params, auth=auth) as r:
            r.raise_for_status()
        return r