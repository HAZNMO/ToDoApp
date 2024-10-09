from pydantic import BaseModel
from typing import Optional

class TodoItemCreate(BaseModel):
    title: str
    description: str

class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
