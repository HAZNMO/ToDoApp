from mongodb_connect.mongo_connection import user_collection
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime
import jwt
import os
from fastapi import HTTPException
import secrets
from TODOS.todo_model import TodoItem
from bson import ObjectId


load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(16))
JWT_ALGORITHM = "HS256"

# Настройка bcrypt для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Хеширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Создание JWT токена
def create_token(email: str) -> str:
    payload = {
        "email": email,
        "timestamp": datetime.now().isoformat()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Декодирование JWT токена
def decode_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def register_user(name: str, email: str, password: str):
    user_exists = await user_collection.find_one({"email": email})
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now()
    }
    result = await user_collection.insert_one(new_user)
    return create_token(email)

async def authenticate_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return create_token(email)
    raise HTTPException(status_code=400, detail="Incorrect email or password")

async def get_user_todos(user_id: str, skip: int = 0, limit: int = 100):
    todos_cursor = await user_collection.find({"user_id": user_id}).skip(skip).limit(limit).to_list(length=limit)
    return todos_cursor

# Функция для создания задачи
async def create_todo_item(user_id: str, todo: TodoItem):
    todo_dict = todo.model_dump()
    todo_dict["user_id"] = user_id
    todo_dict["created_at"] = datetime.now()
    result = await user_collection.insert_one(todo_dict)
    return await get_todo_item(str(result.inserted_id))

# Функция для получения одной задачи по ID
async def get_todo_item(todo_id: str):
    todo = await user_collection.find_one({"_id": ObjectId(todo_id)})
    return todo

# Функция для обновления задачи
async def update_todo_item(todo_id: str, user_id: str, todo: TodoItem):
    update_data = {k: v for k, v in todo.model_dump().items() if v is not None}
    await user_collection.update_one({"_id": ObjectId(todo_id), "user_id": user_id}, {"$set": update_data})
    return await get_todo_item(todo_id)

# Функция для удаления задачи
async def delete_todo_item(todo_id: str, user_id: str):
    result = await user_collection.delete_one({"_id": ObjectId(todo_id), "user_id": user_id})
    return result.deleted_count