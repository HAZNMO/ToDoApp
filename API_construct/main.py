from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn

app = FastAPI()


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


@app.get("/")
def home():
    return {"Welcome": "Page"}


@app.get("/get-user/{user_id}")
def get_user(user_id: int = Path(description="The id of the user", title="The id of the user", gt=0)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


@app.get("/get-by-name")
def get_user_by_name(name: Optional[str] = Query(None, description="The name of the user")):
    for user in users.values():
        if user.name == name:
            return user
    return {"Data": "Not Found"}


@app.post("/create-user/{user_id}")
def create_user(user_id: int, user: User):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user_id] = user
    return users[user_id]


@app.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = users[user_id]
    if user.name is not None:
        updated_user.name = user.name
    if user.username is not None:
        updated_user.username = user.username
    if user.password is not None:
        updated_user.password = user.password
    if user.email is not None:
        updated_user.email = user.email
    if user.age is not None:
        updated_user.age = user.age
    users[user_id] = updated_user
    return users[user_id]


@app.delete("/delete-user")
def delete_user(user_id: int = Query(description="The id of the user", title="The id of the user", gt=0)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"Detail": "User deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
