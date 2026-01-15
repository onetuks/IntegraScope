from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from typing import Any, Dict, List, Optional

from app.server.utils.config import get_config
from app.server.utils.logger import logger

_METADATA_KEYS = (
    "artifact_id",
    "artifact_type",
    "package_id",
    "message_guid",
    "status_code",
    "exception",
    "log_start",
    "log_end",
)


@dataclass(frozen=True)
class SimilarCase:
    distance: Optional[float]
    metadata: Dict[str, Any]
    document: Optional[str]

    @property
    def analysis(self) -> Optional[Dict[str, Any]]:
        return _load_json(self.metadata.get("analysis_json"))

    @property
    def solution(self) -> Optional[Dict[str, Any]]:
        return _load_json(self.metadata.get("solution_json"))


def _load_json(value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def _dump_json(payload: Optional[Dict[str, Any]]) -> Optional[str]:
    if payload is None:
        return None
    try:
        return json.dumps(payload, ensure_ascii=False)
    except (TypeError, ValueError):
        return None


def _build_document(
    log: Optional[str],
    status_code: Optional[int],
    exception: Optional[str],
    artifact_type: Optional[str],
) -> str:
    parts: List[str] = []
    if artifact_type:
        parts.append(f"artifact_type: {artifact_type}")
    if status_code is not None:
        parts.append(f"status_code: {status_code}")
    if exception:
        parts.append(f"exception: {exception}")
    if log:
        parts.append("log:")
        parts.append(log)
    return "\n".join(parts).strip()


def _build_metadata(
    payload: Dict[str, Any],
    analysis: Optional[Dict[str, Any]] = None,
    solution: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}
    for key in _METADATA_KEYS:
        value = payload.get(key)
        if value is None:
            continue
        if key == "status_code":
            try:
                value = int(value)
            except (TypeError, ValueError):
                continue
        if not isinstance(value, (int, float, bool, str)):
            value = str(value)
        metadata[key] = value

    analysis_json = _dump_json(analysis)
    if analysis_json:
        metadata["analysis_json"] = analysis_json
    solution_json = _dump_json(solution)
    if solution_json:
        metadata["solution_json"] = solution_json
    return metadata


def _case_id(payload: Dict[str, Any]) -> str:
    seed = "|".join(
        str(payload.get(key) or "")
        for key in ("artifact_type", "status_code", "exception", "log")
    )
    return sha256(seed.encode("utf-8")).hexdigest()


class ChromaErrorLogStore:
    def __init__(self):
        config = get_config()
        try:
            import chromadb
            from chromadb.utils import embedding_functions
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "chromadb is not available. Install chromadb and "
                "sentence-transformers to enable vector search."
            ) from exc

        self._threshold = config.chroma_similarity_threshold
        self._client = chromadb.HttpClient(
            host=config.chroma_host,
            port=config.chroma_port,
        )
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.chroma_embedding_model,
        )
        self._collection = self._client.get_or_create_collection(
            name=config.chroma_collection,
            metadata={"hnsw:space": "cosine"},
            embedding_function=embedding_fn,
        )

    def find_similar(
        self,
        payload: Dict[str, Any],
        top_k: int = 3,
    ) -> List[SimilarCase]:
        query_text = _build_document(
            log=payload.get("log"),
            status_code=payload.get("status_code"),
            exception=payload.get("exception"),
            artifact_type=payload.get("artifact_type"),
        )
        if not query_text:
            raise ValueError("log is required for similarity search")

        result = self._collection.query(
            query_texts=[query_text],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        return _format_query_results(result, self._threshold)

    def upsert_case(
        self,
        payload: Dict[str, Any],
        analysis: Optional[Dict[str, Any]] = None,
        solution: Optional[Dict[str, Any]] = None,
    ) -> None:
        if analysis is None and solution is None:
            return
        document = _build_document(
            log=payload.get("log"),
            status_code=payload.get("status_code"),
            exception=payload.get("exception"),
            artifact_type=payload.get("artifact_type"),
        )
        if not document:
            raise ValueError("log is required to store a case")

        case_id = _case_id(payload)
        metadata = _build_metadata(payload, analysis=analysis, solution=solution)
        if not metadata:
            raise ValueError("metadata is required to store a case")

        existing_meta = _get_existing_metadata(self._collection, case_id)
        if existing_meta:
            metadata = _merge_metadata(existing_meta, metadata)

        self._collection.upsert(
            ids=[case_id],
            documents=[document],
            metadatas=[metadata],
        )


def _get_existing_metadata(collection, case_id: str) -> Dict[str, Any]:
    try:
        result = collection.get(ids=[case_id], include=["metadatas"])
    except Exception:
        return {}
    metadatas = result.get("metadatas") or []
    return metadatas[0] if metadatas else {}


def _merge_metadata(existing: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(existing)
    merged.update({k: v for k, v in incoming.items() if v is not None})
    return merged


def _format_query_results(
    result: Dict[str, Any],
    threshold: Optional[float],
) -> List[SimilarCase]:
    items: List[SimilarCase] = []
    ids = (result.get("ids") or [[]])[0]
    docs = (result.get("documents") or [[]])[0]
    metadatas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]
    for idx, item_id in enumerate(ids):
        distance = distances[idx] if idx < len(distances) else None
        if threshold is not None and distance is not None and distance > threshold:
            continue
        items.append(
            SimilarCase(
                distance=distance,
                metadata=metadatas[idx] if idx < len(metadatas) else {},
                document=docs[idx] if idx < len(docs) else None,
            )
        )
    if items:
        logger.info("Similar cases found", extra={"count": len(items)})
    return items


@lru_cache(maxsize=1)
def get_error_log_store() -> ChromaErrorLogStore:
    logger.info("Initializing Chroma error log store")
    return ChromaErrorLogStore()
