import requests


PHONE_NUMBER = ""      # Crete admin is_bot user and insert his/her phone_number
PASSWORD = ""          # Crete admin is_bot user and insert his/her password
SERVER_HOST = "http://localhost:8000/"
TOKEN_URL = 'user/token/'
TOKEN_REFRESH_URL = 'user/token/refresh/'
LOGOUT_URL = 'user/token/logout/'


class RestClient:

    METHODS = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
    }

    def __init__(self, phone_number, password, server_host, token_url, token_refresh_url, logout_url):
        self.phone_number = phone_number
        self.password = password
        self.server_host = server_host
        self.token_url = token_url
        self.token_refresh_url = token_refresh_url
        self.logout_url = logout_url
        self.access = ''
        self.refresh = ''

    def _obtain_tokens(self):
        url = self.server_host + self.token_url
        data = {
            "phone_number": self.phone_number,
            "password": self.password
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access = response.json().get('access')
            self.refresh = response.json().get('refresh')
        return response.status_code

    def _refresh_tokens(self):
        url = self.server_host + self.token_refresh_url
        data = {"refresh": self.refresh}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access = response.json().get('access')
            self.refresh = response.json().get('refresh')
        return response.status_code

    def _authenticate(self):
        status = self._refresh_tokens()
        if status in (400, 401):
            status = self._obtain_tokens()
        return status

    def logout(self):
        url = self.server_host + self.logout_url
        data = {"refresh": self.refresh}
        response = requests.post(url, data=data)
        return response

    def send_request(self, method, url, data=None):
        request_method = self.METHODS.get(method)
        if request_method is None:
            response = requests.Response()
            response.status_code = 405
            return response
        url = self.server_host + url
        response = request_method(url, headers={'Authorization': f"Bearer {self.access}"}, data=data)

        if response.status_code in (400, 401):
            auth_status = self._authenticate()
            if auth_status != 200:
                response = requests.Response()
                response.status_code = auth_status
                return response
            else:
                response = request_method(url, headers={'Authorization': f"Bearer {self.access}"}, data=data)
        return response


bot_client = RestClient(PHONE_NUMBER, PASSWORD, SERVER_HOST, TOKEN_URL, TOKEN_REFRESH_URL, LOGOUT_URL)
# Use only next methods: logout, send_request
