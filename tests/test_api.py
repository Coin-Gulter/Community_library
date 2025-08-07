# This file tests the API endpoints themselves.

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """
    Tests the root endpoint to ensure the API is running.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Community Library API"}

# Add more tests here for login, borrowing, returning, etc.,
# using the TestClient to simulate real API calls.
