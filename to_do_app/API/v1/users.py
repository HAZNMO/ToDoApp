from fastapi import APIRouter
from fastapi.security import HTTPBearer

from to_do_app.API.utils.datetime import utcnow
from to_do_app.API.utils.decorator_convert import convert_result
from to_do_app.domains.users.flow import login
from to_do_app.domains.users.flow import register
from to_do_app.domains.users.schemas import UserCreate
from to_do_app.domains.users.schemas import UserLogin
from to_do_app.domains.users.schemas import UserResponse
from to_do_app.domains.users.schemas import UserWithDetails

security = HTTPBearer()
users_router = APIRouter(prefix="/users")


@users_router.post("/register", tags=["Users"], response_model=UserResponse)
@convert_result
async def register_route(user: UserCreate) -> UserResponse:
    user_with_details = UserWithDetails(**user.model_dump(), created_at=utcnow())
    return await register(user_with_details)


@users_router.post("/login", tags=["Users"], response_model=UserResponse)
@convert_result
async def login_route(user: UserLogin) -> UserResponse:
    return await login(user)
