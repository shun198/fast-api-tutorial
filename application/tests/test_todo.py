from datetime import timedelta

from fastapi import status
from routers.auth import create_jwt_token
from tests.utils import override_get_current_user


def test_list_todos(client, test_todo_one):
    user = override_get_current_user()
    jwt_token = create_jwt_token(user.username, user.id, timedelta(minutes=30))
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/api/todos", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json() == [
        {
            "id": test_todo_one.id,
            "title": test_todo_one.title,
            "description": test_todo_one.description,
            "priority": test_todo_one.priority,
            "complete": test_todo_one.complete,
            "owner_id": test_todo_one.owner_id,
        }
    ]


def test_read_todo(client, test_todo_one):
    response = client.get(f"/api/todos/{test_todo_one.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==  {
            "id": test_todo_one.id,
            "title": test_todo_one.title,
            "description": test_todo_one.description,
            "priority": test_todo_one.priority,
            "complete": test_todo_one.complete,
            "owner_id": test_todo_one.owner_id,
        }


def test_read_todo_not_found(client, non_existing_user):
    response = client.get(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(client, test_todo_one):
    payload = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "priority": 1,
    }
    user = override_get_current_user()
    jwt_token = create_jwt_token(user.username, user.id, timedelta(minutes=30))
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/api/todos", json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["priority"] == payload["priority"]


def test_update_todo(client, test_todo_one):
    # まず作成
    payload = {
        "title": "Updated Todo",
        "description": "Updated test",
        "priority": 2,
    }
    user = override_get_current_user()
    jwt_token = create_jwt_token(user.username, user.id, timedelta(minutes=30))
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.put(f"/api/todos/{test_todo_one.id}", json=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["priority"] == payload["priority"]


def test_update_todo_not_found(client, non_existing_user):
    response = client.put(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(client, test_todo_one):
    user = override_get_current_user()
    jwt_token = create_jwt_token(user.username, user.id, timedelta(minutes=30))
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.delete(f"/api/todos/{test_todo_one.id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_todo_not_found(client, non_existing_user):
    response = client.delete(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
