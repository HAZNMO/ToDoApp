from pydantic import BaseModel, Field, constr
from bson import ObjectId
from datetime import datetime, timezone
from enum import Enum


def current_time_factory():
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId')
        return str(value)


class TodoModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: constr(min_length=1)
    description: str = None
    status: TaskStatus = TaskStatus.TO_DO
    user_id: str
    created_at: datetime = Field(default_factory=current_time_factory)
