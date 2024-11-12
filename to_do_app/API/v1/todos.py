from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Query
from fastapi import status

from to_do_app.API.utils.decorator_convert import convert_result
from to_do_app.dependencies.auth.dependencies import get_user_id
from to_do_app.domains.todos.flow import create_todo
from to_do_app.domains.todos.flow import delete_todo
from to_do_app.domains.todos.flow import get_todos
from to_do_app.domains.todos.flow import update_todo
from to_do_app.domains.todos.schemas import CreateTodo
from to_do_app.domains.todos.schemas import CreateTodoIn
from to_do_app.domains.todos.schemas import CreateTodoInDB
from to_do_app.domains.todos.schemas import DeleteTodoIn
from to_do_app.domains.todos.schemas import TaskStatus
from to_do_app.domains.todos.schemas import TodoList
from to_do_app.domains.todos.schemas import TodoModel
from to_do_app.domains.todos.schemas import UpdateTodoIn
from to_do_app.domains.todos.schemas import UpdateTODOModel

todos_router = APIRouter()


# TODO  response model should be equal with return type, and use just on of them
@todos_router.get("/todos", tags=["Todos"], response_model=list[TodoModel])
@convert_result
async def get_todos_route(
    user_id: Annotated[str, Depends(get_user_id)],
    task_status: Annotated[
        TaskStatus | None,
        Query(description="Task status to filter by (To Do, In Progress, Done)"),
    ] = None,
) -> list[TodoModel]:
    return await get_todos(context=TodoList(user_id=user_id, task_status=task_status))

@todos_router.post(
    "/todos",
    tags=["Todos"],
    response_description="Add new to do",
    response_model=CreateTodoInDB,
    status_code=status.HTTP_201_CREATED,
)
@convert_result
async def create_todo_route(
    todo: Annotated[CreateTodoIn, Body(...)],
    user_id: Annotated[str, Depends(get_user_id)],
) -> CreateTodoInDB:
    todo_with_user_id = CreateTodo(**todo.model_dump(), user_id=user_id)
    return await create_todo(context=todo_with_user_id)



@todos_router.put(
    "/todos/{todo_id}",
    tags=["Todos"],
    response_description="Update a to do",
    response_model=UpdateTODOModel,
    response_model_by_alias=False,
)
@convert_result
async def update_todo_route(
    todo_id: str,
    todo_update: Annotated[UpdateTodoIn, Body(...)],
    user_id: Annotated[str, Depends(get_user_id)],
) -> UpdateTodoIn:
    todo_id_and_user_id = todo_update.model_copy(
        update={"todo_id": todo_id, "user_id": user_id}
    )

    return await update_todo(context=todo_id_and_user_id)


@todos_router.delete(
    "/todos/{todo_id}",
    tags=["Todos"],
    response_model=DeleteTodoIn,
    response_description="Delete a to do",
)
@convert_result
async def delete_todo_route(
    todo_id: str, user_id: Annotated[str, Depends(get_user_id)]
) -> DeleteTodoIn:

    delete_todo_model = DeleteTodoIn(todo_id=todo_id, user_id=user_id, message="")
    return await delete_todo(context=delete_todo_model)
