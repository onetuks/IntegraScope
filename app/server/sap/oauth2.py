from __future__ import annotations

import time
from typing import Optional

import requests

from app.server.utils.config import get_config
from app.server.utils.logger import logger


class OAuth2Client:
  """
  Retrieve and cache OAuth2 access tokens for SAP IS APIs, reusing a shared
  requests.Session with Authorization header set.
  """

  def __init__(self, session: Optional[requests.Session] = None):
    cfg = get_config()
    self._session = session or requests.Session()
    self._token_url = cfg.sap_is_token_url
    self._client_id = cfg.sap_is_client_id
    self._client_secret = cfg.sap_is_client_secret

    self._access_token: Optional[str] = None
    self._expires_at: float = 0.0

  @property
  def session(self) -> requests.Session:
    """Return the shared session (auto-authenticated after get_access_token)."""
    return self._session

  def get_access_token(self, force_refresh: bool = False) -> str:
    """
    Return a cached access token, refreshing if expired or forced.
    """
    if (not force_refresh and self._access_token
        and time.time() < self._expires_at):
      return self._access_token

    return self._refresh_token()

  def authorized_session(self) -> requests.Session:
    """
    Ensure the session has a valid Authorization header and return it.
    """
    self.get_access_token()
    return self._session

  def _refresh_token(self) -> str:
    payload = {"grant_type": "client_credentials"}
    headers = {"Accept": "application/json"}

    response = self._session.post(
        self._token_url,
        data=payload,
        headers=headers,
        auth=(self._client_id, self._client_secret),
    )
    response.raise_for_status()

    data = response.json()
    token = data.get("access_token")
    token_type = data.get("token_type", "Bearer")
    expires_in = data.get("expires_in", 0)

    if not token:
      raise ValueError("OAuth token response missing access_token")

    ttl = max(int(expires_in), 0)
    # Renew a bit early to avoid edge expirations.
    self._expires_at = time.time() + (ttl * 0.9 if ttl else 300)
    self._access_token = token

    self._session.headers.update(
        {"Authorization": f"{token_type} {token}"})

    logger.info(
        "Fetched OAuth2 token",
        extra={
          "token_url": self._token_url,
          "expires_in": expires_in,
        },
    )
    return token
