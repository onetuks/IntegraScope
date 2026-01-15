from fastapi import APIRouter

from app.server.sap.object.object_search import ObjectSearch

router = APIRouter()


@router.get("/api/packages")
async def packages():
    packages_ = ObjectSearch().get_package_list()
    return packages_


@router.get("/api/artifacts")
async def artifacts(package_id: str):
    return ObjectSearch().get_artifact_list(package_id)
