from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from to_do_app.API.utils.datetime import utcnow
from to_do_app.API.utils.token_expire import token_expire


class TokenModel(BaseModel):
    user_id: str
    email: str
    exp: datetime = Field(default_factory=token_expire)
    timestamp: str = Field(default_factory=utcnow().isoformat)
