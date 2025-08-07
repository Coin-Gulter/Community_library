import datetime
from pydantic import BaseModel
from .book import Book


class Borrowing(BaseModel):
    id: int
    borrow_date: datetime.datetime
    due_date: datetime.datetime
    book: Book

    class Config:
        from_attributes = True
