from app.tasks.celery_app import celery
from app.core.email import send_email
from app.db.session import SessionLocal
from app.models.base import Borrowing
import datetime


@celery.task
def send_borrow_confirmation_email(member_email: str, book_title: str, due_date: str):
    """
    Celery task to send an email notification when a book is borrowed.
    """
    subject = "Book Borrowing Confirmation"
    body = (
        f"Dear Member,\n\n"
        f"You have successfully borrowed the book '{book_title}'.\n"
        f"Please return it by {due_date}.\n\n"
        f"Thank you,\nThe Community Library"
    )
    send_email(to_email=member_email, subject=subject, body=body)


@celery.task
def send_return_confirmation_email(member_email: str, book_title: str):
    """
    Celery task to send an email notification when a book is returned.
    """
    subject = "Book Return Confirmation"
    body = (
        f"Dear Member,\n\n"
        f"You have successfully returned the book '{book_title}'.\n\n"
        f"Thank you for returning it on time!\nThe Community Library"
    )
    send_email(to_email=member_email, subject=subject, body=body)


@celery.task
def send_single_overdue_email(member_email: str, book_title: str, due_date: str):
    """
    Sub-task to send a single overdue notification email.
    """
    subject = "Overdue Book Reminder"
    body = (
        f"Dear Member,\n\n"
        f"This is a reminder that the book '{book_title}' was due on {due_date}.\n"
        f"Please return it as soon as possible to avoid further penalties.\n\n"
        f"Thank you,\nThe Community Library"
    )
    send_email(to_email=member_email, subject=subject, body=body)


@celery.task
def send_overdue_book_notifications():
    """
    Scheduled task to find all overdue books and trigger notification emails.
    This task is run by Celery Beat.
    """
    db = SessionLocal()
    try:
        overdue_records = db.query(Borrowing).filter(
            Borrowing.due_date < datetime.datetime.utcnow(),
            Borrowing.is_returned == False
        ).all()

        for record in overdue_records:
            # Trigger a separate task for each email to distribute the load
            send_single_overdue_email.delay(
                member_email=record.member.email,
                book_title=record.book.title,
                due_date=record.due_date.strftime("%Y-%m-%d")
            )
        return f"Found and processed {len(overdue_records)} overdue records."
    finally:
        db.close()
