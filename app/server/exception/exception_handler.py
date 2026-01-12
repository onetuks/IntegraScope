from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.server.utils.logger import logger


def _error_response(request: Request, detail, status_code: int):
    request_id = getattr(request.state, "request_id", None)
    body = {"detail": detail}
    if request_id:
        body["request_id"] = request_id
    return JSONResponse(status_code=status_code, content=body)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            "HTTP error",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "path": request.url.path,
            },
        )
        return _error_response(request, exc.detail, exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request,
                                           exc: RequestValidationError):
        logger.warning(
            "Validation error",
            extra={
                "errors": exc.errors(),
                "path": request.url.path,
            },
        )
        return _error_response(request, exc.errors(), 422)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(
            "Unhandled error",
            extra={"path": request.url.path},
        )
        return _error_response(request, "Internal server error", 500)
