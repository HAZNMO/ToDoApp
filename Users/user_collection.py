from mongodb_connect.mongo_connection import todo_collection, user_collection
from bson import ObjectId
from TODOS.todo_model import TodoModel
from typing import List
from pydantic import BaseModel

async def create_user(user_data):
    result = await user_collection.insert_one(user_data)
    return result.inserted_id

async def get_user_todos(user_id, skip=0, limit=100):
    todos_cursor = todo_collection.find({"user_id": ObjectId(user_id)}).skip(skip).limit(limit)
    todos = await todos_cursor.to_list(length=limit)
    return todos

class user_todos(BaseModel):
    todos: List[TodoModel]
