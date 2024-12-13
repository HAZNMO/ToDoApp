import secrets

from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    JWT_SECRET: str = secrets.token_urlsafe(16)
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

class RunSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, init_settings, file_secret_settings

run_settings = RunSettings()
