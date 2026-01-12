from __future__ import annotations

from typing import Any, Dict

import requests

from app.server.utils.logger import logger

DEFAULT_TIMEOUT_SECONDS = 30.0


def request_json(
    session: requests.Session,
    method: str,
    url: str,
    **kwargs,
) -> Dict[str, Any]:
    response = _request(session, method, url, **kwargs)
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        logger.exception(
            "Failed to decode JSON response",
            extra={"method": method, "url": url},
        )
        raise


def request_text(
    session: requests.Session,
    method: str,
    url: str,
    **kwargs,
) -> str:
    response = _request(session, method, url, **kwargs)
    response.raise_for_status()
    return response.text


def _request(
    session: requests.Session,
    method: str,
    url: str,
    **kwargs,
) -> requests.Response:
    timeout = kwargs.pop("timeout", DEFAULT_TIMEOUT_SECONDS)
    try:
        return session.request(method, url, timeout=timeout, **kwargs)
    except requests.RequestException:
        logger.exception(
            "HTTP request failed",
            extra={"method": method, "url": url},
        )
        raise
