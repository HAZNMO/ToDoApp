from fastapi import Depends, Query, Body
from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.domains.todos.schemas import TaskStatus
from to_do_app.domains.todos.service import get_user_todos, create_user_todo, update_user_todo, delete_user_todo
from to_do_app.domains.todos.schemas import UpdateTODOModel, CreateTodoModel
from typing import Optional


#mutat un service aici o chem
async def get_todos(
        user_info: dict = Depends(decode_token),
        task_status: Optional[TaskStatus] = Query(None, description="Task status to filter by (To Do, In Progress, Done)")):
    return await get_user_todos(user_info,task_status)

async def create_todo(todo: CreateTodoModel = Body(...), user_info: dict = Depends(decode_token)):
    return await create_user_todo(todo,user_info)

async def update_todo(todo_id: str, todo_update: UpdateTODOModel = Body(...), user_info: dict = Depends(decode_token)):
    return await update_user_todo(todo_id, todo_update, user_info)

async def delete_todo(todo_id: str, user_info: dict = Depends(decode_token)):
    return await delete_user_todo(todo_id, user_info)