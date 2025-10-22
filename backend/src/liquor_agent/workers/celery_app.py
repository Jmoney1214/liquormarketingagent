"""Celery application for background tasks"""
from celery import Celery
from ..core.config import settings

# Create Celery app
celery_app = Celery(
    "liquor_agent",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Auto-discover tasks from the tasks module
celery_app.autodiscover_tasks(["liquor_agent.workers"])

if __name__ == "__main__":
    celery_app.start()

