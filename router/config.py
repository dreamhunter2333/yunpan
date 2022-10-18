import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    root_path: str
    password: str
    secret: str

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()
