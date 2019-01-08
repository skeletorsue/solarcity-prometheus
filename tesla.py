import time
import json
import requests


class Tesla:
    username = None
    password = None
    access_token = None
    token_expire = 0
    key_cache_file = None
    api_url = 'https://owner-api.teslamotors.com/api'

    def __init__(self, username, password, key_cache_file=None):
        self.username = username
        self.password = password
        self.key_cache_file = key_cache_file
        return

    def _get_access_token(self):
        if self.token_expire > time.time():
            return self.access_token

        try:
            if self.key_cache_file is not None:
                with open(self.key_cache_file) as f:
                    data = json.load(f)
                    if data["token_expire"] > time.time():
                        self.token_expire = data["token_expire"]
                        self.access_token = data["access_token"]
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            print("Unable to load access cache file")

        if self.token_expire < time.time():
            req = requests.post('https://owner-api.teslamotors.com/oauth/token', json={
                'grant_type':    'password',
                'client_id':     'e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e',
                'client_secret': 'c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220',
                'email':         self.username,
                'password':      self.password
            })
            if req.status_code == 200:
                response = req.json()
                self.access_token = response['access_token']
                self.token_expire = time.time() + response['expires_in']
                # print('Your token is: %s' % response['access_token'])
                # print('This token will expire: %s' % (datetime.datetime.fromtimestamp(response['created_at']) + datetime.timedelta(seconds=response['expires_in'])))
            elif req.status_code == 401:
                print('Incorrect username or password')
                raise UserWarning
            elif req.status_code == 404:
                print('API server has changed, contact the developer of this script')
                raise ModuleNotFoundError
            elif req.status_code == 500:
                print('An internal server error occurred. Either Tesla API is down or the API has changed since this script was developed.')
                raise ConnectionError
            else:
                print(req.reason)
                raise EnvironmentError

            if self.key_cache_file is not None:
                with open(self.key_cache_file, "w") as f:
                    json.dump({"access_token": self.access_token, "token_expire": self.token_expire}, f)

        return self.access_token

    def list_products(self):
        r = requests.get(
                '%s/1/products' % self.api_url,
                headers={'Authorization': 'Bearer ' + self._get_access_token()}
        )

        return r.json()['response']

    def solar_status(self, site_id):
        r = requests.get(
                '%s/1/energy_sites/%s/live_status' % (self.api_url, site_id),
                headers={'Authorization': 'Bearer ' + self._get_access_token()}
        )

        return r.json()
