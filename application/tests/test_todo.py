import pytest
from config.dependency import get_current_user
from fastapi import status
from main import app


@pytest.fixture
def create_data():
    return {
        "title": "Created Todo",
        "description": "Created test",
        "is_starred": False,
    }


@pytest.fixture
def update_data():
    return {
        "title": "Updated Todo",
        "description": "Updated test",
        "is_starred": False,
        "is_completed": True,
    }


def test_list_todos(client, headers, test_todo_one):
    response = client.get("/api/todos", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json() == [
        {
            "id": test_todo_one.id,
            "title": test_todo_one.title,
            "description": test_todo_one.description,
            "is_starred": test_todo_one.is_starred,
            "is_completed": test_todo_one.is_completed,
            "owner_id": test_todo_one.owner_id,
        }
    ]


def test_list_todos_unauthorized(client):
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_todo(client, headers, test_todo_one):
    response = client.get(f"/api/todos/{test_todo_one.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": test_todo_one.id,
        "title": test_todo_one.title,
        "description": test_todo_one.description,
        "is_starred": test_todo_one.is_starred,
        "is_completed": test_todo_one.is_completed,
        "owner_id": test_todo_one.owner_id,
    }


def test_read_todo_not_found(client, headers, non_existing_user):
    response = client.get(f"/api/todos/{non_existing_user}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_read_todos_unauthorized(client, test_todo_one):
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get(f"/api/todos/{test_todo_one.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_todo(client, headers, create_data, test_todo_one):
    response = client.post("/api/todos", json=create_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == create_data["title"]
    assert response.json()["description"] == create_data["description"]
    assert response.json()["is_starred"] == create_data["is_starred"]


def test_create_todos_unauthorized(client, create_data):
    app.dependency_overrides.pop(get_current_user, None)
    response = client.post(f"/api/todos/", json=create_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_todo(client, headers, update_data, test_todo_one):
    response = client.put(
        f"/api/todos/{test_todo_one.id}", json=update_data, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == update_data["title"]
    assert response.json()["description"] == update_data["description"]
    assert response.json()["is_starred"] == update_data["is_starred"]


def test_update_todo_not_found(client, headers, update_data, non_existing_user):
    response = client.put(
        f"/api/todos/{non_existing_user}", json=update_data, headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_update_todos_unauthorized(client, update_data, test_todo_one):
    app.dependency_overrides.pop(get_current_user, None)
    response = client.put(f"/api/todos/{test_todo_one.id}", json=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_todo(client, headers, test_todo_one):
    response = client.delete(f"/api/todos/{test_todo_one.id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_todo_not_found(client, headers, non_existing_user):
    response = client.delete(f"/api/todos/{non_existing_user}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo_unauthorized(client, test_todo_one):
    app.dependency_overrides.pop(get_current_user, None)
    response = client.delete(f"/api/todos/{test_todo_one.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
