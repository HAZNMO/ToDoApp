from fastapi import APIRouter
from to_do_app.API.v1.todos import todos_router
from to_do_app.API.v1.users import users_router
v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users_router)
v1_router.include_router(todos_router)