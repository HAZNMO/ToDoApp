from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import user_collection
from to_do_app.dependencies.auth.dependencies import (
    hash_password,
    verify_password,
    create_token,
)
from to_do_app.domains.users.schemas import UserCreate, UserLogin
from fastapi import HTTPException
from datetime import datetime


async def register_user(user_create: UserCreate):
    user_exists = await user_collection.find_one({"email": user_create.email})
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_create.password)
    new_user = {
        "name": user_create.name,
        "email": user_create.email,
        "password": hashed_password,
        "created_at": datetime.now(),
    }

    result = await user_collection.insert_one(new_user)

    if result.inserted_id is None:
        raise HTTPException(status_code=500, detail="Failed to register user")

    user_id = str(result.inserted_id)
    return create_token(user_id, user_create.email)


async def authenticate_user(user_login: UserLogin):
    user = await user_collection.find_one({"email": user_login.email})
    if user and verify_password(user_login.password, user["password"]):
        user_id = str(user["_id"])
        return create_token(user_id, user_login.email)
    raise HTTPException(status_code=400, detail="Incorrect email or password")
