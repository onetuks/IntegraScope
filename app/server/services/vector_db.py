# from __future__ import annotations

# from typing import Any, Dict, List, Optional
# from uuid import uuid4

# import chromadb
# from chromadb.api import Collection
# from chromadb.utils import embedding_functions

# from app.server.utils.config import get_config
# from app.server.utils.logger import logger


# class VectorDBService:
#     """Manage ChromaDB component and error_cases collection (HTTP or local)."""

#     COLLECTION_NAME = "integrascope"

#     def __init__(
#         self,
#         embedding_model: str = "all-MiniLM-L6-v2",
#         enable_hybrid: bool = True,
#         host: Optional[str] = None,
#         port: Optional[int] = None,
#     ):
#         config = get_config()
#         self.embedding_model = embedding_model
#         self.enable_hybrid = enable_hybrid
#         self.host = host if host is not None else config.chroma_host
#         self.port = port if port is not None else config.chroma_port

#         self._embedding_function = self._init_embedding_function(embedding_model)
#         self._client = self._init_client()
#         self._collection = self._init_collection()

#     @property
#     def client(self) -> chromadb.ClientAPI:
#         return self._client

#     @property
#     def collection(self) -> Collection:
#         return self._collection

#     def _init_client(self) -> chromadb.ClientAPI:
#         """
#         Use HTTP component when CHROMA_HOST is provided; otherwise fall back to
#         embedded persistent component.
#         """
#         return chromadb.HttpClient(host=self.host, port=self.port)

#     def _init_embedding_function(
#         self,
#         model_name: str,
#     ):
#         """
#         Initialize the embedding function, falling back to default if custom model
#         load fails (e.g., missing weights offline).
#         """
#         try:
#             return embedding_functions.SentenceTransformerEmbeddingFunction(
#                 model_name=model_name
#             )
#         except Exception as exc:
#             logger.warning(
#                 "Falling back to default embedding function",
#                 extra={"model": model_name, "error": str(exc)},
#             )
#             try:
#                 return embedding_functions.DefaultEmbeddingFunction()
#             except Exception as default_exc:
#                 logger.warning(
#                     "Default embedding function unavailable",
#                     extra={"error": str(default_exc)},
#                 )
#                 return None

#     def _init_collection(self) -> Collection:
#         metadata = {
#             "description": "Error cases with embeddings for similarity search",
#             "schema_http_status": "integer",
#             "schema_exception": "string",
#             "schema_error_type": "string",
#             "schema_error_cause": "string",
#             "schema_error_solution": "string",
#             "schema_artifact_id": "string",
#             "schema_artifact_type": "string",
#             "schema_artifact_name": "string",
#             "schema_package_id": "string",
#             "schema_package_name": "string",
#             "schema_message_guid": "string",
#             "schema_correlation_id": "string",
#         }

#         if self.enable_hybrid:
#             metadata["enable_hybrid"] = True
#             metadata["hybrid_lexical"] = True

#         return self._client.get_or_create_collection(
#             name=self.COLLECTION_NAME,
#             metadata=metadata,
#             embedding_function=self._embedding_function,
#         )

#     def upsert(self, cases: List[Dict[str, Any]]) -> List[str]:
#         """
#         Store or update error cases. Each case requires a `text` field;
#         optional metadata keys: iflow_id, adapter_type, error_type, created_at.
#         """
#         if not cases:
#             return []

#         ids: List[str] = []
#         documents: List[str] = []
#         metadatas: List[Dict[str, Any]] = []

#         for case in cases:
#             ids.append(case.get("id") or str(uuid4()))
#             documents.append(case["text"])
#             metadata = {
#                 "http_status": case.get("http_status"),
#                 "exception": case.get("exception"),
#                 "error_type": case.get("error_type"),
#                 "error_cause": case.get("error_cause"),
#                 "error_solution": case.get("error_solution"),
#                 "artifact_id": case.get("artifact_id"),
#                 "artifact_type": case.get("artifact_type"),
#                 "artifact_name": case.get("artifact_name"),
#                 "package_id": case.get("package_id"),
#                 "package_name": case.get("package_name"),
#                 "message_guid": case.get("message_guid"),
#                 "correlation_id": case.get("correlation_id"),
#             }
#             # Strip None values to keep collection filters clean.
#             metadatas.append({k: v for k, v in metadata.items() if v is not None})

#         self._collection.upsert(
#             ids=ids,
#             documents=documents,  # 임베딩 벡터 생성 대상
#             metadatas=metadatas,  # 검색 결과 필터링/분류 위한 부가정보
#         )
#         return ids

#     def query_similar(
#         self,
#         text: str,
#         top_k: int = 5,
#         where: Optional[Dict[str, Any]] = None,
#         where_document: Optional[Dict[str, Any]] = None,
#         include: Optional[List[str]] = None,
#     ):
#         """Retrieve similar error cases with optional metadata filters."""
#         _include = include or [
#             "documents",
#             "embeddings",
#             "metadatas",
#             "distances",
#             "uris",
#             "data",
#         ]
#         return self._collection.query(
#             query_texts=[text],
#             n_results=top_k,
#             where=where,
#             where_document=where_document,
#             include=_include,
#         )

#     def query_similarity(
#         self,
#         text: str,
#         top_k: int = 5,
#         where: Optional[Dict[str, Any]] = None,
#         where_document: Optional[Dict[str, Any]] = None,
#         include: Optional[List[str]] = None,
#     ):
#         """Alias for query_similar to match expected naming in call sites."""
#         return self.query_similar(
#             text=text,
#             top_k=top_k,
#             where=where,
#             where_document=where_document,
#             include=include,
#         )

#     def healthcheck(self) -> bool:
#         """Basic connectivity check against the Chroma component and collection."""
#         try:
#             heartbeat = getattr(self._client, "heartbeat", None)
#             if callable(heartbeat):
#                 heartbeat()

#             self._collection.count()
#             return True
#         except Exception as exc:
#             logger.exception(
#                 "ChromaDB health check failed",
#                 extra={"error": str(exc)},
#             )
#             return False
