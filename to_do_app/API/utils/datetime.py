from datetime import UTC
from datetime import datetime

utc = UTC


def utcnow() -> datetime:
    return datetime.now(tz=utc)
