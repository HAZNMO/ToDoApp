from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from Users.user_repository import register_user, authenticate_user, decode_token

app = FastAPI()

class SignUpSchema(BaseModel):
    name: str
    email: str
    password: str

@app.post("/signup")
async def sign_up(request: SignUpSchema):
    token = await register_user(request.name, request.email, request.password)
    return {"token": token}

class SignInSchema(BaseModel):
    email: str
    password: str

@app.post("/signin")
async def sign_in(request: SignInSchema):
    token = await authenticate_user(request.email, request.password)
    return {"token": token}

@app.post("/authtest")
def auth_test(token: str = Depends(decode_token)):
    return {"email": token["email"]}
