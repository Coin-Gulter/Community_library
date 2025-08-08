from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str


class User(UserBase):
    """Schema for returning user data."""
    id: int
    is_staff: bool

    class Config:
        from_attributes = True
