from __future__ import annotations

import os

from celery import Celery

from . import create_app
from .config import settings

celery = Celery(
    "email_marketing_backend",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["email_marketing_backend.tasks"],
)
celery.conf.update(task_default_queue="default")


@celery.task(name="tasks.health_check")
def health_check() -> str:
    return "ok"


def init_celery(app=None) -> Celery:
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


init_celery()
