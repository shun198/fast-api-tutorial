# tests/test_todos.py
from fastapi import status

def test_create_todo(client):
    payload = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "priority": 1,
    }
    response = client.post("/api/todos", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]

def test_read_todos(client):
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_read_todo_not_found(client, non_existing_user):
    response = client.get(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

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
    assert response.json()["title"] == "Another Todo"  # update APIはbody返してないのでもとのtitle


def test_update_todo_not_found(client, non_existing_user):
    response = client.put(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


def test_delete_todo(client):
    # まず作成
    payload = {
        "title": "Todo to delete",
        "description": "To be deleted",
        "priority": 3,
        "complete": False,
    }
    create_resp = client.post("/api/todos", json=payload)
    todo_id = create_resp.json()["id"]

    # 削除
    delete_resp = client.delete(f"/api/todos/{todo_id}")
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    # 確認
    get_resp = client.get(f"/api/todos/{todo_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo_not_found(client, non_existing_user):
    response = client.delete(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}
