from contextlib import asynccontextmanager
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Depends, Body, status
from pymongo import ReturnDocument
from Users.user_authentification import authenticate_user, register_user, decode_token
from TODOS.todo_model import TodoModel, UpdateTODOModel, current_time_factory
from Users.user_model import UserCreate, UserLogin, UserResponse
from fastapi.security import HTTPBearer
from mongodb_connect.mongo_connection import todo_collection
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

@app.post("/create_todos",
          response_description="Add new to do",
          response_model=TodoModel,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False)
async def create_todo(todo: TodoModel = Body(...), user_info: dict = Depends(decode_token)):
    todo.user_email = user_info.get("email")  # Устанавливаем email пользователя
    new_todo = await todo_collection.insert_one(todo.model_dump(by_alias=True, exclude=["id"]))
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return created_todo


@app.get("/get_todos", response_model=list[TodoModel])
async def get_user_todos(user_info: dict = Depends(decode_token)):
    user_email = user_info.get("email")
    todos = await todo_collection.find({"user_email": user_email}).to_list(1000)
    return todos


@app.put("/todos/{id}",
         response_description="Update a to do",
         response_model=TodoModel,
         response_model_by_alias=False)
async def update_todo(id: str, todo: UpdateTODOModel = Body(...), user_info: dict = Depends(decode_token)):
    update_data = {k: v for k, v in todo.model_dump(by_alias=True).items() if v is not None}
    update_data["updated_at"] = current_time_factory()  # Устанавливаем время обновления
    update_data["user_email"] = user_info.get("email")  # Добавляем email пользователя
    update_result = await todo_collection.find_one_and_update(
        {"_id": ObjectId(id), "user_email": user_info.get("email")},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )

    if update_result is None:
        raise HTTPException(status_code=404, detail="Task not found or you do not have access to this todo")

    return update_result


@app.delete("/todos/{id}", response_description="Delete a to do")
async def delete_todo(id: str, user_info: dict = Depends(decode_token)):
    user_email = user_info.get("email")
    delete_result = await todo_collection.delete_one({"_id": ObjectId(id), "user_email": user_email})

    if delete_result.deleted_count == 1:
        return {"message": f"Task with ID {id} was successfully deleted."}

    raise HTTPException(status_code=404, detail="Task not found or access denied")