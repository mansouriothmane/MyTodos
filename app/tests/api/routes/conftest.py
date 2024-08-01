from fastapi.testclient import TestClient
import pytest

from app.schemas.user import UserResponse


@pytest.fixture
def user_data():
    return {"name": "test", "email": "test@yahoo.fr", "password": "test"}


@pytest.fixture
def login_data():
    return {"username": "test@yahoo.fr", "password": "test"}


@pytest.fixture
def test_user(client: TestClient, user_data) -> UserResponse:
    response = client.post("/users", json=user_data)
    return response.json()
