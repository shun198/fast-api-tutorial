from pydantic_settings import BaseSettings
from config.env import app_settings


# https://github.com/aekasitt/fastapi-csrf-protect/blob/master/src/fastapi_csrf_protect/csrf_config.py
class CsrfSettings(BaseSettings):
  secret_key: str = app_settings.SECRET_KEY
  cookie_samesite :str = app_settings.COOKIE_SAME_SITE
  cookie_secure: bool = app_settings.COOKIE_SECURE
  httponly: bool = app_settings.COOKIE_HTTP_ONLY
  cookie_key: str = app_settings.CSRF_COOKIE_NAME
  header_name: str = app_settings.CSRF_HEADER_NAME
