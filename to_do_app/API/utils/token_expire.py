from datetime import datetime
from datetime import timedelta

from to_do_app.API.utils.datetime import utcnow


def token_expire() -> datetime:
    token_expire_minutes = 30
    expiration = utcnow() + timedelta(minutes=token_expire_minutes)
    return expiration
