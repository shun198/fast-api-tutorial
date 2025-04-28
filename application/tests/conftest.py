import bcrypt
import pytest

from routers.auth import get_current_user
from database import get_db
from fastapi.testclient import TestClient
from sqlalchemy import text
from tests.utils import (
    override_get_current_user,
    override_get_db,
    TestingSessionLocal,
    test_engine,
)
from models import Todos, Users
from main import app


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
def test_user_one():
    return {
        "email": "test_user_01@example.com",
        "username": "test_user_01",
        "first_name": "零一",
        "last_name": "テストユーザ",
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
        password=bcrypt.hashpw(("test").encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        ),
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
