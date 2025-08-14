from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Platepal"
    API_V1_STR: str = "/api/v1"
    SALT: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int
    DATABASE_URL: str
    REDIS_URI: str

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
