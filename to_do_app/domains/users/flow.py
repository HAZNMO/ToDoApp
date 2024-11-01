from to_do_app.domains.users.schemas import UserLogin
from to_do_app.domains.users.schemas import UserResponse
from to_do_app.domains.users.schemas import UserWithDetails
from to_do_app.domains.users.service import authenticate_user
from to_do_app.domains.users.service import register_user


async def register(context: UserWithDetails) -> UserResponse:
    token = await register_user(context)
    return UserResponse(email=context.email, token=token)


async def login(context: UserLogin) -> UserResponse:
    token = await authenticate_user(context)
    return UserResponse(email=context.email, token=token)
