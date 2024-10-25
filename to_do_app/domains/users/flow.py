from to_do_app.domains.users.service import authenticate_user, register_user
from to_do_app.domains.users.schemas import UserCreate, UserLogin, UserResponse

async def register(context: UserCreate):
    token = await register_user(context)
    return UserResponse(email=context.email, token=token)

async def login(context: UserLogin):
    token = await authenticate_user(context)
    return UserResponse(email=context.email, token=token)