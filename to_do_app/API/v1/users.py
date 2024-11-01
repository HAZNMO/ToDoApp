from fastapi import APIRouter
from fastapi.security import HTTPBearer

from to_do_app.domains.users.flow import login
from to_do_app.domains.users.flow import register
from to_do_app.domains.users.schemas import UserLogin
from to_do_app.domains.users.schemas import UserResponse
from to_do_app.domains.users.schemas import UserWithDetails

security = HTTPBearer()
users_router = APIRouter(prefix="/users")


@users_router.post("/register", tags=["Users"], response_model=UserResponse)
async def register_route(user: UserWithDetails):
    return await register(user)


@users_router.post("/login", tags=["Users"], response_model=UserResponse)
async def login_route(user: UserLogin) -> UserResponse:
    return await login(user)
