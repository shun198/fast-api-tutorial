from datetime import datetime, timedelta, timezone
from jose import jwt

from config.env import app_settings


def create_jwt_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {"sub": username, "iss": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM)


def decode_jwt_token(token: str):
    decoded_token = jwt.decode(
        token,
        app_settings.SECRET_KEY,
        algorithms=[app_settings.ALGORITHM],
    )
    return decoded_token
