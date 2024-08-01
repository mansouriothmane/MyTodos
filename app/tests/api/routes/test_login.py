from fastapi.testclient import TestClient


def test_login(client: TestClient, test_user, login_data):
    response = client.post("/token", json=login_data)
    assert response.status_code == 200
    assert response.json()["access_token"]
