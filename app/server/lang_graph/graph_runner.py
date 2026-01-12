from email.utils import format_datetime
from enum import Enum
from typing import TypedDict, Optional

from cachetools.func import lru_cache
from fastapi import HTTPException
from langgraph.graph import END, StateGraph

from app.server.lang_chain import AnalysisModel
from app.server.lang_chain.chain_runner import LangChainClient, \
    get_langchain_client, AgentType
from app.server.sap.log.error_log import ErrorLogService


class ActionType(Enum):
    ERROR_LOG = "error_log"
    ANALYSIS = "analysis"
    SOLUTION = "solution"
    RESOLVE_WITH_ANALYSIS = "resolve_with_analysis"


class GraphState(TypedDict, total=False):
    action_type: ActionType
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: str
    log_end: str
    log: str
    origin_log: str
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

        builder.add_node("print_state_node", self._print_state)
        builder.add_node("error_log_node", self._error_log)
        builder.add_node("analysis_node", self._analysis)
        builder.add_node("solution_node", self._solution)

        builder.set_entry_point("print_state_node")
        builder.add_conditional_edges("print_state_node",
                                      self._route,
                                      {
                                          "error_log": "error_log_node",
                                          "analysis": "analysis_node",
                                          "solution": "solution_node",
                                          "resolve_with_analysis": "error_log_node"
                                      })
        builder.add_conditional_edges("error_log_node",
                                      self._route,
                                      {
                                          "error_log": END,
                                          "resolve_with_analysis": "analysis_node"
                                      })
        builder.add_conditional_edges("analysis_node",
                                      self._route,
                                      {
                                          "analysis": END,
                                          "resolve_with_analysis": "solution_node"
                                      })
        builder.add_edge("solution_node", END)

        return builder.compile()

    def _route(self, state: GraphState) -> str:
        action_type_ = state["action_type"]
        return action_type_.value

    def _print_state(self, state: GraphState) -> GraphState:
        print("action_type: ", state.get("action_type"))
        print("artifact_id: ", state.get("artifact_id"))
        print("artifact_type: ", state.get("artifact_type"))
        print("package_id: ", state.get("package_id"))
        print("message_guid: ", state.get("message_guid"))
        print("log_start: ", state.get("log_start"))
        print("log_end: ", state.get("log_end"))
        print("log: ", state.get("log"))
        print("origin_log: ", state.get("origin_log"))
        print("status_code: ", state.get("status_code"))
        print("exception: ", state.get("exception"))
        print("analysis: ", state.get("analysis"))
        print("solution: ", state.get("solution"))
        return state

    def _error_log(self, state: GraphState) -> GraphState:
        artifact_id = state["message_guid"]
        error_data = ErrorLogService().request_error_data(artifact_id)
        return {
            "artifact_id": error_data.artifact_id,
            "artifact_type": error_data.artifact_type,
            "package_id": error_data.package_id,
            "message_guid": error_data.message_guid,
            "log_start": format_datetime(error_data.log_start),
            "log_end": format_datetime(error_data.log_end),
            "log": error_data.log,
            "origin_log": error_data.origin_log,
            "status_code": error_data.status_code,
            "exception": error_data.exception,
        }

    def _analysis(self, state: GraphState) -> GraphState:
        artifact_type = state["artifact_type"]
        log = state["log"]
        status_code = state["status_code"]
        exception = state["exception"]
        try:
            analysis = self._chain_client.run_chain(
                agent_type=AgentType.ANALYSIS,
                artifact_type=artifact_type,
                status_code=status_code,
                exception=exception, log=log)
            return {
                "analysis": analysis,
            }
        except TypeError as e:
            raise HTTPException(status_code=500,
                                detail="Prompt format Failed" + str(e))
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail="Analysis chain Failed: " + str(e))

    def _solution(self, state: GraphState) -> GraphState:
        artifact_type = state["artifact_type"]
        log = state["log"]
        status_code = state["status_code"]
        exception = state["exception"]
        try:
            solution = self._chain_client.run_chain(
                agent_type=AgentType.SOLUTION,
                artifact_type=artifact_type,
                status_code=status_code,
                exception=exception, log=log, )
            return {
                "solution": solution,
            }
        except TypeError as e:
            raise HTTPException(status_code=400,
                                detail="Prompt format Failed" + str(e))
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail="Solution chain Failed: " + str(e))

    def run(self,
            message_guid: str,
            action_type: ActionType,
            artifact_id: str = None,
            artifact_type: str = None,
            package_id: str = None,
            log_start: str = None,
            log_end: str = None,
            log: str = None,
            origin_log: str = None,
            status_code: int = None,
            exception: str = None,
            analysis: AnalysisModel = None,
            ):
        init_state: GraphState = {"message_guid": message_guid,
                                  "action_type": action_type,
                                  "artifact_id": artifact_id,
                                  "artifact_type": artifact_type,
                                  "package_id": package_id,
                                  "log_start": log_start,
                                  "log_end": log_end,
                                  "log": log,
                                  "origin_log": origin_log,
                                  "status_code": status_code,
                                  "exception": exception,
                                  "analysis": analysis}
        try:
            return self._graph.invoke(init_state)
        except HTTPException as exc:
            raise HTTPException(status_code=exc.status_code,
                                detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc


@lru_cache(maxsize=1)
def get_langgraph_client():
    return LangGraphClient(get_langchain_client())
