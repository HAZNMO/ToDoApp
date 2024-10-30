import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_url: str
    JWT_SECRET: str = secrets.token_urlsafe(16)
    JWT_ALGORITHM: str = "HS256"

    # TODO use pydantic 2 approach https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage
    class Config:
        env_file = ".env"


settings = Settings()
