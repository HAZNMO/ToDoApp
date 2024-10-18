import jwt
import os
import secrets
from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from to_do_api.Infrastructure.DB.mongo_db.mongo_construct import user_collection
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from passlib.context import CryptContext

def utcnow():
    return datetime.now(tz=timezone.utc)

TOKEN_EXPIRE_MINUTES = 30  # Время действия токена в минутах

security = HTTPBearer()
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_hex(16))
JWT_ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# # Создание JWT токена
def create_token(user_id: str, email: str) -> str:
    expiration = utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        "_id": user_id,
        "email": email,
        "exp": expiration,
        "timestamp": utcnow().isoformat()  # UTC для согласованности
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Декодирование JWT токена
def decode_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
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

    if result.inserted_id is None:
        raise HTTPException(status_code=500, detail="Failed to register user")

    user_id = str(result.inserted_id)
    return create_token(user_id, email)

async def authenticate_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        user_id = str(user["_id"])
        return create_token(user_id, email)
    raise HTTPException(status_code=400, detail="Incorrect email or password")




