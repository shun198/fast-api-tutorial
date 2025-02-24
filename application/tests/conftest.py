import os

import pytest
from database import Base
from fastapi.testclient import TestClient
from main import app
from routers.auth import get_current_user, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "test_user_01", "id": 1}


@pytest.fixture
def client():
    return TestClient(app)


# https://docs.pytest.org/en/stable/how-to/fixtures.html
# https://github.com/tiangolo/fastapi/tree/master/tests
@pytest.fixture
def auth_client():
    # https://fastapi.tiangolo.com/advanced/testing-dependencies/
    # https://fastapi.tiangolo.com/tutorial/testing/
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    # https://www.starlette.io/testclient/
    auth_client = TestClient(app)
    yield auth_client
    app.dependency_overrides.clear()


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


# todo: テスト実行時のテストデータのinsertとロールバックの実装
# https://dev.classmethod.jp/articles/flask-sqlalchemy-pytest-mysql/
