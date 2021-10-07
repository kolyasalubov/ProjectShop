"""
The purpose of this module is to create an aware bot client that will raise error, if it don't get whats expected
"""

import functools

from client.client import bot_client
from client.exceptions import ServerError, ClientError


def status_code_check(function):
    """
    Decorator will check response status code, and raises respective error for error handlers to handle.
    If status code is good, then return just result of method
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        if response.status_code >= 500:
            raise ServerError(response=response)
        elif response.status_code >= 400:
            raise ClientError(response=response)
        else:
            return response

    return wrapper


def client_decorator(instance):
    """
    This decorator is used to put a decorator on RestClient instance
    """

    @functools.wraps(instance)
    def wrapper():
        decorated_attr = status_code_check(getattr(instance, "send_request"))
        setattr(instance, "send_request", decorated_attr)

    return wrapper


bot_client = client_decorator(bot_client)
