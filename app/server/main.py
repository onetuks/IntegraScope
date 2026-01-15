from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.server import API_NAME, API_VERSION
from app.server.api.routes import error_log, meta, objects, tested
from app.server.exception.exception_handler import register_exception_handlers
from app.server.security.cors import allowed_headers, allowed_methods, \
    allowed_origins
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
    register_exception_handlers(_app)

    _app.include_router(meta.router)
    _app.include_router(error_log.router)
    _app.include_router(tested.router)
    _app.include_router(objects.router)

    @_app.on_event("startup")
    async def on_startup():
        logger.info("Starting API", extra={"version": API_VERSION})

    @_app.on_event("shutdown")
    async def on_shutdown():
        logger.info("Stopping API")

    return _app


app = create_app()
