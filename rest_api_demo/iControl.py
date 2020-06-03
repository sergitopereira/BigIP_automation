import requests
import json

__version__ = '1.0'


class IControl(object):
    def __init__(self, ip_address, port):
        self.ip = ip_address
        self.port = port
        self.headers = {
            'Content-Type': 'application/json',
            'X-F5-Auth-Token': None
        }
        self.url_base = f"https://{self.ip}:{self.port}/mgmt/tm"
        self.f5token = None

    def get_call(self, url):
        """
        HTTP method GET
        :param url: resource identifier
        :return: json restfull api response
        """
        r = requests.get(url, headers=self.headers, verify=False)
        try:
            if r.status_code == 200:
                return r.json()
            else:
                raise SystemExit(f'iControl GET API call failed, HTTP RESPONSE code {r.status_code}')
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def post_call(self, url, post_data):
        """
        HTTP method POST
        :param url: resource identifier
        :param post_data: post data
        :return: json rest api response
        """
        r = requests.post(url, json.dumps(post_data), headers=self.headers, verify=False)
        try:
            if r.status_code == 200:
                return r.json()
            else:
                raise SystemExit(f'iControl POST API call failed, HTTP RESPONSE code {r.status_code}; error {r.content}'
                                 )
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def patch_call(self, url, patch_data):
        """
        HTTP Method PATCH
        :param url: url for api call
        :param patch_data: patch data
        :return: json rest api
        """
        r = requests.patch(url, json.dumps(patch_data), headers=self.headers, verify=False)
        try:
            if r.status_code == 200:
                return r.json()
            else:
                raise RuntimeError(
                    f'iControl PATCH API call failed, HTTP RESPONSE code {r.status_code}; error {r.content}')
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def put_call(self, url, put_data):
        """
        HTTP METHOD PUT
        :param url: url for api call
        :param put_data: put data
        :return: json rest api
        """
        try:
            r = requests.put(url, json.dumps(put_data), headers=self.headers, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                raise SystemExit('iControl PUT API call failed,HTTP RESPONSE code {r.status_code}; error {r.content}')

        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def get_token(self, username, password):
        """
        :param username: F5 username
        :param password: F5 password
        :return:
        """
        url_auth = f"https://{self.ip}:{self.port}/mgmt/shared/authn/login"
        post_data = {
            'username': username,
            'password': password,
            'loginProviderName': 'tmos'
        }
        r = requests.post(
            url_auth, json.dumps(post_data), auth=(username, password),
            headers=self.headers, verify=False
        )
        try:
            if r.status_code == 200:
                self.f5token = r.json()['token']['token']
                self.headers['X-F5-Auth-Token'] = self.f5token
            else:
                raise SystemExit(f'was not possible to generate a token, status code = {r.status_code}')
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

    def list_virtual_servers(self, filer=None):
        """
        method to list ltm virtual servers
        :return: list of virtual servers
        """
        url = f"{self.url_base}/ltm/virtual/"
        r = self.get_call(url)
        print(self.headers)
        print(f'curl -jkv {url} -x GET -H\'{self.headers}\'')
        return r