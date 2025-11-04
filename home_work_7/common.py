import requests
from typing import Any


class BadRequestError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class BadStatusCodeError(Exception):
    def __init__(self, status_code: int):
        self.status_code = status_code


def make_request(method: str, url: str, body: Any | None = None) -> requests.Response:
    response = requests.request(method, url, data=body, timeout=10)
    
    match response.status_code:
        case code if 200 <= code < 300:
            pass
        case 400:
            raise BadRequestError()
        case 403:
            raise ForbiddenError()
        case _:
            raise BadStatusCodeError(response.status_code)
    
    return response
