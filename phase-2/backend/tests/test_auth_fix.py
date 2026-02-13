import pytest
from fastapi.testclient import TestClient
import uuid

# We need to import app to use with TestClient, but conftest.py likely handles it.
# Assuming pytest detects conftest.py

def test_auth_flow(client):
    # 1. Register
    email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    
    response = client.post(
        "/api/v1/register",
        json={"email": email, "password": password}
    )
    if response.status_code != 200:
        print(f"Registration failed: {response.json()}")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == email
    assert "id" in user_data

    # 2. Login
    response = client.post(
        "/api/v1/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    login_data = response.json()
    assert "access_token" in login_data
    assert "refresh_token" in login_data
    assert ":" in login_data["refresh_token"] # Verify our fix for composite token

    access_token = login_data["access_token"]
    refresh_token = login_data["refresh_token"]

    # 3. Refresh
    response = client.post(
        "/api/v1/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    refresh_data = response.json()
    assert "access_token" in refresh_data
    
    # 4. Login with wrong password
    response = client.post(
        "/api/v1/login",
        json={"email": email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
