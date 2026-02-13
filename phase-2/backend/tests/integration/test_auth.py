"""
Integration tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.user import User
from src.schemas.user import UserCreate
from src.services.auth_service import AuthService
from src.config.database import get_async_session
from unittest.mock import AsyncMock


def test_register_user(client: TestClient):
    """Test user registration endpoint."""
    user_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/v1/register", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == user_data["email"]
    assert "hashed_password" not in data  # Should not expose hashed password


def test_register_user_duplicate_email(client: TestClient):
    """Test user registration with duplicate email."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "securepassword123"
    }

    # Register the first user
    response1 = client.post("/api/v1/register", json=user_data)
    assert response1.status_code == 200

    # Try to register with the same email
    response2 = client.post("/api/v1/register", json=user_data)
    assert response2.status_code == 400


def test_login_user_success(client: TestClient):
    """Test successful user login."""
    # First register a user
    register_data = {
        "email": "login@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200

    # Now try to log in
    login_data = {
        "email": "login@example.com",
        "password": "securepassword123"
    }

    login_response = client.post("/api/v1/login", json=login_data)

    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    # First register a user
    register_data = {
        "email": "invalid@example.com",
        "password": "securepassword123"
    }

    register_response = client.post("/api/v1/register", json=register_data)
    assert register_response.status_code == 200

    # Try to log in with wrong password
    login_data = {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }

    login_response = client.post("/api/v1/login", json=login_data)

    assert login_response.status_code == 401