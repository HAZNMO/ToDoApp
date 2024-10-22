from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import todo_collection
from to_do_app.domains.todos.schemas import UpdateTODOModel, current_time_factory, CreateTodoModel
from pymongo import ReturnDocument
from fastapi import HTTPException, Depends, Body, Query
from bson import ObjectId
from typing import Optional
from to_do_app.domains.todos.schemas import TaskStatus

async def get_user_todos(
        user_info: dict = Depends(decode_token),
        task_status: Optional[TaskStatus] = Query(None, description="Task status to filter by (To Do, In Progress, Done)")):
    user_id = user_info.get("_id")
    query = {"user_id": user_id}

    if task_status is None:
        task_status = await todo_collection.find({"user_id": user_id}).to_list(1000)
        return task_status

    elif task_status:
        query["status"] = task_status

    todos = await todo_collection.find(query).to_list(1000)
    return todos

async def create_todo(todo: CreateTodoModel = Body(...), user_info: dict = Depends(decode_token)):
    todo.user_id = user_info.get("_id")

    new_todo_data = todo.model_dump(by_alias=True, exclude_unset=True)
    new_todo_data['created_at'] = current_time_factory()
    new_todo = await todo_collection.insert_one(new_todo_data)

    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return created_todo

async def update_todo(todo_id: str, todo_update: UpdateTODOModel = Body(...), user_info: dict = Depends(decode_token)):
    update_data = {k: v for k, v in todo_update.model_dump(by_alias=True).items() if v is not None}
    update_data["updated_at"] = current_time_factory()
    update_data["user_id"] = user_info.get("_id")
    update_result = await todo_collection.find_one_and_update(
        {"_id": ObjectId(todo_id), "user_id": user_info.get("_id")},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )

    if update_result is None:
        raise HTTPException(status_code=404, detail="Task not found or you do not have access to this todo")

    return update_result

async def delete_todo(todo_id: str, user_info: dict = Depends(decode_token)):
    user_id = user_info.get("_id")
    delete_result = await todo_collection.delete_one({"_id": ObjectId(todo_id), "user_id": user_id})

    if delete_result.deleted_count == 1:
        return {"message": f"Task with ID {todo_id} was successfully deleted."}

    raise HTTPException(status_code=404, detail="Task not found or access denied")