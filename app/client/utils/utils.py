from datetime import datetime, timedelta
from typing import Optional, Tuple


def parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def format_duration(start: Optional[str], end: Optional[str]) -> str:
    start_dt, end_dt = parse_dt(start), parse_dt(end)
    if not start_dt or not end_dt:
        return "-"
    delta = end_dt - start_dt
    seconds = delta.total_seconds()
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, remainder = divmod(int(seconds), 60)
    return f"{minutes}m {remainder}s"
