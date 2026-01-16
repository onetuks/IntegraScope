from datetime import datetime
from typing import Tuple, Optional, List, Dict, Any

from app.client.api.api_client import get
from app.client.components.fetch_option import TestStatus


def fetch_tested(
        log_start: datetime,
        log_end: datetime,
        status: TestStatus,
        artifact_id: Optional[str] = None,
        skip: int = 0,
        top: int = 20
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        params: Dict[str, Any] = {
            "status": status,
            "log_start": log_start.isoformat(),
            "log_end": log_end.isoformat(),
            "skip": skip,
            "top": top,
        }
        if artifact_id:
            params["artifact_id"] = artifact_id
        response = get("/api/tested", params=params)
        data = response.json()
        return data.get("tested_artifacts", []), None
    except Exception as exc:
        return None, str(exc)
