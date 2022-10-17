import os
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    root_path: str

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()
