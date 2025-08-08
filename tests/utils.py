import random
import string
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.base import User
from app.schemas.user import UserCreate


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_random_user(db: Session, is_staff: bool = False) -> User:
    """Creates a random user in the database."""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_staff=is_staff
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
