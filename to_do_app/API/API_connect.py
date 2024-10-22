from bson import ObjectId
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Body, status, Query
from pymongo import ReturnDocument
from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.domains.users.flow import register, login
from to_do_app.domains.to_dos.schemas import TodoModel, UpdateTODOModel, current_time_factory, TaskStatus, CreateTodoModel
from to_do_app.domains.users.schemas import UserCreate, UserLogin, UserResponse
from fastapi.security import HTTPBearer
from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import todo_collection

security = HTTPBearer()
app = FastAPI()
@app.post("/register", response_model=UserResponse)
async def register_route(user: UserCreate):
    return await register(user)

@app.post("/login", response_model=UserResponse)
async def login_route(user: UserLogin):
    return await login(user)

@app.get("/get_todos", response_model=list[TodoModel])
async def get_user_todos(
        user_info: dict = Depends(decode_token),
        task_status: Optional[TaskStatus] = Query(None, description="Task status to filter by (To Do, In Progress, Done)")):
    user_id = user_info.get("_id")
    query = {"user_id": user_id}

    if task_status is None:
        task_status = await todo_collection.find({"user_id": user_id}).to_list(1000)
        return task_status

    elif task_status:
        query["status"] = task_status

    todos = await todo_collection.find(query).to_list(1000)
    return todos

@app.post("/create_todos",
          response_description="Add new to do",
          response_model=CreateTodoModel,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False)
async def create_todo(todo: CreateTodoModel = Body(...), user_info: dict = Depends(decode_token)):
    todo.user_id = user_info.get("_id")

    new_todo_data = todo.model_dump(by_alias=True, exclude_unset=True)
    new_todo_data['created_at'] = current_time_factory()
    new_todo = await todo_collection.insert_one(new_todo_data)

    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return created_todo

@app.put("/todos/{todo_id}",
         response_description="Update a to do",
         response_model=UpdateTODOModel,
         response_model_by_alias=False)
async def update_todo(todo_id: str, todo_update: UpdateTODOModel = Body(...), user_info: dict = Depends(decode_token)):
    update_data = {k: v for k, v in todo_update.model_dump(by_alias=True).items() if v is not None}
    update_data["updated_at"] = current_time_factory()
    update_data["user_id"] = user_info.get("_id")
    update_result = await todo_collection.find_one_and_update(
        {"_id": ObjectId(todo_id), "user_id": user_info.get("_id")},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )

    if update_result is None:
        raise HTTPException(status_code=404, detail="Task not found or you do not have access to this todo")

    return update_result

@app.delete("/todos/{todo_id}", response_description="Delete a to do")
async def delete_todo(todo_id: str, user_info: dict = Depends(decode_token)):
    user_id = user_info.get("_id")
    delete_result = await todo_collection.delete_one({"_id": ObjectId(todo_id), "user_id": user_id})

    if delete_result.deleted_count == 1:
        return {"message": f"Task with ID {todo_id} was successfully deleted."}

    raise HTTPException(status_code=404, detail="Task not found or access denied")