import os

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    API_VERSION_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PROJECT_NAME: str = "finance_tracker_api"

    SQLALCHEMY_DATABASE_URI: PostgresDsn = os.environ.get(
        "POSTGRES_SQLALCHEMY_DATABASE_URI"
    )
    USERS_OPEN_REGISTRATION: bool = True


settings = Settings()
