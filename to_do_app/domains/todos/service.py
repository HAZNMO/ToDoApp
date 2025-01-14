from bson import ObjectId
from fastapi import HTTPException
from pymongo import ReturnDocument

from to_do_app.API.utils.datetime import utcnow
from to_do_app.API.utils.decorator_convert import convert_result
from to_do_app.domains.todos.schemas import CreateTodoInDB
from to_do_app.domains.todos.schemas import DeleteTodoIn
from to_do_app.domains.todos.schemas import TodoList
from to_do_app.domains.todos.schemas import TodoModel
from to_do_app.domains.todos.schemas import UpdateTodoIn
from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import todo_collection


@convert_result
async def get_user_todos(context: TodoList) -> list[TodoModel]:
    _filter = {}

    if context.user_id is not None:
        _filter["user_id"] = context.user_id
    if context.task_status is not None:
        _filter["status"] = context.task_status

    todos = await todo_collection.find(_filter).to_list(None)
    return todos

@convert_result
async def create_user_todo(create_todos: CreateTodoInDB) -> CreateTodoInDB:
    new_todo_data = create_todos.model_dump(by_alias=True ,exclude_unset=True)
    new_todo_data["user_id"] = create_todos.user_id
    new_todo_data["created_at"] = utcnow()
    new_todo = await todo_collection.insert_one(new_todo_data)
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return CreateTodoInDB(**created_todo)


@convert_result
async def update_user_todo(update_todos: UpdateTodoIn) -> UpdateTodoIn:
    existing_todo = await todo_collection.find_one({"_id": ObjectId(update_todos.todo_id)})

    if existing_todo is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if str(existing_todo["user_id"]) != str(update_todos.user_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this todo"
        )

    update_data = {
        k: v for k, v in update_todos.model_dump(by_alias=True).items() if v is not None
    }
    update_data["updated_at"] = utcnow()

    update_result = await todo_collection.find_one_and_update(
        {"_id": ObjectId(update_todos.todo_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )

    if update_result is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found or you do not have access to this todo",
        )

    return update_result


@convert_result
async def delete_user_todo(delete_todos: DeleteTodoIn) -> DeleteTodoIn:
    existing_todo = await todo_collection.find_one({"_id": ObjectId(delete_todos.todo_id)})

    if existing_todo is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if str(existing_todo["user_id"]) != str(delete_todos.user_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this todo"
        )

    await todo_collection.delete_one({"_id": ObjectId(delete_todos.todo_id)})

    return DeleteTodoIn(
        todo_id=delete_todos.todo_id,
        user_id=delete_todos.user_id,
        message=f"Task of user {delete_todos.user_id} "
        f"with ID {delete_todos.todo_id} was successfully deleted.",
    )

