from bson import ObjectId
from TODOS.todo_model import TodoModel
from mongodb_connect.mongo_connection import todo_collection


async def get_todos(skip: int = 0, limit: int = 100):
    todos_cursor = todo_collection.find().skip(skip).limit(limit)
    todos = await todos_cursor.to_list(length=limit)
    return todos

async def get_todos(todo_id: str):
    todo = await todo_collection.find_all({"_id": ObjectId(todo_id)})
    return todo

async def get_todo(todo_id: str):
    todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    return todo

async def get_todo_item(todo_id: str):
    todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    return todo


async def save_todo_item(user_id: str, todo: TodoModel):
    todo_dict = todo.model_dump()
    todo_dict["user_id"] = user_id
    result = await todo_collection.insert_one(todo_dict)
    return await get_todo_item(str(result.inserted_id))


async def update_todo_item(todo_id: str, user_id: str, todo: TodoModel):
    update_data = {k: v for k, v in todo.model_dump().items() if v is not None}
    await todo_collection.update_one({"_id": ObjectId(todo_id), "user_id": ObjectId(user_id)}, {"$set": update_data})
    return await get_todo_item(todo_id)


async def delete_todo_item(todo_id: str):
    result = await todo_collection.delete_one({"_id": ObjectId(todo_id)})
    return result.deleted_count
