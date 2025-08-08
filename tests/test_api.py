from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.services.user_service import create_user
from app.schemas.user import UserCreate
from tests.utils import random_email, random_lower_string


def test_user_registration_and_login(client: TestClient, db: Session):
    """
    Tests that a user can be created via the registration endpoint
    and then successfully log in.
    """
    email = random_email()
    password = random_lower_string()

    # Step 1: Register the user via the API endpoint
    register_response = client.post("/users/register", json={"email": email, "password": password})
    assert register_response.status_code == 201
    assert register_response.json()["email"] == email

    # Step 2: Log in with the newly created user
    login_data = {"username": email, "password": password}
    login_response = client.post("/auth/token", data=login_data)

    # Assert that the login is successful
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_staff_can_create_book(client: TestClient, db: Session):
    """
    Tests that a user with staff privileges can create a book.
    """
    # Step 1: Create a staff user directly in the database for this test
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = create_user(db, user=user_in)
    user.is_staff = True
    db.commit()

    # Step 2: Log in as the staff user to get a token
    login_data = {"username": email, "password": password}
    login_response = client.post("/auth/token", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Use the token to perform the staff-only action
    book_data = {"title": "Admin Book", "author": "Admin Author"}
    create_book_response = client.post("/api/books", headers=headers, json=book_data)
    assert create_book_response.status_code == 201
    assert create_book_response.json()["title"] == "Admin Book"


def test_member_cannot_create_book(client: TestClient, db: Session):
    """
    Tests that a regular user without staff privileges cannot create a book.
    """
    # Step 1: Create a regular member user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    create_user(db, user=user_in)

    # Step 2: Log in as the member to get a token
    login_data = {"username": email, "password": password}
    login_response = client.post("/auth/token", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Attempt the staff-only action, which should be forbidden
    book_data = {"title": "Member Book", "author": "Member Author"}
    create_book_response = client.post("/api/books", headers=headers, json=book_data)
    assert create_book_response.status_code == 403
