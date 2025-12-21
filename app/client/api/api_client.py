from typing import Optional

import requests
from requests import Response

API_BASE_URL = "http://localhost:8000"


def get(uri: Optional[str] = None) -> Response:
    response = requests.get(API_BASE_URL + uri)
    response.raise_for_status()
    return response


def post(uri: Optional[str] = None, body: Optional[dict] = None, timeout: Optional[int] = None) -> Response:
    response = requests.post(API_BASE_URL + uri, json=body, timeout=timeout)
    response.raise_for_status()
    return response


def put(uri: Optional[str] = None, body: Optional[dict] = None) -> Response:
    response = requests.put(API_BASE_URL + uri, json=body)
    response.raise_for_status()
    return response


def delete(uri: Optional[str] = None):
    response = requests.delete(API_BASE_URL + uri)
    response.raise_for_status()
    return response
