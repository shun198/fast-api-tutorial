from datetime import timedelta

from jose import jwt
from routers.auth import ALGORITHM, SECRET_KEY, create_access_token


def test_create_access_token():
    username = "testuser"
    user_id = 1
    expires_delta = timedelta(hours=1)

    token = create_access_token(username, user_id, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
