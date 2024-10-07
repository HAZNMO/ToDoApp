from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI, Path, Query
import uvicorn

TODO_app = FastAPI()

class User(BaseModel):
    name: Optional[str] = None
    username: str
    password: str
    email: str
    age: Optional[int] = None
    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


users = {}
@TODO_app.get("/")
def home():
    return {"Welcome": "Page"}

@TODO_app.get("/get-user/{user_id}/{name}")
def get_user(user_id: int = Path(description="The id of the user", title="The id of the user", gt=0)):
    return users[user_id]

@TODO_app.get("/get-by-name")
def get_user(name: Optional[str] = Query(None, description="The name of the user")):
    for user_id in users:
        if users[user_id].name == name:
            return users[user_id]
    return {"Data": "Not Found"}

@TODO_app.post("/create-user/{user_id}")
def create_user(user_id: int):
    if user_id in users:
        return {"Data": "User already exists"}

    users[user_id] = users
    return users[user_id]

@TODO_app.put("/update-user/{user_id}")
def update_user(user_id: int, user : UpdateUser):
    if user_id not in users:
        return {"Error": "User not found"}

    if user.name != None:
        users[user_id].name = user.name

    if user.username != None:
        users[user_id].username = user.username

    if user.password != None:
        users[user_id].password = user.password

    if user.email != None:
        users[user_id].password = user.password

    if user.age != None:
        users[user_id].age = user.age

    return users[user_id]

@TODO_app.delete("/delete-user")
def delete_user(user_id: int = Query(description="The id of the user", title="The id of the user", gt=0)):
    if user_id not in users:
        return {"Error": "User not found"}

    del users[user_id]


if __name__ == "__main__":
    uvicorn.run(TODO_app, host="0.0.0.0", port=8000)