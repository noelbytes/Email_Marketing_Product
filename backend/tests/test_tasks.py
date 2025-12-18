from __future__ import annotations

from email_marketing_backend.celery_app import celery, health_check
from email_marketing_backend.tasks import log_heartbeat


def test_celery_tasks_run_in_eager_mode():
    celery.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
        broker_url="memory://",
        result_backend="cache+memory://",
    )

    result = health_check.delay()
    assert result.get() == "ok"

    heartbeat_result = log_heartbeat.delay()
    assert heartbeat_result.get() == "heartbeat"
