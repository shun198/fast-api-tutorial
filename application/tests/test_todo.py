from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_todos_unauthorized():
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}
