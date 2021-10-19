from requests import HTTPError


class ClientError(HTTPError):
    """
    Error for all responses with status code 4xx.
    """
    pass


class ServerError(HTTPError):
    """
    Error for all responses with status coe 5xx
    """
    pass
