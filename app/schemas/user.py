from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_staff: bool

    class Config:
        orm_mode = True  # In Pydantic v2, use from_attributes = True
