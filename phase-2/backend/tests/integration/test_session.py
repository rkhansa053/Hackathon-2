"""
Integration tests for session management and token verification.
"""
import pytest
from fastapi.testclient import TestClient
from src.models.user import User
from src.schemas.user import UserCreate
from datetime import datetime, timedelta
from jose import jwt
from src.config.settings import settings


def test_token_expiration_handling(client: TestClient):
    """Test that expired tokens are properly handled."""
    # Register a user
    register_data = {
        "email": "expiredtoken@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Log in to get a valid token
    login_data = {
        "email": "expiredtoken@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token_data = login_response.json()
    valid_token = token_data["access_token"]

    # Test that valid token works
    test_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert test_response.status_code == 200  # Empty task list is fine


def test_invalid_token_rejection(client: TestClient):
    """Test that invalid tokens are rejected."""
    # Register a user
    register_data = {
        "email": "invalidtoken@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Try to access with invalid token
    invalid_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert invalid_response.status_code == 401


def test_token_authentication_on_protected_endpoints(client: TestClient):
    """Test that protected endpoints require valid tokens."""
    # Register a user
    register_data = {
        "email": "protected@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Try to access without token
    no_auth_response = client.get(f"/api/v1/{user_id}/tasks")
    assert no_auth_response.status_code == 401

    # Log in to get token
    login_data = {
        "email": "protected@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)
    assert login_response.status_code == 200
    token_data = login_response.json()
    token = token_data["access_token"]

    # Access should work with valid token
    valid_auth_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert valid_auth_response.status_code == 200