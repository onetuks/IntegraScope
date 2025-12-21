from email.utils import format_datetime
from typing import TypedDict, Optional

from cachetools.func import lru_cache
from fastapi import HTTPException
from langgraph.graph import END, StateGraph

from app.server.lang_chain.chain_runner import LangChainClient, \
  get_langchain_client, AgentType
from app.server.sap.log.error_log import ErrorLogService


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
      "status_code": error_data.status_code,
      "exception": error_data.exception,
    }

  def _analysis(self, state: GraphState) -> GraphState:
    artifact_type = state["artifact_type"]
    log = state["log"]
    status_code = state["status_code"]
    exception = state["exception"]
    try:
      analysis = self._chain_client.run_chain(agent_type=AgentType.ANALYSIS,
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
      solution = self._chain_client.run_chain(agent_type=AgentType.SOLUTION,
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

  def run(self, message_guid: str):
    init_state: GraphState = {"message_guid": message_guid}
    try:
      return self._graph.invoke(init_state)
    except HTTPException as exc:
      raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
      raise HTTPException(status_code=500, detail=str(exc)) from exc


@lru_cache(maxsize=1)
def get_langgraph_client():
  return LangGraphClient(get_langchain_client())
