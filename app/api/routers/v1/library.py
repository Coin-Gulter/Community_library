from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models import base as user_model
from app.schemas import book as book_schema, borrowing as borrowing_schema
from app.services import library_service

router = APIRouter()


@router.post("/books", response_model=book_schema.Book, status_code=status.HTTP_201_CREATED)
def register_new_book(
    book: book_schema.BookCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """Register a new book in the library (staff only)."""
    return library_service.create_book(db=db, book=book, user=current_user)


@router.post("/books/{book_id}/borrow", response_model=borrowing_schema.Borrowing)
def borrow_a_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """Borrow an available book."""
    return library_service.borrow_book(db=db, book_id=book_id, member=current_user)


@router.post("/borrowings/{borrowing_id}/return", response_model=borrowing_schema.Borrowing)
def return_a_book(
    borrowing_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """Return a borrowed book."""
    return library_service.return_book(db=db, borrowing_id=borrowing_id, member=current_user)


@router.get("/members/me/books", response_model=List[borrowing_schema.Borrowing])
def view_my_borrowed_books(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """View all books currently borrowed by the authenticated member."""
    return library_service.get_member_borrowed_books(db=db, member=current_user)
