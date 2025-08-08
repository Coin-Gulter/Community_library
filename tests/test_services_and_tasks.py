import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services import library_service, user_service
from app.schemas.book import BookCreate
from app.schemas.user import UserCreate
from app.tasks import email_tasks
from tests.utils import create_random_user


# --- User Service Tests ---
def test_create_user(db: Session):
    user_in = UserCreate(email="test@example.com", password="password123")
    user = user_service.create_user(db, user=user_in)
    assert user.email == user_in.email


def test_create_existing_user_fails(db: Session):
    user_in = UserCreate(email="test@example.com", password="password123")
    user_service.create_user(db, user=user_in)
    with pytest.raises(HTTPException):
        user_service.create_user(db, user=user_in)


# --- Library Service Tests ---
def test_create_book_by_staff(db: Session):
    staff_user = create_random_user(db, is_staff=True)
    book_in = BookCreate(title="Test Book", author="Test Author")
    book = library_service.create_book(db, book=book_in, user=staff_user)
    assert book.title == "Test Book"


def test_create_book_by_member_fails(db: Session):
    member_user = create_random_user(db, is_staff=False)
    book_in = BookCreate(title="Another Book", author="Another Author")
    with pytest.raises(HTTPException):
        library_service.create_book(db, book=book_in, user=member_user)


# --- Celery Task Tests ---
def test_send_borrow_email_task(mocker):
    """Test the borrow confirmation email task, mocking the actual email sending."""
    mock_send_email = mocker.patch("app.tasks.email_tasks.send_email")

    member_email = "member@test.com"
    book_title = "The Hitchhiker's Guide"
    due_date = "2025-01-01"

    # Call the task that internally calls send_email
    email_tasks.send_borrow_confirmation_email(member_email, book_title, due_date)

    # Assert that our mock was called exactly once with the correct arguments
    mock_send_email.assert_called_once()
    call_args = mock_send_email.call_args[1]
    assert call_args["to_email"] == member_email
