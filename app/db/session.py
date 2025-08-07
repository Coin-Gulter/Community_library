from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine using the database URL from settings
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function to get a database session.
    Ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
