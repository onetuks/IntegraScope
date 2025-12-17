from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

from app.server import API_NAME, API_VERSION, _success_response
from app.server.security.cors import allowed_headers, allowed_methods, allowed_origins
from app.server.services.log.error_log import ErrorLogService
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
async def health(request: Request):
    return _success_response(
        request,
        {
            "status": "ok",
            "version": API_VERSION,
        },
    )


@app.get("/api/info")
async def api_info(request: Request):
    return _success_response(
        request,
        {
            "name": API_NAME,
            "version": API_VERSION,
            "docs_url": app.docs_url,
            "openapi_url": app.openapi_url,
            "status": "ok",
        },
    )


class ErrorAnalysisRequest(BaseModel):
    artifact_id: str = Field(..., description="artifact name")


@app.post("/api/analysis")
async def analysis(request: ErrorAnalysisRequest):
    error_data = ErrorLogService().request_error_data(request.artifact_id)
    return _success_response(request, error_data)
