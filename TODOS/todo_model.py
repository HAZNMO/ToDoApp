from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class TodoItem(BaseModel):
    id: ObjectId = None
    title: str
    description: str = None
    status: TaskStatus = TaskStatus.TO_DO
    user_id: str
    created_at: datetime = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
