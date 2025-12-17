from datetime import datetime, timezone

import requests
from pydantic import BaseModel


def _ms_to_tz(ms: str, tz: str = 'UTC') -> datetime:
    """
    ms: Unix timestamp in milliseconds
    tz: timezone string(e.g 'Asia/Seoul', 'UTC')
    """
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)


class MplDto(BaseModel):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: datetime
    log_end: datetime


class MplApiClient:
    """SAP IS Message Processing Log API Request Client"""

    _URL = ("https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com/api/v1" +
            "/MessageProcessingLogs?" + "$filter=IntegrationFlowName eq ")

    def __init__(self, session: requests.Session | None = None):
        self._session = session or requests.Session()

    def get_mpl(self,
                artifact_id: str,
                token: str = None) -> MplDto:
        """
        Fetch Message Processing Log by Integration Flow name and return DTO.
        """
        response = self._session.get(
            url=f"{self._URL}'{artifact_id}'",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            },
        )
        response.raise_for_status()

        json = response.json()
        target = json["d"]["results"][-1]

        return MplDto(artifact_id=artifact_id,
                      artifact_type=target["IntegrationArtifact"]["Type"],
                      package_id=target["IntegrationArtifact"]["PackageId"],
                      message_guid=target["MessageGuid"],
                      log_start=_ms_to_tz(target["LogStart"][6:-2]),
                      log_end=_ms_to_tz(target["LogEnd"][6:-2]))
