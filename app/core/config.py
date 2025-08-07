from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Manages application settings loaded from environment variables.
    """
    # Database configuration
    DATABASE_URL: str

    # JWT Authentication settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Celery configuration
    CELERY_BROKER_URL: str = "redis://broker:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://broker:6379/0"

    class Config:
        # Specifies the file to load environment variables from
        env_file = ".env"


# Create a single, reusable instance of the settings
settings = Settings("./.env")
