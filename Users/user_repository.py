from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime
import jwt
import os
from fastapi import HTTPException
import secrets

# Загрузка переменных окружения
load_dotenv()

# Настройка JWT и bcrypt
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(16))
JWT_ALGORITHM = "HS256"

# Настройка bcrypt для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Подключение к MongoDB
class MongoDBConnection:
    def __init__(self, database_name="tododb"):
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.database = self.client[database_name]

    def get_collection(self, collection_name):
        return self.database[collection_name]

mongodb_connection = MongoDBConnection()
user_collection = mongodb_connection.get_collection("users")

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
        "timestamp": datetime.utcnow().isoformat()
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

# Функция для регистрации нового пользователя
async def register_user(name: str, email: str, password: str):
    user_exists = await user_collection.find_one({"email": email})
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    result = await user_collection.insert_one(new_user)
    return create_token(email)

# Функция для авторизации пользователя
async def authenticate_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return create_token(email)
    raise HTTPException(status_code=400, detail="Incorrect email or password")
