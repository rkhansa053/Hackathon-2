import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API."""
    with TestClient(app, base_url="http://localhost") as test_client:
        yield test_client