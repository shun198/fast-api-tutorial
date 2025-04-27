from fastapi import status
from main import app
from routers.auth import get_current_user, get_db
from tests.utils import client, override_get_current_user, override_get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_list_todos_unauthorized():
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_list_todos(test_todo):
    response = client.get(
        "/api/todos",
        headers={"Authorization": "Bearer faketoken"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_todos_not_found(non_existing_user):
    response = client.get(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_get_todos_unauthorized():
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_post_todos(test_todo_one):
    response = client.post("/api/todos", json=test_todo_one)
    assert response.status_code == status.HTTP_201_CREATED


def test_post_todos_unauthorized():
    response = client.post("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_put_todos_not_found(non_existing_user, test_todo_one):
    response = client.put(f"/api/todos/{non_existing_user}", json=test_todo_one)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_put_todos_unauthorized():
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_todos_not_found(client, non_existing_user):
    response = client.delete(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todos_unauthorized():
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}
