from fastapi.security import HTTPBearer
from fastapi import APIRouter
from to_do_app.domains.users.flow import register, login
from to_do_app.domains.users.schemas import UserCreate, UserLogin, UserResponse

security = HTTPBearer()
users_router = APIRouter(prefix="/users")


@users_router.post("/register", response_model=UserResponse)
async def register_route(user: UserCreate):
    return await register(user)


@users_router.post("/login", response_model=UserResponse)
async def login_route(user: UserLogin):
    return await login(user)
