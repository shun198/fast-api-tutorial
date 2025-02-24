from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_todos_unauthorized():
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_get_todos_unauthorized():
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_post_todos_unauthorized():
    response = client.post("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_put_todos_unauthorized():
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_todos_unauthorized():
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


