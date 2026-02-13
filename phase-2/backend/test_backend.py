import asyncio
import traceback
from src.main import app
from src.config.database import init_db
from fastapi.testclient import TestClient

def test_backend():
    print("Testing backend functionality...")

    try:
        # Test importing and initializing the app
        print("[OK] Application imported successfully")

        # Test database initialization
        print("Initializing database...")
        asyncio.run(init_db())
        print("[OK] Database initialized successfully")

        # Create test client
        client = TestClient(app)
        print("[OK] Test client created successfully")

        # Test health endpoint
        print("Testing health endpoint...")
        response = client.get("/health")
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            print("[OK] Health endpoint working correctly")
        else:
            print("[FAIL] Health endpoint failed")

        # Test API endpoints
        print("\nTesting API endpoints...")
        response = client.get("/docs")
        print(f"Docs endpoint status: {response.status_code}")

        response = client.get("/api/v1/tasks/nonexistent_user/tasks")
        print(f"Tasks endpoint status: {response.status_code}")

    except Exception as e:
        print(f"[FAIL] Error occurred: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_backend()