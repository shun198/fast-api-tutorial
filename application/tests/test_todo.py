from fastapi import status


def test_list_todos_unauthorized(client):
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_get_todos_not_found(auth_client, non_existing_user):
    response = auth_client.get(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_get_todos_unauthorized(client):
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_post_todos_unauthorized(client):
    response = client.post("/api/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_put_todos_not_found(auth_client, non_existing_user):
    response = auth_client.put(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_put_todos_unauthorized(client):
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_todos_not_found(auth_client, non_existing_user):
    response = auth_client.delete(f"/api/todos/{non_existing_user}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    

def test_delete_todos_unauthorized(client):
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


