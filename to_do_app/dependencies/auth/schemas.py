from datetime import datetime

from pydantic import Field

from to_do_app.API.utils.datetime import utcnow
from to_do_app.API.utils.token_expire import token_expire
from to_do_app.domains.users.schemas import UserBase


class TokenModel(UserBase):
    user_id: str
    email: str
    exp: datetime = Field(default_factory=token_expire)
    timestamp: str = Field(default_factory=utcnow().isoformat)
