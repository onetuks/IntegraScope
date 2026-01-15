from fastapi import APIRouter, Request

from app.server import API_NAME, API_VERSION

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "version": API_VERSION,
    }


@router.get("/api/info")
async def api_info(request: Request):
    return {
        "name": API_NAME,
        "version": API_VERSION,
        "docs_url": request.app.docs_url,
        "openapi_url": request.app.openapi_url,
        "status": "ok",
    }
