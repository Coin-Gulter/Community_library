import logging
from app.db.session import engine
from app.models.base import Base 

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Creates all database tables based on the SQLAlchemy models.
    """
    try:
        logger.info("Creating all database tables...")
        # The main command to create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"An error occurred while creating tables: {e}")
        raise

if __name__ == "__main__":
    init_db()

