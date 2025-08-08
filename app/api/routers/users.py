from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import user as user_schema
from app.services import user_service

router = APIRouter()


@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def register_new_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint to register a new member.
    """
    return user_service.create_user(db=db, user=user)
