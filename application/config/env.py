import os
import re

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
    SENDGRID_API_KEY: str = os.environ.get("SENDGRID_API_KEY")
    COOKIE_SECURE: bool = os.environ.get("COOKIE_SECURE") == "True"
    COOKIE_HTTP_ONLY: bool = os.environ.get("COOKIE_HTTP_ONLY") == "True"
    COOKIE_SAME_SITE: str = os.environ.get("COOKIE_SAME_SITE")
    CSRF_COOKIE_NAME: str = "csrftoken"
    CSRF_HEADER_NAME: str = "X-CSRF-Token"
    EXCLUDED_PATHS: list = [
        re.compile(r"^/api/auth/login"),
        re.compile(r"^/api/auth/logout"),
        re.compile(r"^/api//auth/refresh"),
    ]
    TEST_MODE: bool = os.environ.get("TEST") == "True"


app_settings = AppSettings()
