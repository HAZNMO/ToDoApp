from typing import Optional
from fastapi import APIRouter
from fastapi import Depends, Body, status, Query
from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.domains.todos.flow import create_todo, update_todo, delete_todo, get_todos
from to_do_app.domains.todos.schemas import TodoModel, UpdateTODOModel, TaskStatus, CreateTodoModel, TodoList, \
    DeleteTodoModel

todos_router = APIRouter()
@todos_router.get("/todos", response_model=list[TodoModel])
async def get_todos_route(
    task_status: Optional[TaskStatus] = Query(None, description="Task status to filter by (To Do, In Progress, Done)"),
    user_info: dict = Depends(decode_token)):
    user_id = user_info.get("_id")
    return await get_todos(context=TodoList(task_status=task_status, user_id=user_id))

@todos_router.post("/todos",
          response_description="Add new to do",
          response_model=CreateTodoModel,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False)
async def create_todo_route(todo: CreateTodoModel = Body(...), user_info: dict = Depends(decode_token)):
    user_id = user_info.get("_id")
    todo_with_user_id = todo.model_copy(update={"user_id": user_id})
    return await create_todo(context=todo_with_user_id)


@todos_router.put("/todos/{todo_id}",
         response_description="Update a to do",
         response_model=UpdateTODOModel,
         response_model_by_alias=False)
async def update_todo_route(todo_id: str, todo_update: UpdateTODOModel = Body(...), user_info: dict = Depends(decode_token)):
    user_id = user_info.get("_id")
    todo_id_and_user_id = todo_update.model_copy(update={"todo_id": todo_id, "user_id": user_id})
    return await update_todo(context=todo_id_and_user_id)

@todos_router.delete("/todos/{todo_id}", response_description="Delete a to do")
async def delete_todo_route(todo_id: str, user_info: dict = Depends(decode_token)):
    user_id = user_info.get("_id")
    delete_todo_model = DeleteTodoModel(todo_id=todo_id, user_id=user_id)
    return await delete_todo(context=delete_todo_model)