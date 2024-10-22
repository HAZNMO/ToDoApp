from typing import Optional
from fastapi import APIRouter
from fastapi import Depends, Body, status, Query
from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.domains.to_dos.flow import get_user_todos
from to_do_app.domains.to_dos.service import create_todo, update_todo, delete_todo
from to_do_app.domains.to_dos.schemas import TodoModel, UpdateTODOModel, TaskStatus, CreateTodoModel

to_dos_router = APIRouter(prefix="/todos")
@to_dos_router.get("/get_todos", response_model=list[TodoModel])
async def get_todos_route(
    task_status: Optional[TaskStatus] = Query(None, description="Task status to filter by (To Do, In Progress, Done)"),
    user_info: dict = Depends(decode_token)):
    return await get_user_todos(user_info=user_info, task_status=task_status)

@to_dos_router.post("/create_todos",
          response_description="Add new to do",
          response_model=CreateTodoModel,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False)
async def create_todo_route(todo: CreateTodoModel = Body(...), user_info: dict = Depends(decode_token)):
    return await create_todo(todo, user_info)

@to_dos_router.put("/todos/{todo_id}",
         response_description="Update a to do",
         response_model=UpdateTODOModel,
         response_model_by_alias=False)
async def update_todo_route(todo_id: str, todo_update: UpdateTODOModel = Body(...), user_info: dict = Depends(decode_token)):
    return await update_todo(todo_id,todo_update,user_info)

@to_dos_router.delete("/todos/{todo_id}", response_description="Delete a to do")
async def delete_todo_route(todo_id: str, user_info: dict = Depends(decode_token)):
    return await delete_todo(todo_id,user_info)