from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import datetime

from app.models import book as book_model, user as user_model, borrowing as borrowing_model
from app.schemas import book as book_schema


def create_book(db: Session, book: book_schema.BookCreate, user: user_model.User):
    """Registers a new book. Only accessible by staff."""
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to register new books."
        )
    db_book = book_model.Book(
        title=book.title,
        author=book.author,
        total_copies=book.total_copies,
        available_copies=book.total_copies
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def borrow_book(db: Session, book_id: int, member: user_model.User):
    """Borrows a book for a member."""
    db_book = db.query(book_model.Book).filter(book_model.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if db_book.available_copies < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No available copies")

    # Decrement copy count
    db_book.available_copies -= 1

    # Create borrowing record
    due_date = datetime.datetime.utcnow() + datetime.timedelta(days=14)
    db_borrowing = borrowing_model.Borrowing(
        book_id=book_id,
        member_id=member.id,
        due_date=due_date
    )
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


def return_book(db: Session, borrowing_id: int, member: user_model.User):
    """Returns a borrowed book."""
    db_borrowing = db.query(borrowing_model.Borrowing).filter(
        borrowing_model.Borrowing.id == borrowing_id
    ).first()

    if not db_borrowing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing record not found")

    if db_borrowing.member_id != member.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You did not borrow this book")

    if db_borrowing.is_returned:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book has already been returned")

    # Mark as returned
    db_borrowing.is_returned = True
    db_borrowing.return_date = datetime.datetime.utcnow()

    # Increment copy count
    db_borrowing.book.available_copies += 1

    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


def get_member_borrowed_books(db: Session, member: user_model.User):
    """Gets all currently borrowed books for a specific member."""
    return db.query(borrowing_model.Borrowing).filter(
        borrowing_model.Borrowing.member_id == member.id,
        borrowing_model.Borrowing.is_returned == False
    ).all()
