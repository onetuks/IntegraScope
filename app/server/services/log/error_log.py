from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests

from app.server.services.component import (ErrorInfoApiClient, MplApiClient,
                                           OAuth2Client)
from app.server.services.log.error_regulation import \
    ErrorLogRegulationComponent


@dataclass
class ErrorData:
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: datetime
    log_end: datetime
    log: str
    status_code: Optional[int]
    exception: Optional[str]


class ErrorLogService:
    """
    Extract Error Log Service

    1. OAuth2 -> get Access Token
    2. Request MPL of target InterfaceFlowName -> get MPLDto (metadata)
    3. Request ErrInfo of target MessageGuid -> get ErrorLog (document)

    Now, I can pass the document and metadata to vector_db.
    If there is no document similar enough, we have to query to LLM.
    Otherwise, there is any document similar enough, we will return it.
    """

    def __init__(self):
        self._session = requests.Session()
        self._oauth2_client = OAuth2Client(session=self._session)
        self._mpl_api_client = MplApiClient(session=self._session)
        self._error_info_api_client = ErrorInfoApiClient(session=self._session)
        self._error_log_regulation = ErrorLogRegulationComponent()
        self._token = self._oauth2_client.get_access_token()

    def request_error_data(self, artifact_id: str) -> ErrorData:
        mpl_dto = self._mpl_api_client.get_mpl(artifact_id=artifact_id,
                                               token=self._token)
        raw_log = self._error_info_api_client.get_err_log(
            message_guid=mpl_dto.message_guid, token=self._token)
        log_dto = self._error_log_regulation.normalize_log(log=raw_log)

        return ErrorData(
            artifact_id=mpl_dto.artifact_id,
            artifact_type=mpl_dto.artifact_type,
            package_id=mpl_dto.package_id,
            message_guid=mpl_dto.message_guid,
            log_start=mpl_dto.log_start,
            log_end=mpl_dto.log_end,
            log=log_dto.normalized_log,
            status_code=log_dto.status_code,
            exception=log_dto.exception,
        )
