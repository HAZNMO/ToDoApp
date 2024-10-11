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

# class PydanticObjectId(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, value):
#         if not ObjectId.is_valid(value):
#             raise ValueError('Invalid ObjectId')
#         return str(value)


class TodoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    description: str = Field(...)
    created_at: datetime = Field(default_factory=current_time_factory)
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
            }
        }
    )

class UpdateTODOModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: Optional[str] = Field(...)
    description: Optional[str] = Field(...)
    #created_at: datetime = Field(default_factory=current_time_factory)
    status: Optional[TaskStatus] = TaskStatus.TO_DO.value
    updated_at: datetime = Field(default_factory=current_time_factory)
    model_config = ConfigDict(
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.strftime('%Y-%m-%d/%H:%M:%S')},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Walk the dog (Optional)",
                "description": "Walk the dog after come back from school (Optional)",
                "status": TaskStatus.TO_DO.value
            }
        },
    )