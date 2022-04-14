import getpass

import keyring
import requests
import requests.auth


class CredentialsManager:
    def __init__(self, credentials_id: str):
        self.credentials_id = credentials_id
        self.username_key = self.credentials_id + '_USERNAME'

    @staticmethod
    def _get_credentials_from_user():
        """ Get credentials from user """
        username = input('Username: ')
        password = getpass.getpass()
        return username, password

    def _store_credentials_to_keyring(self, credentials):
        """ Store credentials to the keyring """
        username, password = credentials
        keyring.set_password(self.credentials_id, self.username_key, username)
        keyring.set_password(self.credentials_id, username, password)

    def _retrieve_credentials_from_keyring(self):
        """ Retrieve credentials from the keyring """
        username = keyring.get_password(self.credentials_id, self.username_key)
        if username is None:
            return None
        password = keyring.get_password(self.credentials_id, username)
        if password is None:
            return None
        return username, password

    def get_credentials(self, force_keyring_update=False):
        """ Get credentials, either from user input or keyring

        Parameters
        ==========
        force_keyring_update : bool (default: False)
            If True, update the credentials that are already stored in the
            keyring. This means that credentials will be requested to the user.

        Returns
        =======
        username : str
        password : str
        """
        credentials = self._retrieve_credentials_from_keyring()
        if (credentials is None) or force_keyring_update:
            credentials = self._get_credentials_from_user()
            self._store_credentials_to_keyring(credentials)
        return credentials


class HTTPAuthClient:

    def __init__(self, credentials_id: str):
        self.credentials_id = credentials_id
        self.__http_auth = self._get_http_auth()

    def _get_http_auth(self):
        """ Get a HTTPBasicAuth object populated using CredentialsManager() """
        cred = CredentialsManager(self.credentials_id).get_credentials()
        return requests.auth.HTTPBasicAuth(*cred)

    def update_credentials(self):
        """ Update the username and password stored in the keyring
        (users will be asked to type them in).
        """
        CredentialsManager(self.credentials_id).get_credentials(
            force_keyring_update=True)
        self.__http_auth = self._get_http_auth()

    def query(self, url, params=None):
        """ Send an HTTP query and return response. """
        auth = self.__http_auth
        with requests.get(url, params=params, auth=auth) as r:
            r.raise_for_status()
        return r