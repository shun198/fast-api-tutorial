from datetime import timedelta

from fastapi import status
from jose import jwt
from routers.auth import ALGORITHM, SECRET_KEY, create_jwt_token


def test_create_jwt_token():
    username = "test_user_01"
    user_id = 1
    expires_delta = timedelta(minutes=30)

    token = create_jwt_token(username, user_id, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["iss"] == user_id


def test_create_user(client, test_admin_user_data):
    response = client.post("/api/auth", json=test_admin_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"msg": "user created"}


def test_create_user_duplicate(client):
    pass


def test_get_current_user():
    pass


def test_get_current_user_invalid_username():
    pass


def test_get_current_user_invalid_user_id():
    pass


def test_get_current_user_invalid_user_id():
    pass


def test_get_current_user_token_expired():
    pass


def test_get_current_user_token_invalid_jwt():
    pass


def test_login_for_access_token():
    pass


def test_login_for_access_token_invalid_username():
    pass


def test_login_for_access_token_invalid_password():
    pass


def test_refresh_token():
    pass


def test_refresh_token_user_not_found():
    pass
