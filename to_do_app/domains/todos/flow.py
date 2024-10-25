from to_do_app.domains.todos.schemas import TodoList, DeleteTodoModel
from to_do_app.domains.todos.service import (
    get_user_todos,
    create_user_todo,
    update_user_todo,
    delete_user_todo,
)
from to_do_app.domains.todos.schemas import UpdateTODOModel, CreateTodoModel


async def get_todos(context: TodoList):
    return await get_user_todos(context)


async def create_todo(context: CreateTodoModel):
    return await create_user_todo(context)


async def update_todo(context: UpdateTODOModel):
    return await update_user_todo(context)


async def delete_todo(context: DeleteTodoModel):
    return await delete_user_todo(context)
