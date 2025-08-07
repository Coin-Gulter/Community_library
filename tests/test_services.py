# This file tests the core business logic in the services layer.

import pytest
from sqlalchemy.orm import Session
from app.services import library_service
from app.schemas.book import BookCreate
from app.models.user import User


def test_create_book_by_staff(db: Session):
    """
    Tests that a staff member can successfully create a new book.
    """
    staff_user = User(email="staff@example.com", hashed_password="fake_password_hash", is_staff=True)
    book_schema = BookCreate(title="The Great Gatsby", author="F. Scott Fitzgerald", total_copies=5)

    book = library_service.create_book(db=db, book=book_schema, user=staff_user)

    assert book is not None
    assert book.title == "The Great Gatsby"
    assert book.available_copies == 5
    assert book.total_copies == 5


def test_create_book_by_non_staff_fails(db: Session):
    """
    Tests that a non-staff member cannot create a book, expecting a 403 Forbidden error.
    """
    from fastapi import HTTPException

    non_staff_user = User(email="member@example.com", hashed_password="fake_password_hash", is_staff=False)
    book_schema = BookCreate(title="1984", author="George Orwell")

    with pytest.raises(HTTPException) as excinfo:
        library_service.create_book(db=db, book=book_schema, user=non_staff_user)

    assert excinfo.value.status_code == 403
