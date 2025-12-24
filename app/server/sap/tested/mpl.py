from datetime import datetime
from typing import List, Optional
from urllib.parse import quote

import requests
from pydantic import BaseModel

from app.server.sap.oauth2 import OAuth2Client
from app.server.utils.config import get_config
from app.server.utils.datetime import ms_to_tz, to_gmt_0, to_gmt_9


class TestedMplDto(BaseModel):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    correlation_id: str
    log_start: datetime
    log_end: datetime
    status: str


def _build_filter(log_start: str, log_end: str) -> str:
    exp = (
        f"LogStart gt datetimeoffset'{log_start}Z'"
        f" and LogEnd lt datetimeoffset'{log_end}Z'"
    )
    return quote(exp, safe="'=:T-")


class TestedMplClient:
    _URL = f"{get_config().sap_is_base_url}/MessageProcessingLogs"

    def __init__(self, session: requests.Session | None = None):
        self._session = session or requests.Session()
        self._oauth2_client = OAuth2Client(self._session)

    def get_tested_artifacts(self,
                             log_start: datetime,
                             log_end: datetime,
                             status: str) -> List[TestedMplDto]:
        """
        Fetch Message Processing Logs for period(LogStart ~ LogEnd)
        :param log_start: 로그 시작 시간
        :param log_end: 로그 종료 시간
        :param status: 테스트 상태
        :return: TestedMplDto
        """
        gmt_log_start, gmt_log_end = to_gmt_0(log_start), to_gmt_0(log_end)

        datetime_format = "%Y-%m-%dT%H:%M:%S"

        response = self._session.get(
            url=f"{self._URL}?$filter=" +
                f"LogStart gt datetime'{gmt_log_start.strftime(datetime_format)}'" +
                f" and LogEnd lt datetime'{gmt_log_end.strftime(datetime_format)}'" +
                (f" and Status eq '{status}'" if status is not None and status != 'ALL' else ""),
            headers={
                'Accept': 'application/json',
                'Authorization': f"Bearer {self._oauth2_client.get_access_token()}"
            })

        json = response.json()
        artifacts = json["d"]["results"][:min(20, len(json["d"]["results"]))]

        tested_artifacts = list()
        for artifact in artifacts:
            tested_artifacts.append(
                TestedMplDto(
                    artifact_id=artifact["IntegrationArtifact"]["Id"],
                    artifact_type=artifact["IntegrationArtifact"]["Type"],
                    package_id=artifact["IntegrationArtifact"]["PackageId"],
                    message_guid=artifact["MessageGuid"],
                    correlation_id=artifact["CorrelationId"],
                    log_start=to_gmt_9(ms_to_tz(artifact["LogStart"][6:-2])),
                    log_end=to_gmt_9(ms_to_tz(artifact["LogEnd"][6:-2])),
                    status=artifact["Status"],
                )
            )
        return sorted(tested_artifacts, key=lambda a: a.log_start, reverse=True)
