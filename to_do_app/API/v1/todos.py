from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Query
from fastapi import status

from to_do_app.dependencies.auth.dependencies import decode_token
from to_do_app.dependencies.auth.dependencies import get_user_id
from to_do_app.domains.todos.flow import create_todo
from to_do_app.domains.todos.flow import delete_todo
from to_do_app.domains.todos.flow import get_todos
from to_do_app.domains.todos.flow import update_todo
from to_do_app.domains.todos.schemas import CreateTodoIn
from to_do_app.domains.todos.schemas import CreateTodoModel
from to_do_app.domains.todos.schemas import DeleteTodoModel
from to_do_app.domains.todos.schemas import TaskStatus
from to_do_app.domains.todos.schemas import TodoList
from to_do_app.domains.todos.schemas import TodoModel
from to_do_app.domains.todos.schemas import UpdateTODOModel

todos_router = APIRouter()


# TODO  response model should be equal with return type, and use just on of them
@todos_router.get("/todos", response_model=list[TodoModel])
async def get_todos_route(
    user_info: Annotated[dict, Depends(decode_token)],  # TODO use user_id dependency
    task_status: Annotated[
        TaskStatus | None,
        Query(description="Task status to filter by (To Do, In Progress, Done)"),
    ] = None,
) -> TodoList:
    user_id = user_info.get("user_id")

    return await get_todos(context=TodoList(user_id=user_id, task_status=task_status))


@todos_router.post(
    "/todos",
    response_description="Add new to do",
    response_model=CreateTodoModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_todo_route(
    user_info: Annotated[dict, Depends(decode_token)],
    todo: Annotated[CreateTodoIn, Body(...)],
) -> CreateTodoModel:

    # TODO adjust using partial model with small args, then pass to flow with user id then pass to service with full object to be saved
    user_id = user_info.get("user_id")
    todo_with_user_id = todo.model_copy(update={"user_id": user_id})
    return await create_todo(context=todo_with_user_id)


@todos_router.put(
    "/todos/{todo_id}",
    response_description="Update a to do",
    response_model=UpdateTODOModel,
    response_model_by_alias=False,
)
async def update_todo_route(
    todo_id: str,
    user_info: Annotated[dict, Depends(decode_token)],
    todo_update: Annotated[UpdateTODOModel, Body(...)],
) -> UpdateTODOModel:
    user_id = user_info.get("user_id")
    todo_id_and_user_id = todo_update.model_copy(
        update={"todo_id": todo_id, "user_id": user_id}
    )

    # TODO verify is the same user that was the author of todo is allowed to change
    return await update_todo(context=todo_id_and_user_id)


@todos_router.delete(
    "/todos/{todo_id}",
    response_model=DeleteTodoModel,
    response_description="Delete a to do",
)
async def delete_todo_route(
    todo_id: str, user_id: Annotated[str, Depends(get_user_id)]
) -> DeleteTodoModel:

    delete_todo_model = DeleteTodoModel(todo_id=todo_id, user_id=user_id, message="")
    return await delete_todo(context=delete_todo_model)
