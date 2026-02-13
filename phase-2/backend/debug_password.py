from src.utils.security import get_password_hash

def test_password_hash():
    try:
        # Test with a very short password
        password = "pass"
        print(f"Testing password hash with: {password}")

        hashed = get_password_hash(password)
        print(f"Success! Hashed password: {hashed[:50]}...")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_hash()