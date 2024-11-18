from fastapi import HTTPException

from to_do_app.API.utils.datetime import utcnow
from to_do_app.dependencies.auth.dependencies import create_token
from to_do_app.dependencies.auth.dependencies import hash_password
from to_do_app.dependencies.auth.dependencies import verify_password
from to_do_app.dependencies.auth.schemas import UserBase
from to_do_app.domains.users.schemas import UserCreate
from to_do_app.domains.users.schemas import UserLogin
from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import user_collection


async def register_user(user_create: UserCreate, collection=user_collection):
    user_exists = await collection.find_one({"email": user_create.email})
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_create.password)

    new_user_data = user_create.model_copy(
        update={"password": hashed_password, "created_at": utcnow()}
    ).model_dump()

    result = await collection.insert_one(new_user_data)

    if result.inserted_id is None:
        raise HTTPException(status_code=500, detail="Failed to register user")

    user_id = str(result.inserted_id)
    user_base = UserBase(user_id=user_id, email=user_create.email)
    token = create_token(user_base)

    return token

async def authenticate_user(user_login: UserLogin):
    user = await user_collection.find_one({"email": user_login.email})
    if user and verify_password(user_login.password, user["password"]):
        user_id = str(user["_id"])
        user_base = UserBase(user_id=user_id, email=user_login.email)
        return create_token(user_base)
    raise HTTPException(status_code=400, detail="Incorrect email or password")
