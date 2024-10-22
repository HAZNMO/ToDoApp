from fastapi import Depends, Query
from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.domains.todos.schemas import TaskStatus
from to_do_app.domains.todos.service import get_user_todos
from typing import Optional


#mutat un service aici o chem
async def get_todos(
        user_info: dict = Depends(decode_token),
        task_status: Optional[TaskStatus] = Query(None, description="Task status to filter by (To Do, In Progress, Done)")):
    return await get_user_todos(user_info,task_status)