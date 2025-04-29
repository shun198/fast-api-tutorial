from datetime import datetime, timedelta, timezone

import bcrypt
from config.env import app_settings
from jose import jwt


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


def check_password(raw_password, hashed_password) -> bool:
    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed_password.encode("utf-8"))


def hash_password(password: str):
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    return hashed_password
