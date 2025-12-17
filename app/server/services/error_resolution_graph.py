# from __future__ import annotations

# from typing import Any, Callable, Dict, Optional, TypedDict

# from langgraph.graph import END, StateGraph

# from app.server.services.error_log import ErrorData, ErrorLogService
# from app.server.services.llm_runner import make_langchain_gemini_runner
# from app.server.services.vector_db import VectorDBService


# class ErrorResolutionState(TypedDict, total=False):
#     artifact_id: str
#     similarity_threshold: float
#     top_k: int
#     error_data: ErrorData
#     document: str
#     vector_results: Dict[str, Any]
#     best_distance: Optional[float]
#     best_score: Optional[float]
#     vector_hits: Optional[list]
#     vector_upsert_ids: Any
#     llm_answer: Any
#     final_response: Dict[str, Any]


# class ErrorResolutionGraph:
#     """
#     LangGraph workflow that:
#     1) Pulls MPL/ErrInfo via ErrorLogService
#     2) Queries Chroma for similar cases
#     3) Falls back to LLM when similarity is below threshold
#     """

#     def __init__(
#         self,
#         vector_db: Optional[VectorDBService] = None,
#         error_log_service: Optional[ErrorLogService] = None,
#         llm_runner: Optional[Callable[[Dict[str, Any]], Any]] = None,
#         default_similarity_threshold: float = 0.35,
#         default_top_k: int = 5,
#     ):
#         self._vector_db = vector_db or VectorDBService()
#         self._error_log_service = error_log_service or ErrorLogService()
#         # Use provided LLM runner or fall back to Gemini runner (free-tier friendly).
#         self._llm_runner = llm_runner or make_langchain_gemini_runner()
#         self._default_similarity_threshold = default_similarity_threshold
#         self._default_top_k = default_top_k
#         self._graph = self._build_graph()

#     def invoke(
#         self,
#         artifact_id: str,
#         similarity_threshold: Optional[float] = None,
#         top_k: Optional[int] = None,
#     ):
#         initial_state: ErrorResolutionState = {
#             "artifact_id": artifact_id,
#             "similarity_threshold": (
#                 similarity_threshold
#                 if similarity_threshold is not None
#                 else self._default_similarity_threshold
#             ),
#             "top_k": top_k if top_k is not None else self._default_top_k,
#         }
#         return self._graph.invoke(initial_state)

#     # --- graph construction -------------------------------------------------
#     def _build_graph(self):
#         graph = StateGraph(ErrorResolutionState)
#         graph.add_node("fetch_error_data", self._fetch_error_data)
#         graph.add_node("vector_query", self._vector_query)
#         graph.add_node("llm_fallback", self._llm_fallback)
#         graph.add_node("return_vector_result", self._return_vector_result)

#         graph.set_entry_point("fetch_error_data")
#         graph.add_edge("fetch_error_data", "vector_query")
#         graph.add_conditional_edges(
#             "vector_query",
#             self._should_use_llm,
#             {"llm": "llm_fallback", "vector": "return_vector_result"},
#         )
#         graph.add_edge("llm_fallback", END)
#         graph.add_edge("return_vector_result", END)
#         return graph.compile()

#     # --- nodes --------------------------------------------------------------
#     def _fetch_error_data(self, state: ErrorResolutionState) -> ErrorResolutionState:
#         error_data = self._error_log_service.request_error_data(
#             artifact_id=state["artifact_id"]
#         )
#         return {
#             "error_data": error_data,
#             "document": error_data.log,
#         }

#     def _vector_query(self, state: ErrorResolutionState) -> ErrorResolutionState:
#         results = self._vector_db.query_similarity(
#             text=state["document"], top_k=int(state.get("top_k", self._default_top_k))
#         )

#         best_distance: Optional[float] = None
#         best_score: Optional[float] = None
#         distances = results.get("distances") if isinstance(results, dict) else None
#         scores = results.get("scores") if isinstance(results, dict) else None

#         if scores and isinstance(scores, list) and scores[0]:
#             first_row = scores[0] if isinstance(scores[0], list) else scores
#             if first_row:
#                 best_score = first_row[0]

#         if (
#             best_score is None
#             and distances
#             and isinstance(distances, list)
#             and distances[0]
#         ):
#             first_row = distances[0] if isinstance(distances[0], list) else distances
#             if first_row:
#                 best_distance = first_row[0]
#                 best_score = 1 / (1 + best_distance)

#         hits = self._extract_hits(results)

#         return {
#             "vector_results": results,
#             "best_distance": best_distance,
#             "best_score": best_score,
#             "vector_hits": hits,
#         }

#     def _llm_fallback(self, state: ErrorResolutionState) -> ErrorResolutionState:
#         payload = {
#             "artifact_type": state["error_data"].artifact_type,
#             "status_code": state["error_data"].status_code,
#             "exception_name": state["error_data"].exception_name,
#             "log": state.get("document"),
#             "vector_results": state.get("vector_results"),
#         }
#         answer = self._llm_runner(payload)

