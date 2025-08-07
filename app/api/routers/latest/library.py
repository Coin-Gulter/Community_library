from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models import user as user_model
from app.schemas import book as book_schema, borrowing as borrowing_schema
from app.services import library_service

from app.tasks.email_tasks import send_borrow_confirmation_email, send_return_confirmation_email

router = APIRouter()


@router.post("/books", response_model=book_schema.Book, status_code=status.HTTP_201_CREATED)
def register_new_book_latest(
    book: book_schema.BookCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """Register a new book in the library (staff only)."""
    return library_service.create_book(db=db, book=book, user=current_user)


@router.post("/books/{book_id}/borrow", response_model=borrowing_schema.Borrowing)
def borrow_a_book_latest(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """Borrow an available book and send an email notification."""
    borrowing_record = library_service.borrow_book(db=db, book_id=book_id, member=current_user)

    # Trigger the Celery task to send an email in the background
    # This call is ONLY present in the 'latest' version.
    send_borrow_confirmation_email.delay(
        member_email=current_user.email,
        book_title=borrowing_record.book.title,
        due_date=borrowing_record.due_date.strftime("%Y-%m-%d")
    )

    return borrowing_record


@router.post("/borrowings/{borrowing_id}/return", response_model=borrowing_schema.Borrowing)
def return_a_book_latest(
    borrowing_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """Return a borrowed book and send an email notification."""
    borrowing_record = library_service.return_book(db=db, borrowing_id=borrowing_id, member=current_user)

    # Trigger the Celery task to send an email in the background
    # This call is ONLY present in the 'latest' version.
    send_return_confirmation_email.delay(
        member_email=current_user.email,
        book_title=borrowing_record.book.title
    )

    return borrowing_record


@router.get("/members/me/books", response_model=List[borrowing_schema.Borrowing])
def view_my_borrowed_books_latest(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """View all books currently borrowed by the authenticated member."""
    return library_service.get_member_borrowed_books(db=db, member=current_user)
