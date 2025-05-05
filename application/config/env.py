import os

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 1))
    SQLALCHEMY_DATABASE_URL: str = os.environ.get("SQLALCHEMY_DATABASE_URL")
    SLACK_WEBHOOK_URL: str = os.environ.get("SLACK_WEBHOOK_URL", "")
    DEBUG: bool = os.environ.get("DEBUG") == "True"


app_settings = AppSettings()
