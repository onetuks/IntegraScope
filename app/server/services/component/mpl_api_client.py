import requests

from app.server.models.mpl import MessageProcessingLogDto
from app.server.models.mpl import MplResponse
from app.server.models.mpl import MessageProcessingLog
from app.server.models.mpl import IntegrationArtifact


class MplApiClient:
  """SAP IS Message Processing Log API Request Client"""

  _URL = "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com/api/v1/MessageProcessingLogs?$filter=IntegrationFlowName eq "

  def __init__(self, session: requests.Session | None = None):
    self._session = session or requests.Session()

  def get_mpl(self,
      artifact_id: str,
      token: str = None
  ) -> MessageProcessingLogDto:
    """
    Fetch Message Processing Log by Integration Flow name and return DTO.
    """
    response = self._session.get(
        url=f"{self._URL}{artifact_id}",
        headers={
          "Accept": "application/json",
          "Authorization": f"Bearer {token}"
        },
    )
    response.raise_for_status()

    mpl_response = MplResponse.model_validate(response.json())
    if not mpl_response.d.results:
      raise ValueError(f"No MPL found for artifact_id={artifact_id}")

    mpl: MessageProcessingLog = mpl_response.d.results[-1]
    artifact: IntegrationArtifact | None = mpl.integration_artifact

    return MessageProcessingLogDto(
        message_guid=mpl.message_guid,
        correlation_id=mpl.correlation_id or "",
        artifact_id=(artifact.id if artifact else ""),
        artifact_name=(artifact.name if artifact else ""),
        artifact_type=(artifact.type if artifact else ""),
        package_id=(artifact.package_id if artifact else ""),
        package_name=(artifact.package_name if artifact else ""),
    )
