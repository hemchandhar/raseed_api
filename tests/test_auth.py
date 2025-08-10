from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Raseed API"}

@patch("app.services.user_service.get_user_by_email")
@patch("app.services.user_service.create_user")
def test_register(mock_create_user, mock_get_user_by_email):
    mock_get_user_by_email.return_value = None
    mock_create_user.return_value = {"id": "some_id", "email": "test@example.com", "full_name": "Test User"}

    response = client.post("/auth/register", json={"email": "test@example.com", "password": "testpassword", "full_name": "Test User"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

@patch("app.services.user_service.get_user_by_email")
def test_register_existing_user(mock_get_user_by_email):
    mock_get_user_by_email.return_value = {"id": "some_id", "email": "test@example.com", "full_name": "Test User"}

    response = client.post("/auth/register", json={"email": "test@example.com", "password": "testpassword", "full_name": "Test User"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
