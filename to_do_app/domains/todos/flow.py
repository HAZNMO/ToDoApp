from to_do_app.domains.todos.schemas import CreateTodoIn
from to_do_app.domains.todos.schemas import DeleteTodoModel
from to_do_app.domains.todos.schemas import TodoList
from to_do_app.domains.todos.schemas import UpdateTODOModel
from to_do_app.domains.todos.service import create_user_todo
from to_do_app.domains.todos.service import delete_user_todo
from to_do_app.domains.todos.service import get_user_todos
from to_do_app.domains.todos.service import update_user_todo


async def get_todos(context: TodoList) -> TodoList:
    return await get_user_todos(context)


async def create_todo(context: CreateTodoIn) -> CreateTodoIn:
    return await create_user_todo(context)


async def update_todo(context: UpdateTODOModel) -> UpdateTODOModel:
    return await update_user_todo(context)


async def delete_todo(context: DeleteTodoModel) -> DeleteTodoModel:
    return await delete_user_todo(context)
