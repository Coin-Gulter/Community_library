import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.db.session import get_db
from app.models.base import Base

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Fixture to provide a clean database session for each test function.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        # Drop all tables after the test is done
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator:
    """
    Fixture to provide a TestClient that uses the same db session as the test.
    """
    def override_get_db():
        """Dependency override."""
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
