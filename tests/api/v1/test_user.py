from fastapi.testclient import TestClient

from app.api.v1.user import get_user_service
from app.main import app
from app.services.user_service import UserService
from tests.test_db import TestingSessionLocal

# Setup the TestClient
client = TestClient(app)

# Dependency to override the get_db dependency in the main app
def override_get_user_service():
    session = TestingSessionLocal()
    yield UserService(session=session)

app.dependency_overrides[get_user_service] = override_get_user_service


def test_create_and_get_user():
    # Create a new user
    response = client.post("/api/v1/users", json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["name"] == "Test User"
    assert "id" in created_user

    # Fetch the created user
    get_response = client.get(f"/api/v1/users/{created_user['id']}")
    assert get_response.status_code == 200
    fetched_user = get_response.json()
    assert fetched_user["id"] == created_user["id"]
    assert fetched_user["name"] == created_user["name"]


def test_get_nonexistent_user():
    response = client.get("/api/v1/users/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_list_users():
    # Ensure there is at least one user
    response = client.post("/api/v1/users", json={"name": "Another User", "email": "another@example.com"})
    users = client.get("/api/v1/users")
    assert users.status_code == 200
    assert len(users.json()) >= 1

def test_update_user():
    # Create a new user to update
    response = client.post("/api/v1/users", json={"name": "Update User", "email": "update@example.com"})
    created_user = response.json()
    user_id = created_user["id"]
    # Update the user's name
    update_response = client.put(f"/api/v1/users/{user_id}", json={"name": "Updated Name", "email": "updated@example.com"})
    assert update_response.status_code == 200
    updated_user = update_response.json()
    assert updated_user["name"] == "Updated Name"


def test_update_nonexistent_user():
    update_response = client.put("/api/v1/users/9999", json={"name": "Nonexistent User", "email": "some@example.com"})
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "User not found"}


def test_delete_user():
    # Create a new user to delete
    response = client.post("/api/v1/users", json={"name": "Delete User", "email": "delete@example.com"})
    created_user = response.json()
    user_id = created_user["id"]
    # Delete the user
    delete_response = client.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 200
    # Verify the user is deleted
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "User not found"}


def test_delete_nonexistent_user():
    delete_response = client.delete("/api/v1/users/9999")
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "User not found"}
