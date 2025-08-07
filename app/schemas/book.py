from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str


class BookCreate(BookBase):
    total_copies: int = 1


class Book(BookBase):
    id: int
    available_copies: int

    class Config:
        from_attributes = True
