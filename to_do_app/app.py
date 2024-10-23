from fastapi import FastAPI
from to_do_app.API import api_router
app = FastAPI()
app.include_router(api_router)