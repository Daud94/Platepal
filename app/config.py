from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Platepal"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = ""
    SALT: str

    class Config:
        env_file = ".env"

        env_file_encoding = "utf-8"

settings = Settings()
