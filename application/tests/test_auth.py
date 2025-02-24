from datetime import timedelta

from jose import jwt
from main import app
from routers.auth import ALGORITHM, SECRET_KEY, create_access_token, get_db
from tests.utils import override_get_db

app.dependency_overrides[get_db] = override_get_db


def test_create_access_token():
    username = "testuser"
    user_id = 1
    is_admin = "user"
    expires_delta = timedelta(hours=1)

    token = create_access_token(username, user_id, is_admin, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["is_admin"] == is_admin
