from to_do_app.domains.users.service import authenticate_user, register_user
from to_do_app.domains.users.schemas import UserCreate, UserLogin, UserResponse

async def register(user: UserCreate):
    token = await register_user(user.name, user.email, user.password)
    return UserResponse(email=user.email, token=token)

async def login(user: UserLogin):
    token = await authenticate_user(user.email, user.password)
    return UserResponse(email=user.email, token=token)