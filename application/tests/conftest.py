import pytest
from fastapi.testclient import TestClient
from main import app
from routers.auth import get_current_user, get_db
from tests.utils import override_get_current_user, override_get_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    auth_client = TestClient(app)
    yield auth_client
    app.dependency_overrides.clear()


@pytest.fixture
def non_existing_user():
    return "99999"
