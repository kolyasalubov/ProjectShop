import os

import requests
from dotenv import load_dotenv

load_dotenv("../.env")

PHONE_NUMBER = os.environ.get(
    "BOT_PHONE_NUMBER"
)  # Crete admin is_bot user and insert his/her phone_number
PASSWORD = os.environ.get(
    "BOT_PASSWORD"
)  # Crete admin is_bot user and insert his/her password
SERVER_HOST = os.environ.get(
    "SERVER_HOST"
)  # "http://localhost:8000/" insert for local testing
API_ROOT = os.environ.get("API_ROOT")
TOKEN_URL = os.environ.get("TOKEN_URL")
TOKEN_REFRESH_URL = os.environ.get("TOKEN_REFRESH_URL")
LOGOUT_URL = os.environ.get("LOGOUT_URL")


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
        self.get_user_ib_by_telegram_id_url (str): The url for retrieving user id by user telegram id
        self.get_user_ib_by_phone_number_url (str): The url for retrieving user id by user phone number
        self.access (str): access token
        self.refresh (str): refresh token
    """

    METHODS = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete,
        "PATCH": requests.patch,
    }

    def __init__(
        self,
        phone_number,
        password,
        server_host,
        api_root,
        token_url,
        token_refresh_url,
        logout_url,
    ):
        self.phone_number = phone_number
        self.password = password
        self.server_host = server_host
        self.api_root = api_root
        self.token_url = token_url
        self.token_refresh_url = token_refresh_url
        self.logout_url = logout_url
        self.access = ""
        self.refresh = ""

    def _obtain_tokens(self) -> int:
        """
        Obtain access and refresh tokens using self.phone_number and self.password.

        Return authentication status code: int
        """

        url = self.server_host + self.token_url
        data = {"phone_number": self.phone_number, "password": self.password}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access = response.json().get("access")
            self.refresh = response.json().get("refresh")
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
            self.access = response.json().get("access")
            self.refresh = response.json().get("refresh")
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
        headers = {"Authorization": f"Bearer {self.access}"}
        response = requests.post(url, headers=headers, data=data)
        return response

    def send_request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        data: dict = None,
        params: dict = None,
    ) -> requests.Response:
        """
        Provide sending request.

        Parameters:
            method (str): request method
            url (str): request url
            headers (dict, None): additional request headers
            data (dict, None): request body
            params (dict, None): additional data to send via URL

        Return: request.Response object
        """

        request_method = self.METHODS.get(method)
        if headers:
            headers.update({"Authorization": f"Bearer {self.access}"})
        else:
            headers = {"Authorization": f"Bearer {self.access}"}

        if request_method is None:
            response = requests.Response()
            response.status_code = 405
            return response

        if self.server_host not in url:
            url = self.server_host + self.api_root + url

        response = request_method(url, headers=headers, data=data, params=params)

        if response.status_code == 401:
            auth_status = self._authenticate()
            if auth_status != 200:
                response = requests.Response()
                response.status_code = auth_status
                return response
            else:
                headers["Authorization"] = f"Bearer {self.access}"
                response = request_method(
                    url, headers=headers, data=data, params=params
                )
        return response


bot_client = RestClient(
    phone_number=PHONE_NUMBER,
    password=PASSWORD,
    server_host=SERVER_HOST,
    api_root=API_ROOT,
    token_url=TOKEN_URL,
    token_refresh_url=TOKEN_REFRESH_URL,
    logout_url=LOGOUT_URL,
    )

# Use only next methods: logout, send_request
