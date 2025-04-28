from datetime import timedelta

from fastapi import status
from routers.auth import create_jwt_token
from tests.utils import TestingSessionLocal, override_get_current_user


def test_create_todo(client):
    payload = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "priority": 1,
    }
    user = override_get_current_user()
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    jwt_token = create_jwt_token(user.username, user.id, timedelta(minutes=30))
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/api/todos", json=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["priority"] == payload["priority"]


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


def test_read_todo_not_found(client, non_existing_user):
    response = client.get(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo(client):
    # まず作成
    payload = {
        "title": "Another Todo",
        "description": "Another test",
        "priority": 2,
    }
    create_resp = client.post("/api/todos", json=payload)
    todo_id = create_resp.json()["id"]

    # 更新
    updated_payload = {
        "title": "Updated Todo",
        "description": "Updated description",
        "priority": 5,
    }
    response = client.put(f"/api/todos/{todo_id}", json=updated_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Another Todo"


def test_update_todo_not_found(client, non_existing_user):
    response = client.put(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(client):
    payload = {
        "title": "Todo to delete",
        "description": "To be deleted",
        "priority": 3,
        "complete": False,
    }
    create_resp = client.post("/api/todos", json=payload)
    todo_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/api/todos/{todo_id}")
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    get_resp = client.get(f"/api/todos/{todo_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo_not_found(client, non_existing_user):
    response = client.delete(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
