from bson import ObjectId
from datetime import datetime
from todo_schema import TodoItemCreate, TodoItemUpdate
from mongodb_connect.mongo_connection import todo_collection

async def get_todos(skip: int = 0, limit: int = 100):
    todos_cursor = todo_collection.find().skip(skip).limit(limit)
    todos = await todos_cursor.to_list(length=limit)
    return todos

async def get_todo(todo_id: str):
    todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    return todo

async def create_todo_item(todo: TodoItemCreate):
    todo_dict = todo.dict()
    todo_dict["completed"] = False
    todo_dict["created_at"] = datetime.utcnow()
    result = await todo_collection.insert_one(todo_dict)
    return await get_todo(result.inserted_id)

async def update_todo_item(todo_id: str, todo: TodoItemUpdate):
    update_data = {k: v for k, v in todo.dict().items() if v is not None}
    if update_data.get("completed", False):
        update_data["completed_at"] = datetime.utcnow()
    else:
        update_data["completed_at"] = None
    await todo_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": update_data})
    return await get_todo(todo_id)

async def delete_todo_item(todo_id: str):
    result = await todo_collection.delete_one({"_id": ObjectId(todo_id)})
    return result.deleted_count
