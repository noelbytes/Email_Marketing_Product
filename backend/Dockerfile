FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY src ./src
COPY migrations ./migrations
COPY entrypoint.sh ./entrypoint.sh
COPY gunicorn.conf.py ./gunicorn.conf.py

RUN pip install --upgrade pip && pip install -e ".[dev]" && chmod +x /app/entrypoint.sh

ENV FLASK_APP=email_marketing_backend.app

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
