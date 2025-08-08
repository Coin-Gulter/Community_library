import argparse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.base import User
from app.core.security import get_password_hash


def create_staff_user(db: Session, email: str, password: str):
    """Creates a new staff user in the database."""
    # Check if user already exists
    if db.query(User).filter(User.email == email).first():
        print(f"Error: User with email {email} already exists.")
        return

    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        is_staff=True  # The key difference: set is_staff to True
    )
    db.add(db_user)
    db.commit()
    print(f"Successfully created staff user: {email}")


if __name__ == "__main__":
    # Set up argument parser to accept email and password from the command line
    parser = argparse.ArgumentParser(description="Create a new staff user.")
    parser.add_argument("--email", type=str, required=True, help="Email address for the new staff user.")
    parser.add_argument("--password", type=str, required=True, help="Password for the new staff user.")

    args = parser.parse_args()

    db = SessionLocal()
    try:
        create_staff_user(db, email=args.email, password=args.password)
    finally:
        db.close()
