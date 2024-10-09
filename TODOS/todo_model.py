from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Todo(BaseModel):
    id: Optional[str]
    title: str
    description: str
    completed: bool = False
    created_at: Optional[datetime]
    completed_at: Optional[datetime] = None
