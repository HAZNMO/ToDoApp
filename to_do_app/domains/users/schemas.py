from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from to_do_app.API.utils.datetime import utcnow


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    token: str


class UserBase(BaseModel):
    user_id: str
    email: str

class UserWithDetails(UserCreate):
    created_at: datetime = Field(default_factory=utcnow)
    password: str
