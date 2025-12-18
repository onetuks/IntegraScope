import datetime
from typing import TypedDict, Optional

from app.server.lang_chain.chain_runner import LangChainClient


class GraphState(TypedDict, total=False):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: str
    log_end: str
    log: str
    status_code: int
    exception: str
    analysis: Optional[str]
    solution: Optional[str]


class LangGraphClient:
    def __init__(self, chain_client: LangChainClient):
        self._chain_client = chain_client
        self._graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph()