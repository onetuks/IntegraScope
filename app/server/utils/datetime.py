from datetime import datetime, timezone, timedelta


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def ms_to_tz(ms: str, tz: timezone = timezone.utc) -> datetime:
    """
    ms: Unix timestamp in milliseconds
    tz: timezone string(e.g 'Asia/Seoul', 'UTC')
    """
    return datetime.fromtimestamp(int(ms) / 1000, tz=tz)


def to_gmt_0(date: str) -> str:
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    gmt_0 = dt - timedelta(hours=9)
    return gmt_0.strftime("%Y-%m-%dT%H:%M:%S")


def to_gmt_9(date: datetime) -> datetime:
    return date + timedelta(hours=9)
