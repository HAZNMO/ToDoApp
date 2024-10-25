from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import todo_collection
from to_do_app.domains.todos.schemas import (
    UpdateTODOModel,
    current_time_factory,
    CreateTodoModel,
    TodoList,
    DeleteTodoModel,
)
from pymongo import ReturnDocument
from fastapi import HTTPException
from bson import ObjectId


async def get_user_todos(user_todos: TodoList):
    query = {"user_id": user_todos.user_id}

    if user_todos.task_status is None:
        task_status = await todo_collection.find(
            {"user_id": user_todos.user_id}
        ).to_list(1000)
        return task_status

    elif user_todos.task_status:
        query["status"] = user_todos.task_status

    todos = await todo_collection.find(query).to_list(1000)
    return todos


async def create_user_todo(create_todos: CreateTodoModel):
    new_todo_data = create_todos.model_dump(by_alias=True, exclude_unset=True)
    new_todo_data["user_id"] = create_todos.user_id
    new_todo_data["created_at"] = current_time_factory()

    new_todo = await todo_collection.insert_one(new_todo_data)

    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return created_todo


async def update_user_todo(update_todos: UpdateTODOModel):
    update_data = {
        k: v for k, v in update_todos.model_dump(by_alias=True).items() if v is not None
    }
    update_data["updated_at"] = current_time_factory()

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


async def delete_user_todo(delete_todos: DeleteTodoModel):
    delete_result = await todo_collection.delete_one(
        {"_id": ObjectId(delete_todos.todo_id), "user_id": delete_todos.user_id}
    )

    if delete_result.deleted_count == 1:
        return {
            "message": f"Task with ID {delete_todos.todo_id} was successfully deleted."
        }

    raise HTTPException(status_code=404, detail="Task not found or access denied")
