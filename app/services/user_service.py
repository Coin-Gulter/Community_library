from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import base as user_model
from app.schemas import user as user_schema
from app.core.security import get_password_hash


def create_user(db: Session, user: user_schema.UserCreate):
    """
    Handles the business logic for creating a new user.
    """
    # Check if a user with that email already exists
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password and create the new user object
    hashed_password = get_password_hash(user.password)
    new_user = user_model.User(
        email=user.email,
        hashed_password=hashed_password,
        is_staff=False  # New registrations are always non-staff
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
