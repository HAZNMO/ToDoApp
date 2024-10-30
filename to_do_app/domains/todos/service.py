from bson import ObjectId
from fastapi import HTTPException
from pymongo import ReturnDocument

from to_do_app.API.utils.datetime import utcnow
from to_do_app.domains.todos.schemas import CreateTodoIn
from to_do_app.domains.todos.schemas import DeleteTodoModel
from to_do_app.domains.todos.schemas import TodoList
from to_do_app.domains.todos.schemas import UpdateTODOModel
from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import todo_collection


async def get_user_todos(context: TodoList) -> TodoList:
    _filter = {}

    if context.user_id is not None:
        _filter["user_id"] = context.user_id
    if context.task_status is not None:
        _filter["status"] = context.task_status

    todos = await todo_collection.find(_filter).to_list(None)
    return todos


async def create_user_todo(create_todos: CreateTodoIn) -> CreateTodoIn:
    new_todo_data = create_todos.model_dump(by_alias=True, exclude_unset=True)
    new_todo_data["user_id"] = create_todos.user_id
    new_todo_data["created_at"] = utcnow()

    new_todo = await todo_collection.insert_one(new_todo_data)

    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return created_todo


async def update_user_todo(update_todos: UpdateTODOModel) -> UpdateTODOModel:
    update_data = {
        k: v for k, v in update_todos.model_dump(by_alias=True).items() if v is not None
    }
    update_data["updated_at"] = utcnow()

    update_result = await todo_collection.find_one_and_update(
        {"_id": ObjectId(update_todos.todo_id), "user_id": update_todos.user_id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )

    if update_result is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found or you do not have access to this todo",
        )

    return update_result


async def delete_user_todo(delete_todos: DeleteTodoModel) -> DeleteTodoModel:
    delete_result = await todo_collection.delete_one(
        {"_id": ObjectId(delete_todos.todo_id), "user_id": delete_todos.user_id}
    )

    if delete_result.deleted_count == 1:
        return DeleteTodoModel(
            todo_id=delete_todos.todo_id,
            user_id=delete_todos.user_id,
            message=f"Task of user {delete_todos.user_id} "
            f"with ID {delete_todos.todo_id} was successfully deleted.",
        )

    raise HTTPException(status_code=404, detail="Task not found or access denied")
