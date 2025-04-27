import pytest

from routers.auth import get_current_user, get_db
from fastapi.testclient import TestClient
from tests.utils import override_get_current_user, override_get_db
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
def test_todo_one():
    return {
        "title": "test task 01",
        "description": "description of test task 01",
        "priority": 1,
        "complete": False,
    }
