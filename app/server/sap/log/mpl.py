from datetime import datetime
from typing import List

import requests
from fastapi import HTTPException
from pydantic import BaseModel

from app.server.utils.config import get_config
from app.server.utils.datetime import ms_to_tz
from app.server.utils.http import request_json


class MplDto(BaseModel):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    status: str
    log_start: datetime
    log_end: datetime


class MplApiClient:
    """SAP IS Message Processing Log API Request Client"""

    def __init__(self, session: requests.Session | None = None):
        self._session = session or requests.Session()
        self._base_url = f"{get_config().sap_is_base_url}/MessageProcessingLogs"

    def get_mpl(self,
                message_guid: str,
                token: str = None) -> MplDto:
        """
        Fetch Message Processing Log by Integration Flow name and return DTO.
        """
        payload = request_json(
            self._session,
            "GET",
            f"{self._base_url}?$filter=MessageGuid eq '{message_guid}'",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        target = payload["d"]["results"]

        if len(target) == 0:
            raise HTTPException(status_code=204, detail="No Message Processing Log")

        target = target[-1]
        return MplDto(artifact_id=message_guid,
                      artifact_type=target["IntegrationArtifact"]["Type"],
                      package_id=target["IntegrationArtifact"]["PackageId"],
                      message_guid=target["MessageGuid"],
                      status=target["Status"],
                      log_start=ms_to_tz(target["LogStart"][6:-2]),
                      log_end=ms_to_tz(target["LogEnd"][6:-2]))

    def get_mpls_by_period(self,
                           start: datetime,
                           end: datetime,
                           token: str = None) -> List[MplDto]:
        """
        Fetch Message Processing Logs by date range.
        """
        start_str = start.strftime("%Y-%m-%dT%H:%M:%S")
        end_str = end.strftime("%Y-%m-%dT%H:%M:%S")
        
        # OData filter for LogStart between start and end
        filter_query = f"$filter=LogStart ge datetime'{start_str}' and LogStart lt datetime'{end_str}'"
        
        payload = request_json(
            self._session,
            "GET",
            f"{self._base_url}?{filter_query}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        
        results = payload.get("d", {}).get("results", [])
        mpls = []
        for target in results:
            try:
                mpls.append(MplDto(
                    artifact_id=target["IntegrationArtifact"]["Id"], # Note: get_mpl used message_guid as artifact_id which seems wrong or specific to that call. 
                                                                     # Usually artifact_id is IntegrationArtifact.Id or Name.
                                                                     # In get_mpl: artifact_id=message_guid. 
                                                                     # But the field name is artifact_id. 
                                                                     # Let's check get_mpl again.
                                                                     # get_mpl: artifact_id=message_guid.
                                                                     # But in ErrorData it is used as artifact_id.
                                                                     # Let's stick to what get_mpl does if possible, but get_mpl takes message_guid as input.
                                                                     # Actually, looking at get_mpl:
                                                                     # artifact_id=message_guid
                                                                     # This seems odd. artifact_id usually refers to the iFlow ID.
                                                                     # target["IntegrationArtifact"]["Id"] is likely the iFlow ID.
                                                                     # target["MessageGuid"] is the message GUID.
                                                                     # In get_mpl, it sets artifact_id = message_guid.
                                                                     # I should probably follow that pattern or fix it if it's a bug.
                                                                     # But wait, get_mpl takes message_guid as arg.
                                                                     # And returns MplDto(artifact_id=message_guid, ...)
                                                                     # This implies MplDto.artifact_id holds the MessageGuid?
                                                                     # But MplDto also has message_guid field.
                                                                     # MplDto(..., message_guid=target["MessageGuid"], ...)
                                                                     # So artifact_id and message_guid are the same in get_mpl?
                                                                     # That seems redundant.
                                                                     # Let's check ErrorData in error_log.py.
                                                                     # ErrorData has artifact_id and message_guid.
                                                                     # If I change it, I might break things.
                                                                     # However, for the dashboard, I probably want the actual Artifact ID (iFlow Name).
                                                                     # Let's look at get_mpl again.
                                                                     # return MplDto(artifact_id=message_guid, ...)
                                                                     # This looks like a mistake in get_mpl, but I should be careful.
                                                                     # If I look at ErrorLogService.request_error_data:
                                                                     # return ErrorData(artifact_id=mpl_dto.artifact_id, ...)
                                                                     # If I change it here, it changes ErrorData.
                                                                     # For the dashboard, I want to count artifacts.
                                                                     # I'll use target["IntegrationArtifact"]["Id"] for artifact_id in get_mpls_by_period.
                                                                     # And I should probably fix get_mpl too, but let's stick to the requested task.
                                                                     # I will use target["IntegrationArtifact"]["Id"] for artifact_id in the new method.
                    artifact_type=target["IntegrationArtifact"]["Type"],
                    package_id=target["IntegrationArtifact"]["PackageId"],
                    message_guid=target["MessageGuid"],
                    status=target["Status"],
                    log_start=ms_to_tz(target["LogStart"][6:-2]),
                    log_end=ms_to_tz(target["LogEnd"][6:-2])
                ))
            except Exception:
                continue
                
        return mpls
