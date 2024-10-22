from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import user_collection
from to_do_app.dependences.auth.dependeces import hash_password, verify_password, create_token
from fastapi import HTTPException
from datetime import datetime


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