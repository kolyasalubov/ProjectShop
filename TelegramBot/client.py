import requests
import os


PHONE_NUMBER = os.environ.get('BOT_PHONE_NUMBER')      # Crete admin is_bot user and insert his/her phone_number
PASSWORD = os.environ.get('BOT_PASSWORD')          # Crete admin is_bot user and insert his/her password
SERVER_HOST = os.environ.get('SERVER_HOST')         # "http://localhost:8000/" insert for local testing
TOKEN_URL = 'users/token/'
TOKEN_REFRESH_URL = 'users/token/refresh/'
LOGOUT_URL = 'users/token/logout/'


class RestClient:
    """
    Implement client for JWT token authentication.

    Attributes:
        self.METHODS (dict): Includes allowed HTTP methods
        self.phone_number (str): The phone number for authentication
        self.password (str): The password for authentication
        self.server_host (str): The server address
        self.token_url (str): The url for obtaining tokens
        self.token_refresh_url (str): The url for refreshing tokens
        self.logout_url (str): The url for log out
        self.access (str): access token
        self.refresh (str): refresh token
    """

    METHODS = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'PATCH': requests.patch,
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

    def _obtain_tokens(self) -> int:
        """
        Obtain access and refresh tokens using self.phone_number and self.password.

        Return authentication status code: int
        """
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

    def _refresh_tokens(self) -> int:
        """
        Refresh access and refresh tokens using self.refresh.

        Return authentication status code: int
        """
        url = self.server_host + self.token_refresh_url
        data = {"refresh": self.refresh}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access = response.json().get('access')
            self.refresh = response.json().get('refresh')
        return response.status_code

    def _authenticate(self) -> int:
        """
        Ensure JWT token authentication flow.

        Return authentication status code: int
        """
        status = self._refresh_tokens()
        if status in (400, 401):
            status = self._obtain_tokens()
        return status

    def logout(self) -> requests.Response:
        """
        Ensures log out through blacklisting refresh token.

        Return: requests.Response object
        """
        url = self.server_host + self.logout_url
        data = {"refresh": self.refresh}
        headers = {'Authorization': f"Bearer {self.access}"}
        response = requests.post(url, headers=headers, data=data)
        return response

    def send_request(self, method: str, url: str, headers: dict = None, data: dict = None,
                     params: dict = None) -> requests.Response:
        """
        Provide sending request.

        Parameters:
            method (str): request's method
            url (str): request's url
            headers (dict, None): additional request's headers
            data (dict, None): request's body
            params (dict, None): additional data to send via URL

        Return: request.Response object
        """
        request_method = self.METHODS.get(method)
        if headers:
            headers.update({'Authorization': f"Bearer {self.access}"})
        else:
            headers = {'Authorization': f"Bearer {self.access}"}

        if request_method is None:
            response = requests.Response()
            response.status_code = 405
            return response

        url = self.server_host + url
        response = request_method(url, headers=headers, data=data, params=params)

        if response.status_code == 401:
            auth_status = self._authenticate()
            if auth_status != 200:
                response = requests.Response()
                response.status_code = auth_status
                return response
            else:
                headers['Authorization'] = f"Bearer {self.access}"
                response = request_method(url, headers=headers, data=data, params=params)
        return response



bot_client = RestClient(PHONE_NUMBER, PASSWORD, SERVER_HOST, TOKEN_URL, TOKEN_REFRESH_URL, LOGOUT_URL)
# Use only next methods: logout, send_request
