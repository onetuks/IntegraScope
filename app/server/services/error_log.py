from dataclasses import dataclass

import requests

from app.server.models.mpl import MessageProcessingLogDto
from app.server.services.component import ErrorInfoApiClient, MplApiClient, OAuth2Client
from app.server.services.component.regulation import ErrorLogRegulationComponent


@dataclass
class ErrorData:
    metadata: MessageProcessingLogDto
    document: str


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
        mpl_dto = self._mpl_api_client.get_mpl(
            artifact_id=artifact_id, token=self._token
        )
        raw_log = self._error_info_api_client.get_err_log(
            message_guid=artifact_id, token=self._token
        )
        document = self._error_log_regulation.build_document_from_log(log=raw_log)

        return ErrorData(metadata=mpl_dto, document=document)
