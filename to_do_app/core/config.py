import secrets

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    JWT_SECRET: str = secrets.token_urlsafe(16)
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

class RunSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000

run_settings = RunSettings()
