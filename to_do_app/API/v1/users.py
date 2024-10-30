from fastapi import APIRouter
from fastapi.security import HTTPBearer

from to_do_app.domains.users.flow import login
from to_do_app.domains.users.flow import register
from to_do_app.domains.users.schemas import UserCreate
from to_do_app.domains.users.schemas import UserLogin
from to_do_app.domains.users.schemas import UserResponse

security = HTTPBearer()
users_router = APIRouter(prefix="/users")


@users_router.post("/register", tags=["Users"], response_model=UserResponse)
async def register_route(user: UserCreate):
    return await register(user)


@users_router.post("/login", tags=["Users"], response_model=UserResponse)
async def login_route(user: UserLogin) -> UserResponse:
    return await login(user)
