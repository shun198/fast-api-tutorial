import pytest


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
