from datetime import datetime, timezone


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def ms_to_tz(ms: str, tz: timezone = timezone.utc) -> datetime:
    """
    ms: Unix timestamp in milliseconds
    tz: timezone string(e.g 'Asia/Seoul', 'UTC')
    """
    return datetime.fromtimestamp(int(ms) / 1000, tz=tz)
