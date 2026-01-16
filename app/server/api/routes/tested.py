from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.server.sap.tested.mpl import TestedMplClient, TestedMplDto

router = APIRouter()


class TestedResponse(BaseModel):
    tested_artifacts: List[TestedMplDto]


@router.get("/api/tested", response_model=TestedResponse)
async def tested(
    artifact_id: Optional[str] = None,
    log_start: Optional[datetime] = None,
    log_end: Optional[datetime] = None,
    status: str = "ALL",
    skip: int = 0,
    top: int = 20,
):
    if log_start is None:
        log_start = datetime.now() - timedelta(hours=2)
    if log_end is None:
        log_end = datetime.now()
    artifacts_ = TestedMplClient().get_tested_artifacts(
        artifact_id,
        log_start,
        log_end,
        status,
        skip,
        top,
    )
    return TestedResponse(tested_artifacts=artifacts_)
