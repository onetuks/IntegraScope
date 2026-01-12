from __future__ import annotations

import logging
import os
from typing import Optional

import requests
from requests import Response

logger = logging.getLogger("client.api")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


def _get_default_timeout() -> Optional[float]:
    value = os.getenv("API_TIMEOUT_SECONDS")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


DEFAULT_TIMEOUT_SECONDS = _get_default_timeout()
_SESSION = requests.Session()


def _build_url(uri: Optional[str]) -> str:
    if not uri:
        return API_BASE_URL
    if uri.startswith(("http://", "https://")):
        return uri
    if not uri.startswith("/"):
        uri = f"/{uri}"
    return f"{API_BASE_URL}{uri}"


def _request(method: str, uri: Optional[str], **kwargs) -> Response:
    timeout = kwargs.pop("timeout", DEFAULT_TIMEOUT_SECONDS)
    if timeout is not None:
        kwargs["timeout"] = timeout
    url = _build_url(uri)
    try:
        response = _SESSION.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.RequestException:
        logger.exception("API request failed", extra={"method": method, "url": url})
        raise


def get(
    uri: Optional[str] = None,
    params: Optional[dict] = None,
    timeout: Optional[float] = None,
) -> Response:
    return _request("GET", uri, params=params, timeout=timeout)


def post(
    uri: Optional[str] = None,
    body: Optional[dict] = None,
    timeout: Optional[float] = None,
) -> Response:
    return _request("POST", uri, json=body, timeout=timeout)


def put(
    uri: Optional[str] = None,
    body: Optional[dict] = None,
    timeout: Optional[float] = None,
) -> Response:
    return _request("PUT", uri, json=body, timeout=timeout)


def delete(uri: Optional[str] = None, timeout: Optional[float] = None) -> Response:
    return _request("DELETE", uri, timeout=timeout)
