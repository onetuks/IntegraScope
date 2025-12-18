from email.utils import format_datetime
from typing import TypedDict, Optional

from fastapi import HTTPException

from app.server.lang_chain.chain_runner import LangChainClient
from langgraph.graph import END, StateGraph

from app.server.services.log.error_log import ErrorLogService


class GraphState(TypedDict, total=False):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: str
    log_end: str
    log: str
    status_code: Optional[int]
    exception: Optional[str]
    analysis: Optional[str]
    solution: Optional[str]


class LangGraphClient:

    def __init__(self, chain_client: LangChainClient):
        self._chain_client = chain_client
        self._graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(GraphState)

        builder.add_node("error_log", self._error_log)
        builder.add_node("analysis", self._analysis)
        builder.add_node("solution", self._solution)

        builder.set_entry_point("error_log")
        builder.add_edge("error_log", "analysis")
        builder.add_edge("analysis", "solution")
        builder.add_edge("solution", END)

        return builder.compile()

    def _error_log(self, state: GraphState) -> GraphState:
        artifact_id = state["artifact_id"]
        error_data = ErrorLogService().request_error_data(artifact_id)
        return {
            "artifact_id": artifact_id,
            "artifact_type": error_data.artifact_type,
            "package_id": error_data.package_id,
            "message_guid": error_data.message_guid,
            "log_start": format_datetime(error_data.log_start),
            "log_end": format_datetime(error_data.log_end),
            "log": error_data.log,
            "status_code": error_data.status_code,
            "exception": error_data.exception,
        }

    def run(self, artifact_id: str):
        init_state: GraphState = {"artifact_id": artifact_id}
        try:
            return self._graph.invoke(init_state)
        except HTTPException as exc:
            raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
