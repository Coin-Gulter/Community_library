from celery import Celery
from app.core.config import settings

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.email_tasks"]
)

# Add the Celery Beat schedule
celery.conf.beat_schedule = {
    'notify-overdue-books-every-day': {
        'task': 'app.tasks.email_tasks.send_overdue_book_notifications',
        'schedule': 86400.0,  # Run every 24 hours (in seconds)
    },
}

celery.conf.timezone = 'UTC'
