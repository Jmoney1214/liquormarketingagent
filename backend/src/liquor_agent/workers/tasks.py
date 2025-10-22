"""Celery tasks for background processing"""
from .celery_app import celery_app


@celery_app.task(name="test_task")
def test_task():
    """Test task to verify Celery is working"""
    return "Celery is working!"


# Placeholder for future tasks
# Will be implemented in Sprint 4 (Messaging System)

