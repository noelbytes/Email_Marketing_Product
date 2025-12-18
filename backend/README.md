# Backend (Flask)

Flask 3.x service that powers the API, data models, and Celery task orchestration.

## Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
flask seed-iam
flask --app email_marketing_backend.app run --debug
```

Run the worker:

```bash
celery -A email_marketing_backend.celery_app worker -l info
```

## Scripts

- `pytest` – run unit tests.
- `ruff check` / `ruff format` – lint/format.
- `flask db upgrade` – run migrations.
- `flask seed-iam` – seed default roles/permissions.

## Environment

Environment variables live in `.env` and include database, redis, and secret settings. For local Compose use the provided `.env.example`.

Authenticated API requests should prefer `Authorization: Bearer <token>` (register via `/api/auth/register`, then `/api/auth/login`). The legacy `X-API-Key` header still works for service-to-service traffic.

## Local SMTP (Mailhog)

When running via Docker Compose, SMTP defaults to `mailhog:1025`. Use `POST /api/templates/<id>/send-test` to send a preview email and view it at `http://localhost:8025`.
