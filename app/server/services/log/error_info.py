import requests


class ErrorInfoApiClient:
    """SAP IS Error Log fetch service"""

    _URL = "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogErrorInformations('"

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
