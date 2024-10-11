from contextlib import asynccontextmanager

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Depends, Body, status
from fastapi.responses import Response
from pymongo import ReturnDocument

from Users.user_repository import (
    get_user_todos,update_todo_item, delete_todo_item)
from Users.user_authentification import authenticate_user, register_user, decode_token
from TODOS.todo_model import TodoModel, UpdateTODOModel, PyObjectId
from TODOS.todo_repository import save_todo_item
from Users.user_model import UserCreate, UserLogin, UserResponse
from fastapi.security import HTTPBearer
from mongodb_connect.mongo_connection import todo_collection
from Users.user_collection import user_todos
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
          response_model_by_alias=False,)
async def create_todo(todo: TodoModel = Body(...)):
    new_todo = await todo_collection.insert_one(todo.model_dump(by_alias=True, exclude=["id"]))
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return created_todo

@app.get("/get_todos")
async def list_todos():
    return user_todos(todos = await todo_collection.find().to_list(1000))

@app.put("/todos/{id}",
         response_description="Update a to do",
         response_model=TodoModel,
         response_model_by_alias=False,
         )
async def update_todo(id: str,todo: UpdateTODOModel = Body(...)):
    update_data = {k: v for k, v in todo.model_dump(by_alias=True).items() if v is not None}

    if len(update_data) >= 1:
        update_result = await todo_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"To do {id} not found")

    raise HTTPException(status_code=404, detail=f"To do {id} not found")


@app.delete("/todos/{id}", response_description="Delete a to do")
async def delete_todo(id: str):
    delete_result = await todo_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"To do {id} not found")


# @app.post("/todo")
# async def create_todo_route(todo: TodoModel, user_id: dict = Depends(decode_token)):
#     todo_item = await save_todo_item(user_id['email'], todo)
#     return todo_item
#
# @app.get("/todo")
# async def get_todo(user_id: dict = Depends(decode_token)):
#     todos = await get_user_todos(user_id['email'])
#     return todos
#
# @app.get("/todos")
# async def get_todos():
#    todos = await get_todos()
#    return todos

# @app.get("/todos")
# async def get_todos(user_id: dict = Depends(decode_token)):
#     todos = await get_user_todos(user_id['email'])
#     return todos, user_id

# @app.put("/todos/{todo_id}")
# async def update_todo_item(todo_id: str, todo: TodoModel, user_id: dict = Depends(decode_token)):
#     updated_todo_item = await update_todo_item(todo_id, user_id['email'], todo)
#     if not updated_todo_item:
#         raise HTTPException(status_code=404, detail="Todo not found or you do not have access to this todo")
#     return updated_todo_item

# @app.delete("/todojs/{todo_id}")
# async def delete_todo_item(todo_id: str, user_id: dict = Depends(decode_token)):
#     deleted_count = await delete_todo_item(todo_id, user_id['email'])
#     if deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Todo not found or you do not have access to this todo")
#     return {"detail": "Todo deleted successfully"}
