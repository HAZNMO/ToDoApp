from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from API_construct.new_main import sign, decode

app = FastAPI()
userlist = []

class SignUpSchema(BaseModel):
    name: str = "Cris"
    email: str = "Cris@gmail.com"
    password: str = "Cris1234"

@app.post("/signup")
def sign_up(request: SignUpSchema):
    for user in userlist:
        if user.email == request.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    userlist.append(request)

    token = sign(request.email)

    for user in userlist:
        print(user.name, user.email, user.password)

    return {"token": token}

class SignInSchema(BaseModel):
    email: str = "Cris@gmail.com"
    password: str = "Cris1234"

@app.post("/signin")
def sign_in(request: SignInSchema):
    for user in userlist:
        if user.email == request.email:
            if user.password == request.password:
                token = sign(user.email)
                return {"token": token}
            else:
                raise HTTPException(status_code=400, detail="Incorrect password")
    raise HTTPException(status_code=400, detail="Incorrect email")

@app.post("/authtest")
def auth_test(decoded: str = Depends(decode)):
    return decoded

