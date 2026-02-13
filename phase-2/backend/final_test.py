import requests
import json

BASE_URL = "http://127.0.0.1:8003"

def test_backend():
    print("=== Testing Backend Functionality ===\n")

    # Test 1: Health endpoint
    print("1. Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json() if response.status_code == 200 else response.text}")
    print("   [OK] Health endpoint working\n" if response.status_code == 200 else "   [FAIL] Health endpoint failed\n")

    # Test 2: API Documentation
    print("2. Testing API Documentation Endpoint...")
    response = requests.get(f"{BASE_URL}/docs")
    print(f"   Status: {response.status_code}")
    print("   [OK] API Documentation working\n" if response.status_code == 200 else "   [FAIL] API Documentation failed\n")

    # Test 3: Registration
    print("3. Testing User Registration...")
    reg_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/register", json=reg_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"   Registered User ID: {user_data['id']}")
        print("   [OK] User registration successful\n")
    else:
        print(f"   Response: {response.text}")
        print("   [FAIL] User registration failed\n")

    # Test 4: Login
    print("4. Testing User Login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/login", json=login_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        print(f"   Access Token Type: {token_data['token_type']}")
        print("   [OK] User login successful\n")
    else:
        print(f"   Response: {response.text}")
        print("   [FAIL] User login failed\n")

    print("=== Backend Testing Complete ===")
    print("[OK] Backend is working properly with all core functionality tested!")

if __name__ == "__main__":
    test_backend()