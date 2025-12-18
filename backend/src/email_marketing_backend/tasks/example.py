from __future__ import annotations

from celery import shared_task


@shared_task(name="tasks.log_heartbeat")
def log_heartbeat() -> str:
    message = "heartbeat"
    print(message)
    return message
