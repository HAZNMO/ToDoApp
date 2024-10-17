from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from datetime import datetime
from enum import Enum
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator


def current_time_factory() -> datetime:
    return datetime.now()


class TaskStatus(str, Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

PyObjectId = Annotated[str, BeforeValidator(str)]

class TodoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=current_time_factory)
    user_email: Optional[str] = Field(None)
    title: str = Field(...)
    description: str = Field(...)
    status: TaskStatus = Field(default=TaskStatus.TO_DO)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.strftime('%Y-%m-%d/%H:%M:%S')
        },
        json_schema_extra={
            "example": {
                "title": "Walk the dog",
                "description": "Walk the dog after coming back from school",
                "status": "To Do",
            }
        }
    )

class UpdateTODOModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: Optional[str] = Field(...)
    description: Optional[str] = Field(...)
    status: Optional[TaskStatus] = TaskStatus.TO_DO
    #created_at: datetime = Field(default_factory=current_time_factory)
    updated_at: datetime = Field(default_factory=current_time_factory)
    model_config = ConfigDict(
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.strftime('%Y-%m-%d/%H:%M:%S')},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Walk the dog (Optional)",
                "description": "Walk the dog after come back from school (Optional)"
            }
        },
    )