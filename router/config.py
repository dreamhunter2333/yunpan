import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    root_path: str = "data"
    password: str = "password"
    secret: str = "secret"

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()
