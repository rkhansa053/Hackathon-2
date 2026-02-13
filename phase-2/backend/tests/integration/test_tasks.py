"""
Integration tests for task endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from src.models.user import User
from src.models.task import Task
from src.schemas.user import UserCreate
from src.schemas.task import TaskCreate, TaskUpdate
from uuid import UUID


def test_task_crud_operations(client: TestClient):
    """Test complete CRUD operations for tasks."""
    # First register a user
    register_data = {
        "email": "taskuser@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Log in to get token
    login_data = {
        "email": "taskuser@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token_data = login_response.json()
    token = token_data["access_token"]

    # Create a task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
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

    # Get the task
    get_response = client.get(
        f"/api/v1/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["title"] == task_data["title"]

    # Update the task
    update_data = {
        "title": "Updated Test Task",
        "description": "This is an updated test task",
        "completed": True
    }

    update_response = client.put(
        f"/api/v1/{user_id}/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["completed"] == update_data["completed"]

    # Get all tasks for the user
    get_all_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_all_response.status_code == 200
    tasks_list = get_all_response.json()
    assert len(tasks_list) == 1
    assert tasks_list[0]["id"] == task_id

    # Delete the task
    delete_response = client.delete(
        f"/api/v1/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 200

    # Verify the task is gone
    get_deleted_response = client.get(
        f"/api/v1/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_deleted_response.status_code == 404


def test_user_isolation(client: TestClient):
    """Test that users can only access their own tasks."""
    # Register first user
    user1_data = {
        "email": "user1@example.com",
        "password": "securepassword123"
    }

    user1_register = client.post("/api/v1/register", json=user1_data)
    assert user1_register.status_code == 200
    user1 = user1_register.json()
    user1_id = user1["id"]

    # Log in as first user
    login1_data = {
        "email": "user1@example.com",
        "password": "securepassword123"
    }
    login1_response = client.post("/api/v1/login", json=login1_data)
    assert login1_response.status_code == 200
    user1_token = login1_response.json()["access_token"]

    # Register second user
    user2_data = {
        "email": "user2@example.com",
        "password": "securepassword123"
    }

    user2_register = client.post("/api/v1/register", json=user2_data)
    assert user2_register.status_code == 200
    user2 = user2_register.json()
    user2_id = user2["id"]

    # Log in as second user
    login2_data = {
        "email": "user2@example.com",
        "password": "securepassword123"
    }
    login2_response = client.post("/api/v1/login", json=login2_data)
    assert login2_response.status_code == 200
    user2_token = login2_response.json()["access_token"]

    # Create a task for user1
    task_data = {
        "title": "User1's Task",
        "description": "This belongs to user1",
        "completed": False
    }

    create_task_response = client.post(
        f"/api/v1/{user1_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert create_task_response.status_code == 200
    task = create_task_response.json()
    task_id = task["id"]

    # Verify user2 cannot access user1's task
    get_task_as_user2 = client.get(
        f"/api/v1/{user1_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert get_task_as_user2.status_code == 403  # Forbidden

    # Verify user2 can access their own tasks list
    get_user2_tasks = client.get(
        f"/api/v1/{user2_id}/tasks",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert get_user2_tasks.status_code == 200
    assert len(get_user2_tasks.json()) == 0  # User2 has no tasks yet


def test_toggle_task_completion(client: TestClient):
    """Test toggling task completion status."""
    # Register a user
    register_data = {
        "email": "toggleuser@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Log in to get token
    login_data = {
        "email": "toggleuser@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token_data = login_response.json()
    token = token_data["access_token"]

    # Create a task
    task_data = {
        "title": "Toggle Task",
        "description": "This task will be toggled",
        "completed": False
    }

    create_response = client.post(
        f"/api/v1/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 200
    task = create_response.json()
    task_id = task["id"]

    # Toggle completion status
    toggle_response = client.patch(
        f"/api/v1/{user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["completed"] == True

    # Toggle again to set to incomplete
    toggle_response2 = client.patch(
        f"/api/v1/{user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert toggle_response2.status_code == 200
    toggled_task2 = toggle_response2.json()
    assert toggled_task2["completed"] == False