from fastapi.testclient import TestClient


def test_create_user(client: TestClient, user_data):
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
