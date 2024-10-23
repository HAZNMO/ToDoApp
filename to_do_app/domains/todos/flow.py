from fastapi import Depends, Body

from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.domains.todos.schemas import TaskStatus, TodoList, TodoModel
from to_do_app.domains.todos.service import get_user_todos, create_user_todo, update_user_todo, delete_user_todo
from to_do_app.domains.todos.schemas import UpdateTODOModel, CreateTodoModel
from typing import Optional

# class TodoList(BaseModel):
#     user_id: str
#     task_status: TaskStatus | None = None

#mutat un service aici o chem
async def get_todos(context: TodoList):
    return await get_user_todos(context)

async def create_todo(context: CreateTodoModel):
    return await create_user_todo(context)

async def update_todo(context: UpdateTODOModel):
    return await update_user_todo(context)

async def delete_todo(todo_id: str, user_info: dict = Depends(decode_token)):
    return await delete_user_todo(todo_id, user_info)