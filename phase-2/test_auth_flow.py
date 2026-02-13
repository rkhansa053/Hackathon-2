import httpx
import asyncio
import uuid

async def test_register_and_login():
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    
    # Increase timeout to 60 seconds
    timeout = httpx.Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Register
        print(f"Registering {email}...")
        try:
            reg_response = await client.post(
                "http://localhost:8000/api/v1/register",
                json={"email": email, "password": password}
            )
            print(f"Register Status: {reg_response.status_code}")
            print(f"Register Response: {reg_response.text}")
            
            if reg_response.status_code != 200:
                return

            # Login
            print(f"Logging in {email}...")
            login_response = await client.post(
                "http://localhost:8000/api/v1/login",
                json={"email": email, "password": password}
            )
            print(f"Login Status: {login_response.status_code}")
            print(f"Login Response: {login_response.text}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_register_and_login())