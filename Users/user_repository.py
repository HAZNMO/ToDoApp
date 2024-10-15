from mongodb_connect.mongo_connection import user_collection
from TODOS.todo_model import TodoModel
from bson import ObjectId

from datetime import datetime, timezone

def utcnow():
    return datetime.now(tz=timezone.utc)

async def get_user_todos(user_id: str, skip: int = 0, limit: int = 100):
    todos_cursor = await user_collection.find({"user_id": user_id}).skip(skip).limit(limit).to_list(length=limit)
    return todos_cursor

async def create_todo_item(user_id: str, todo: TodoModel):
    todo_dict = todo.model_dump()
    todo_dict["user_id"] = user_id
    todo_dict["created_at"] = utcnow().isoformat()
    result = await user_collection.insert_one(todo_dict)
    return await get_todo_item(str(result.inserted_id))

async def get_todo_item(todo_id: str):
    todo = await user_collection.find_one({"_id": ObjectId(todo_id)})
    return todo

async def update_todo_item(todo_id: str, user_id: str, todo: TodoModel):
    update_data = {k: v for k, v in todo.model_dump().items() if v is not None}
    await user_collection.update_one({"_id": ObjectId(todo_id), "user_id": user_id}, {"$set": update_data})
    return await get_todo_item(todo_id)

async def delete_todo_item(todo_id: str, user_id: str):
    result = await user_collection.delete_one({"_id": ObjectId(todo_id), "user_id": user_id})
    return result.deleted_count