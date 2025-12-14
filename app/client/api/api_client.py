from typing import Optional

import requests

SERVER_BASE_URL = "http://localhost:8000"


async def get(uri: Optional[str] = None):
  return requests.get(SERVER_BASE_URL + uri).raise_for_status()


async def post(uri: Optional[str] = None, body: Optional[dict] = None):
  return requests.post(SERVER_BASE_URL + uri, json=body).raise_for_status()


async def put(uri: Optional[str] = None, body: Optional[dict] = None):
  return requests.put(SERVER_BASE_URL + uri, json=body).raise_for_status()


async def delete(uri: Optional[str] = None):
  return requests.delete(SERVER_BASE_URL + uri).raise_for_status()
