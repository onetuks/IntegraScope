# from __future__ import annotations

# from typing import Any, Callable, Dict, List, Optional

# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI

# from app.server.utils.config import get_config

# PROMPT_TEMPLATE = """
# You are a SAP Cloud Integration error analyst.
# Summarize the issue and propose remediation. Return ONLY valid JSON with keys:
# - error_type: short label (e.g., AUTH_ERROR, NETWORK_ERROR, VALIDATION_ERROR, UNKNOWN)
# - error_cause: brief one-liner cause
# - error_solution: 2-4 concise remediation steps in a single string; use bullet/numbering inside the string if helpful.

# Context to use (id-like values removed):
# - artifact_type: {artifact_type}
# - status_code: {status_code}
# - exception_name: {exception_name}
# - log: {log}

# Nearest vector matches (distance is Chroma distance; smaller is more similar):
# {matches}

# {format_instructions}
# """.strip()


# def _format_top_matches(vector_results: Dict[str, Any], limit: int = 3) -> str:
#   docs: List[Any] = (vector_results or {}).get("documents") or []
#   metas: List[Any] = (vector_results or {}).get("metadatas") or []
#   distances: List[Any] = (vector_results or {}).get("distances") or []

#   if not docs:
#     return "No similar cases found."

#   doc_rows = docs[0] if isinstance(docs[0], list) else docs
#   meta_rows = metas[0] if metas and isinstance(metas[0], list) else metas
#   dist_rows = distances[0] if distances and isinstance(distances[0],
#                                                        list) else distances

#   def _sanitize(meta: Any) -> Any:
#     if not isinstance(meta, dict):
#       return meta
#     return {
#       k: v
#       for k, v in meta.items()
#       if k
#          not in {
#            "artifact_id",
#            "artifact_name",
#            "artifact_type",
#            "package_id",
#            "package_name",
#            "message_guid",
#            "correlation_id",
#          }
#     }

#   lines: List[str] = []
#   for idx, doc in enumerate(doc_rows[:limit]):
#     meta = _sanitize(meta_rows[idx] if idx < len(meta_rows) else {})
#     dist = dist_rows[idx] if idx < len(dist_rows) else None
#     lines.append(
#         f"- match#{idx + 1} distance={dist}: metadata={meta}\n  document:\n{doc}"
#     )
#   return "\n".join(lines)


# def make_langchain_gemini_runner(
#     model_name: Optional[str] = None, temperature: Optional[float] = None
# ) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
#   """
#   Create an LLM runner using LangChain + Gemini (free-tier friendly) returning structured JSON.
#   """
#   config = get_config()
#   llm = ChatGoogleGenerativeAI(
#       model=model_name or config.gemini_model,
#       temperature=temperature if temperature is not None else config.gemini_temperature,
#       max_output_tokens=1024,
#       google_api_key=config.google_api_key,
#   )

#   parser = JsonOutputParser()
#   prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#   chain = prompt.partial(
#     format_instructions=parser.get_format_instructions()) | llm | parser

#   def _run(payload: Dict[str, Any]) -> Dict[str, Any]:
#     matches = _format_top_matches(payload.get("vector_results"))
#     return chain.invoke(
#         {
#           "artifact_type": payload.get("artifact_type"),
#           "status_code": payload.get("status_code"),
#           "exception_name": payload.get("exception_name"),
#           "log": payload.get("log") or "",
#           "matches": matches,
#         }
#     )

#   return _run
