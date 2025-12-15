from app.server.models.mpl import MessageProcessingLogDto


class MPLService:
  """SAP IS Message Processing Log API Request Client"""

  _URL = "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com/api/v1/MessageProcessingLogs?$filter=IntegrationFlowName eq "

  def __init__(self):
    pass

  def get_mpl(self, artifact_id: str) -> MessageProcessingLogDto:
    