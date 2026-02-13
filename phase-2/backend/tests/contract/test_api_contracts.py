"""
Contract tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from src.schemas.user import UserCreate, UserRead
from src.schemas.task import TaskCreate, TaskRead
from typing import Dict, Any


def test_api_contract_user_registration(client: TestClient):
    """Test that user registration API contract matches specification."""
    user_data = {
        "email": "contract@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/v1/register", json=user_data)

    assert response.status_code == 200
    data = response.json()

    # Verify response structure matches UserRead schema
    assert "id" in data
    assert isinstance(data["id"], str)  # UUID as string
    assert "email" in data
    assert data["email"] == user_data["email"]
    assert "created_at" in data
    assert "updated_at" in data
    assert "is_active" in data
    assert isinstance(data["is_active"], bool)


def test_api_contract_user_login(client: TestClient):
    """Test that user login API contract matches specification."""
    # First register a user
    register_data = {
        "email": "logincontract@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200

    # Login
    login_data = {
        "email": "logincontract@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/v1/login", json=login_data)

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


def test_api_contract_task_crud(client: TestClient):
    """Test that task CRUD API contracts match specification."""
    # Register and login user
    register_data = {
        "email": "taskcontract@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    login_data = {
        "email": "taskcontract@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Test POST /api/{user_id}/tasks
    task_data = {
        "title": "Contract Test Task",
        "description": "This tests the task creation contract",
        "completed": False
    }

    create_response = client.post(
        f"/api/v1/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 200
    created_task = create_response.json()

    # Verify response structure matches TaskRead schema
    assert "id" in created_task
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["completed"] == task_data["completed"]
    assert "user_id" in created_task
    assert "created_at" in created_task
    assert "updated_at" in created_task

    task_id = created_task["id"]

    # Test GET /api/{user_id}/tasks/{id}
    get_response = client.get(
        f"/api/v1/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    retrieved_task = get_response.json()

    # Verify structure again
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == task_data["title"]
    assert retrieved_task["completed"] == task_data["completed"]

    # Test GET /api/{user_id}/tasks (list)
    list_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert list_response.status_code == 200
    tasks_list = list_response.json()
    assert isinstance(tasks_list, list)
    assert len(tasks_list) >= 1  # At least our created task
    assert any(task["id"] == task_id for task in tasks_list)


def test_api_contract_task_update(client: TestClient):
    """Test that task update API contract matches specification."""
    # Register and login user
    register_data = {
        "email": "updatecontract@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    login_data = {
        "email": "updatecontract@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a task
    task_data = {
        "title": "Original Title",
        "description": "Original Description",
        "completed": False
    }

    create_response = client.post(
        f"/api/v1/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]

    # Update the task
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }

    update_response = client.put(
        f"/api/v1/{user_id}/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()

    # Verify response structure and values
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    assert updated_task["completed"] == update_data["completed"]


def test_api_contract_task_completion_toggle(client: TestClient):
    """Test that task completion toggle API contract matches specification."""
    # Register and login user
    register_data = {
        "email": "togglecontract@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    login_data = {
        "email": "togglecontract@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a task
    task_data = {
        "title": "Toggle Contract Task",
        "description": "Task for testing completion toggle contract",
        "completed": False
    }

    create_response = client.post(
        f"/api/v1/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]

    # Toggle completion
    toggle_response = client.patch(
        f"/api/v1/{user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()

    # Verify response structure and that completion state changed
    assert toggled_task["id"] == task_id
    assert toggled_task["completed"] == True  # Should be toggled to True

    # Toggle back to False
    toggle_back_response = client.patch(
        f"/api/v1/{user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert toggle_back_response.status_code == 200
    toggled_back_task = toggle_back_response.json()

    # Verify it's now False again
    assert toggled_back_task["id"] == task_id
    assert toggled_back_task["completed"] == False


def test_api_contract_error_responses(client: TestClient):
    """Test that error responses follow the expected contract."""
    # Test invalid user ID format
    response = client.get("/api/v1/invalid-user-id/tasks")
    assert response.status_code == 400
    error_data = response.json()
    assert "detail" in error_data

    # Test non-existent task access
    # First create a user
    register_data = {
        "email": "errorcontract@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Login to get token
    login_data = {
        "email": "errorcontract@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Try to access non-existent task
    response = client.get(
        f"/api/v1/{user_id}/tasks/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data