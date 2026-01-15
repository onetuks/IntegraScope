from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.server.lang_chain import AnalysisModel, SolutionsModel
from app.server.lang_graph.graph_runner import (
    ActionType,
    LangGraphClient,
    get_langgraph_client,
)
from app.server.utils.logger import logger
from app.server.vector_store import get_error_log_store

router = APIRouter()


class ErrorLogRequest(BaseModel):
    message_guid: str = Field(..., description="message guid")


class ErrorLogResponse(BaseModel):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: str
    log_end: str
    log: str
    origin_log: str
    status_code: Optional[int]
    exception: str


@router.post("/api/error-log", response_model=ErrorLogResponse)
async def error_log(
    request: ErrorLogRequest,
    graph_runner: LangGraphClient = Depends(get_langgraph_client),
):
    state = graph_runner.run(
        message_guid=request.message_guid,
        action_type=ActionType.ERROR_LOG,
    )
    return ErrorLogResponse(
        artifact_id=state.get("artifact_id"),
        artifact_type=state.get("artifact_type"),
        package_id=state.get("package_id"),
        message_guid=state.get("message_guid"),
        log_start=state.get("log_start"),
        log_end=state.get("log_end"),
        log=state.get("log"),
        origin_log=state.get("origin_log"),
        status_code=state.get("status_code"),
        exception=state.get("exception"),
    )


class ErrorAnalysisRequest(BaseModel):
    artifact_id: Optional[str] = None
    artifact_type: Optional[str] = None
    package_id: Optional[str] = None
    message_guid: Optional[str] = None
    log_start: Optional[str] = None
    log_end: Optional[str] = None
    log: str = Field(..., description="normalized log")
    origin_log: Optional[str] = None
    status_code: Optional[int] = None
    exception: Optional[str] = None


class ErrorAnalysisResponse(BaseModel):
    message_guid: str
    analysis: AnalysisModel


@router.post("/api/analysis", response_model=ErrorAnalysisResponse)
async def analysis(
    request: ErrorAnalysisRequest,
    graph_runner: LangGraphClient = Depends(get_langgraph_client),
):
    payload = _build_log_payload(request.model_dump())
    if not payload.get("log"):
        raise HTTPException(status_code=400, detail="log is required")

    cached = _find_similar_case(payload, "analysis")
    if cached:
        return ErrorAnalysisResponse(
            message_guid=request.message_guid or "-",
            analysis=cached,
        )

    state = graph_runner.run(
        message_guid=request.message_guid,
        action_type=ActionType.ANALYSIS,
        artifact_id=request.artifact_id,
        artifact_type=request.artifact_type,
        package_id=request.package_id,
        log_start=request.log_start,
        log_end=request.log_end,
        log=request.log,
        origin_log=request.origin_log,
        status_code=request.status_code,
        exception=request.exception,
    )
    analysis_result = state.get("analysis")
    _store_case(payload, analysis=analysis_result)
    return ErrorAnalysisResponse(
        message_guid=request.message_guid or "-",
        analysis=analysis_result,
    )


class ErrorSolutionRequest(BaseModel):
    artifact_id: Optional[str] = None
    artifact_type: Optional[str] = None
    package_id: Optional[str] = None
    message_guid: Optional[str] = None
    log_start: Optional[str] = None
    log_end: Optional[str] = None
    log: str = Field(..., description="normalized log")
    origin_log: Optional[str] = None
    status_code: Optional[int] = None
    exception: Optional[str] = None
    analysis: Optional[AnalysisModel] = None


class ErrorSolutionResponse(BaseModel):
    message_guid: str
    solution: SolutionsModel


@router.post("/api/solutions", response_model=ErrorSolutionResponse)
async def solution(
    request: ErrorSolutionRequest,
    graph_runner: LangGraphClient = Depends(get_langgraph_client),
):
    payload = _build_log_payload(request.model_dump())
    if not payload.get("log"):
        raise HTTPException(status_code=400, detail="log is required")

    cached = _find_similar_case(payload, "solution")
    if cached:
        return ErrorSolutionResponse(
            message_guid=request.message_guid or "-",
            solution=cached,
        )

    state = graph_runner.run(
        message_guid=request.message_guid,
        action_type=ActionType.SOLUTION,
        artifact_id=request.artifact_id,
        artifact_type=request.artifact_type,
        package_id=request.package_id,
        log_start=request.log_start,
        log_end=request.log_end,
        log=request.log,
        origin_log=request.origin_log,
        status_code=request.status_code,
        exception=request.exception,
        analysis=request.analysis,
    )
    solution_result = state.get("solution")
    analysis_payload = request.analysis.model_dump() if request.analysis else None
    _store_case(payload, analysis=analysis_payload, solution=solution_result)
    return ErrorSolutionResponse(
        message_guid=request.message_guid or "-",
        solution=solution_result,
    )


class ResolveWithAnalysisResponse(BaseModel):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: str
    log_end: str
    log: str
    origin_log: str
    status_code: Optional[int]
    exception: str
    analysis: AnalysisModel
    solution: SolutionsModel


@router.post("/api/resolve-with-analysis", response_model=ResolveWithAnalysisResponse)
async def resolve_with_analysis(
    request: ErrorLogRequest,
    graph_runner: LangGraphClient = Depends(get_langgraph_client),
):
    state = graph_runner.run(
        message_guid=request.message_guid,
        action_type=ActionType.RESOLVE_WITH_ANALYSIS,
    )
    return ResolveWithAnalysisResponse(
        artifact_id=state.get("artifact_id"),
        artifact_type=state.get("artifact_type"),
        package_id=state.get("package_id"),
        message_guid=state.get("message_guid"),
        log_start=state.get("log_start"),
        log_end=state.get("log_end"),
        log=state.get("log"),
        origin_log=state.get("origin_log"),
        status_code=state.get("status_code"),
        exception=state.get("exception"),
        analysis=state.get("analysis"),
        solution=state.get("solution"),
    )


def _build_log_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_id": data.get("artifact_id"),
        "artifact_type": data.get("artifact_type"),
        "package_id": data.get("package_id"),
        "message_guid": data.get("message_guid"),
        "log_start": data.get("log_start"),
        "log_end": data.get("log_end"),
        "log": data.get("log"),
        "status_code": data.get("status_code"),
        "exception": data.get("exception"),
    }


def _find_similar_case(payload: Dict[str, Any], field: str) -> Optional[Dict[str, Any]]:
    try:
        store = get_error_log_store()
    except Exception as exc:
        logger.info("Vector store unavailable", extra={"error": str(exc)})
        return None

    try:
        cases = store.find_similar(payload)
    except Exception as exc:
        logger.warning(
            "Vector search failed",
            extra={"error": str(exc)},
        )
        return None

    for case in cases:
        result = getattr(case, field, None)
        if result:
            return result
    return None


def _store_case(
    payload: Dict[str, Any],
    analysis: Optional[Dict[str, Any]] = None,
    solution: Optional[Dict[str, Any]] = None,
) -> None:
    try:
        store = get_error_log_store()
        store.upsert_case(payload, analysis=analysis, solution=solution)
    except Exception as exc:
        logger.warning(
            "Failed to store case in vector store",
            extra={"error": str(exc)},
        )
