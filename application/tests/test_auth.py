from datetime import timedelta
from fastapi import status
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


def test_create_user(client, test_user_one):
    response = client.post("/api/auth", json=test_user_one)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"msg": "user created"}
