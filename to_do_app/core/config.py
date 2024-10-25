import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_url: str
    JWT_SECRET: str = secrets.token_urlsafe(16)
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