#         vector_ids = self._vector_db.upsert(
#             [
#                 {
#                     "id": state["error_data"].message_guid,
#                     "text": state.get("document"),
#                     "http_status": state["error_data"].status_code,
#                     "exception": state["error_data"].exception_name,
#                     "artifact_id": state["error_data"].artifact_id,
#                     "artifact_type": state["error_data"].artifact_type,
#                     "artifact_name": state["error_data"].artifact_name,
#                     "package_id": state["error_data"].package_id,
#                     "package_name": state["error_data"].package_name,
#                     "message_guid": state["error_data"].message_guid,
#                     "correlation_id": state["error_data"].correlation_id,
#                     "error_type": answer.get("error_type"),
#                     "error_cause": answer.get("error_cause"),
#                     "error_solution": answer.get("error_solution"),
#                 }
#             ]
#         )

#         return {
#             "llm_answer": answer,
#             "vector_upsert_ids": vector_ids,
#             "final_response": {
#                 "source": "llm",
#                 "artifact_id": state.get("artifact_id"),
#                 "metadata": {
#                     "artifact_id": state["error_data"].artifact_id,
#                     "artifact_type": state["error_data"].artifact_type,
#                     "artifact_name": state["error_data"].artifact_name,
#                     "package_id": state["error_data"].package_id,
#                     "package_name": state["error_data"].package_name,
#                     "message_guid": state["error_data"].message_guid,
#                     "correlation_id": state["error_data"].correlation_id,
#                 },
#                 "document": state.get("document"),
#                 "vector_results": state.get("vector_results"),
#                 "llm_answer": answer,
#                 "vector_upsert_ids": vector_ids,
#             },
#         }

#     def _return_vector_result(
#         self, state: ErrorResolutionState
#     ) -> ErrorResolutionState:
#         threshold = float(
#             state.get("similarity_threshold", self._default_similarity_threshold)
#         )
#         passing_hits = [
#             hit
#             for hit in (state.get("vector_hits") or [])
#             if (
#                 (hit.get("score") is not None and hit["score"] >= threshold)
#                 or (hit.get("distance") is not None and hit["distance"] <= threshold)
#             )
#         ]
#         return {
#             "final_response": {
#                 "source": "vector_db",
#                 "artifact_id": state.get("artifact_id"),
#                 "metadata": {
#                     "artifact_id": state["error_data"].artifact_id,
#                     "artifact_type": state["error_data"].artifact_type,
#                     "artifact_name": state["error_data"].artifact_name,
#                     "package_id": state["error_data"].package_id,
#                     "package_name": state["error_data"].package_name,
#                     "message_guid": state["error_data"].message_guid,
#                     "correlation_id": state["error_data"].correlation_id,
#                 },
#                 "document": state.get("document"),
#                 "vector_results": state.get("vector_results"),
#                 "best_distance": state.get("best_distance"),
#                 "best_score": state.get("best_score"),
#                 "hits": state.get("vector_hits"),
#                 "hits_meeting_threshold": passing_hits,
#             }
#         }

#     # --- routers ------------------------------------------------------------
#     def _should_use_llm(self, state: ErrorResolutionState) -> str:
#         score = state.get("best_score")
#         distance = state.get("best_distance")
#         threshold = float(
#             state.get("similarity_threshold", self._default_similarity_threshold)
#         )
#         if score is not None:
#             return "vector" if score >= threshold else "llm"
#         if distance is not None:
#             return "vector" if distance <= threshold else "llm"
#         return "llm"

#     # --- helpers -----------------------------------------------------------
#     def _extract_hits(self, results: Dict[str, Any]) -> list:
#         docs = results.get("documents") if isinstance(results, dict) else None
#         metas = results.get("metadatas") if isinstance(results, dict) else None
#         distances = results.get("distances") if isinstance(results, dict) else None
#         scores = results.get("scores") if isinstance(results, dict) else None

#         docs_row = docs[0] if docs and isinstance(docs[0], list) else docs or []
#         metas_row = metas[0] if metas and isinstance(metas[0], list) else metas or []
#         dist_row = (
#             distances[0]
#             if distances and isinstance(distances[0], list)
#             else distances or []
#         )
#         score_row = (
#             scores[0] if scores and isinstance(scores[0], list) else scores or []
#         )

#         hits = []
#         max_len = max(len(docs_row), len(metas_row), len(dist_row), len(score_row))
#         for idx in range(max_len):
#             hits.append(
#                 {
#                     "document": docs_row[idx] if idx < len(docs_row) else None,
#                     "metadata": metas_row[idx] if idx < len(metas_row) else None,
#                     "distance": dist_row[idx] if idx < len(dist_row) else None,
#                     "score": score_row[idx] if idx < len(score_row) else None,
#                 }
#             )
#         return hits
