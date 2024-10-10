from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from Users.user_repository import (
    get_user_todos,
    update_todo_item, delete_todo_item)
from Users.user_authentification import authenticate_user, register_user, decode_token
from TODOS.todo_model import TodoModel
from TODOS.todo_repository import save_todo_item
from Users.user_model import UserCreate, UserLogin, UserResponse
from fastapi.security import HTTPBearer
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app):
    from mongodb_connect.mongo_connection import mongodb_connection

    try:
        await mongodb_connection.client.admin.command("ping")
    except Exception as e:
        print("Mongo Error", e)
        raise e

    yield
app = FastAPI(lifespan=lifespan)

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    token = await register_user(user.name, user.email, user.password)
    return UserResponse(email=user.email, token=token)

@app.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    token = await authenticate_user(user.email, user.password)
    return UserResponse(email=user.email, token=token)

@app.post("/todo")
async def create_todo_route(todo: TodoModel, user_id: dict = Depends(decode_token)):
    todo_item = await save_todo_item(user_id['email'], todo)
    return todo_item

@app.get("/todo")
async def get_todo(user_id: dict = Depends(decode_token)):
    todos = await get_user_todos(user_id['email'])
    return todos

@app.get("/todos")
async def get_todos():
   todos = await get_todos()
   return todos

# @app.get("/todos")
# async def get_todos(user_id: dict = Depends(decode_token)):
#     todos = await get_user_todos(user_id['email'])
#     return todos, user_id

@app.put("/todos/{todo_id}")
async def update_todo_item(todo_id: str, todo: TodoModel, user_id: dict = Depends(decode_token)):
    updated_todo_item = await update_todo_item(todo_id, user_id['email'], todo)
    if not updated_todo_item:
        raise HTTPException(status_code=404, detail="Todo not found or you do not have access to this todo")
    return updated_todo_item

@app.delete("/todos/{todo_id}")
async def delete_todo_item(todo_id: str, user_id: dict = Depends(decode_token)):
    deleted_count = await delete_todo_item(todo_id, user_id['email'])
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found or you do not have access to this todo")
    return {"detail": "Todo deleted successfully"}
