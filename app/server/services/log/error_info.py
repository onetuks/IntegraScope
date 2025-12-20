import requests

from app.server.utils.config import get_config


class ErrorInfoApiClient:
  """SAP IS Error Log fetch service"""

  _URL = get_config().sap_is_base_url + "/MessageProcessingLogErrorInformations('"

  def __init__(self, session: requests.Session | None = None):
    self._session = session or requests.Session()

  def get_err_log(self, message_guid: str, token: str = None) -> str:
    response = self._session.get(
        url=f"{self._URL}{message_guid}')/$value",
        headers={
          'Accept': 'application/json',
          'Authorization': f'Bearer {token}'
        },
    )
    response.raise_for_status()
    return response.text
