from datetime import datetime

import requests
from fastapi import HTTPException
from pydantic import BaseModel

from app.server.utils.config import get_config
from app.server.utils.datetime import ms_to_tz


class MplDto(BaseModel):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: datetime
    log_end: datetime


class MplApiClient:
    """SAP IS Message Processing Log API Request Client"""

    _URL = (get_config().sap_is_base_url +
            "/MessageProcessingLogs?" + "$filter=MessageGuid eq ")

    def __init__(self, session: requests.Session | None = None):
        self._session = session or requests.Session()

    def get_mpl(self,
                message_guid: str,
                token: str = None) -> MplDto:
        """
        Fetch Message Processing Log by Integration Flow name and return DTO.
        """
        response = self._session.get(
            url=f"{self._URL}'{message_guid}'",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            },
        )
        response.raise_for_status()

        json = response.json()
        target = json["d"]["results"]

        if len(target) == 0:
            raise HTTPException(status_code=204, detail="No Message Processing Log")

        target = target[-1]
        return MplDto(artifact_id=message_guid,
                      artifact_type=target["IntegrationArtifact"]["Type"],
                      package_id=target["IntegrationArtifact"]["PackageId"],
                      message_guid=target["MessageGuid"],
                      log_start=ms_to_tz(target["LogStart"][6:-2]),
                      log_end=ms_to_tz(target["LogEnd"][6:-2]))
