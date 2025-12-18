#!/usr/bin/env sh
set -eu

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  echo "Waiting for database..."
  python - <<'PY'
import os, time
from sqlalchemy import create_engine

url = os.environ.get("DATABASE_URL")
if not url:
    raise SystemExit("DATABASE_URL is not set")

engine = create_engine(url, pool_pre_ping=True)
deadline = time.time() + 60
while True:
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        break
    except Exception:
        if time.time() > deadline:
            raise
        time.sleep(2)
print("Database is ready.")
PY

  echo "Applying migrations..."
  flask --app email_marketing_backend.app db upgrade
  echo "Seeding IAM..."
  flask --app email_marketing_backend.app seed-iam
fi

exec "$@"
