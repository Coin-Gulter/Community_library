# This file defines the base class for all your models.
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_staff = Column(Boolean, default=False)

    borrowings = relationship("Borrowing", back_populates="member")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)

    borrowings = relationship("Borrowing", back_populates="book")


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)

    book = relationship("Book", back_populates="borrowings")
    member = relationship("User", back_populates="borrowings")
