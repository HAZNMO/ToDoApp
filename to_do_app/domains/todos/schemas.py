from datetime import datetime
from enum import StrEnum
from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic.functional_validators import BeforeValidator

from to_do_app.core.config import utcnow


class TaskStatus(StrEnum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


PyObjectId = Annotated[str, BeforeValidator(str)]


class TodoList(BaseModel):
    user_id: str
    task_status: TaskStatus | None = None


class DeleteTodoModel(BaseModel):
    todo_id: str
    user_id: str
    message: str


class TodoModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    created_at: datetime = Field(None, alias="created_at")
    updated_at: datetime = Field(None, alias="updated_at")
    user_id: PyObjectId | None = Field(default=None)
    title: str = Field(...)
    description: str = Field(...)
    status: TaskStatus = Field(default=TaskStatus.TO_DO)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: (
                v.strftime("%Y-%m-%d/%H:%M:%S") if v is not None else None
            )
        },
        json_schema_extra={
            "example": {
                "_id": str(ObjectId()),
                "title": "Walk the dog",
                "description": "Walk the dog after coming back from school",
                "status": "To Do",
            }
        },
    )


class CreateTodoModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=utcnow)
    user_id: PyObjectId | None = Field(default=None)
    title: str = Field(...)
    description: str = Field(...)
    status: TaskStatus = Field(default=TaskStatus.TO_DO)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d/%H:%M:%S")},
        json_schema_extra={
            "example": {
                "title": "Walk the dog",
                "description": "Walk the dog after coming back from school",
                "status": "To Do",
            }
        },
    )


class UpdateTODOModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    user_id: PyObjectId | None = Field(default=None)
    title: str | None = Field(...)
    description: str | None = Field(...)
    status: TaskStatus | None = Field(default=TaskStatus.TO_DO)
    updated_at: datetime = Field(default_factory=utcnow)

    model_config = ConfigDict(
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.strftime("%Y-%m-%d/%H:%M:%S"),
        },
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Walk the dog (Optional)",
                "description": "Walk the dog after coming back from school (Optional)",
            }
        },
    )
