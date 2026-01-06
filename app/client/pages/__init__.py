from datetime import datetime
from typing import Tuple, Optional, List, Dict, Any

from app.client.api.api_client import get
from app.client.components.fetch_option import TestStatus


def fetch_tested(
        log_start: datetime,
        log_end: datetime,
        status: TestStatus,
        artifact_id: Optional[str] = None
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        response = get(f"/api/tested" +
                       f"?status={status}" +
                       (f"&artifact_id={artifact_id}" if artifact_id else "") +
                       f"&log_start={log_start.isoformat()}" +
                       f"&log_end={log_end.isoformat()}")
        data = response.json()
        return data.get("tested_artifacts", []), None
    except Exception as exc:
        return None, str(exc)
