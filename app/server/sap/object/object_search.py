from typing import List

import requests

from app.server.sap.oauth2 import OAuth2Client
from app.server.utils.config import get_config


class ObjectSearch:
    _URL = f"{get_config().sap_is_base_url}/IntegrationPackages"

    def __init__(self, session: requests.Session | None = None):
        self._session = session or requests.Session()
        self._oauth2_client = OAuth2Client(self._session)

    def get_package_list(self) -> List[str]:
        response = self._session.get(
            url=self._URL,
            headers={
                "Accept": "application/json",
                'Authorization': f"Bearer {self._oauth2_client.get_access_token()}"
            }
        )

        json = response.json()
        results = json["d"]["results"]
        return [result["Id"] for result in results]

    def get_artifact_list(self, package_id: str) -> List[str]:
        response = self._session.get(
            url=f"{self._URL}('{package_id}')/IntegrationDesigntimeArtifacts",
            headers={
                "Accept": "application/json",
                'Authorization': f"Bearer {self._oauth2_client.get_access_token()}"
            }
        )

        json = response.json()
        results = json["d"]["results"]
        return [result["Id"] for result in results]
