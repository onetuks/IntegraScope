from typing import List

import requests

from app.server.sap.oauth2 import OAuth2Client
from app.server.utils.config import get_config
from app.server.utils.http import request_json


class ObjectSearch:
    def __init__(self, session: requests.Session | None = None):
        self._session = session or requests.Session()
        self._oauth2_client = OAuth2Client(self._session)
        self._base_url = f"{get_config().sap_is_base_url}/IntegrationPackages"

    def get_package_list(self) -> List[str]:
        payload = request_json(
            self._session,
            "GET",
            self._base_url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._oauth2_client.get_access_token()}",
            },
        )
        results = payload["d"]["results"]
        return [result["Id"] for result in results]

    def get_artifact_list(self, package_id: str) -> List[str]:
        payload = request_json(
            self._session,
            "GET",
            f"{self._base_url}('{package_id}')/IntegrationDesigntimeArtifacts",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._oauth2_client.get_access_token()}",
            },
        )
        results = payload["d"]["results"]
        return [result["Id"] for result in results]
