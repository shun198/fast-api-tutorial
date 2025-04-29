from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from main import app
from models.todo import Todos
from models.user import Users
from config.jwt import create_jwt_token, hash_password
from config.dependency import get_current_user
from sqlalchemy import text
from tests.utils import (
    TestingSessionLocal,
    override_get_current_user,
    override_get_db,
    test_engine,
)

from infrastructure.database import get_db


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client


@pytest.fixture
def non_existing_user():
    return "99999"


@pytest.fixture
def test_admin_user_data():
    return {
        "email": "test_admin_user_01@example.com",
        "username": "test_admin_user_01",
        "first_name": "零一",
        "last_name": "テスト管理ユーザ",
        "password": "test",
        "is_active": True,
        "is_admin": True,
        "phone_number": "08011112222",
    }


@pytest.fixture
def test_user_one():
    user = Users(
        id=1,
        username="test_user_01",
        email="test_user_01@example.com",
        first_name="零一",
        last_name="テストユーザ",
        password=hash_password("test"),
        is_active=True,
        is_admin=True,
        phone_number="08011112222",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with test_engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_todo_one():
    user = override_get_current_user()
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    todo = Todos(
        id=1,
        title="test task 01",
        description="description of test task 01",
        priority=1,
        complete=False,
        owner_id=user.id,
    )
    db.add(todo)
    db.commit()
    yield todo
    with test_engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def headers():
    user = override_get_current_user()
    jwt_token = create_jwt_token(user.username, user.id, timedelta(minutes=30))
    headers = {"Authorization": f"Bearer {jwt_token}"}
    return headers
