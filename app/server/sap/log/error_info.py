import requests

from app.server.utils.config import get_config
from app.server.utils.http import request_text


class ErrorInfoApiClient:
  """SAP IS Error Log fetch service"""

  def __init__(self, session: requests.Session | None = None):
    self._session = session or requests.Session()
    self._base_url = (
      f"{get_config().sap_is_base_url}"
      "/MessageProcessingLogErrorInformations('"
    )

  def get_err_log(self, message_guid: str, token: str = None) -> str:
    return request_text(
        self._session,
        "GET",
        f"{self._base_url}{message_guid}')/$value",
        headers={
          "Accept": "application/json",
          "Authorization": f"Bearer {token}",
        },
    )
