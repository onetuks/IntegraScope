from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

from app.server import API_NAME, API_VERSION
from app.server.lang_graph.graph_runner import LangGraphClient, \
    get_langgraph_client
from app.server.security.cors import allowed_headers, allowed_methods, \
    allowed_origins
from app.server.sap.tested.mpl import TestedMplDto, TestedMplClient
from app.server.utils.logger import logger


def create_app() -> FastAPI:
    _app = FastAPI(title=API_NAME, version=API_VERSION)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins(),
        allow_credentials=True,
        allow_methods=allowed_methods(),
        allow_headers=allowed_headers(),
    )

    @_app.on_event("startup")
    async def on_startup():
        logger.info("Starting API", extra={"version": API_VERSION})

    @_app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Stopping API")

    return _app


app = create_app()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": API_VERSION,
    }


@app.get("/api/info")
async def api_info():
    return {
        "name": API_NAME,
        "version": API_VERSION,
        "docs_url": "/docs",
        "openapi_url": app.openapi_url,
        "status": "ok",
    }


class ErrorAnalysisRequest(BaseModel):
    message_guid: str = Field(..., description="message guid")


class AnalysisResponse(BaseModel):
    artifact_id: str
    artifact_type: str
    package_id: str
    message_guid: str
    log_start: str
    log_end: str
    log: str
    status_code: Optional[int]
    exception: str
    analysis: str
    solution: str


@app.post("/api/analysis", response_model=AnalysisResponse)
async def analysis(
        request: ErrorAnalysisRequest,
        graph_runner: LangGraphClient = Depends(get_langgraph_client)):
    state = graph_runner.run(message_guid=request.message_guid)
    return AnalysisResponse(
        artifact_id=state.get("artifact_id"),
        artifact_type=state.get("artifact_type"),
        package_id=state.get("package_id"),
        message_guid=state.get("message_guid"),
        log_start=state.get("log_start"),
        log_end=state.get("log_end"),
        log=state.get("log"),
        status_code=state.get("status_code"),
        exception=state.get("exception"),
        analysis=state.get("analysis"),
        solution=state.get("solution")
    )


class TestedResponse(BaseModel):
    tested_artifacts: List[TestedMplDto]


@app.get("/api/tested", response_model=TestedResponse)
async def tested(
        log_start: str = str(datetime.now() - timedelta(hours=2)),
        log_end: str = str(datetime.now())
):
    artifacts = TestedMplClient().get_tested_artifacts(log_start, log_end)
    return TestedResponse(tested_artifacts=artifacts)
