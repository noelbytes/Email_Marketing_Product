from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask
from flask import request
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import settings
from .extensions import cors, db, migrate
from .api.routes import api_bp
from .api.auth import auth_bp
from . import db as _models  # noqa: F401  # ensure models register with SQLAlchemy
from .cli import register_cli
from .errors import register_error_handlers
from .api.authz import authenticate_request


def create_app() -> Flask:
    app = Flask(__name__)
    is_sqlite = settings.database_url.startswith("sqlite")
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        SQLALCHEMY_DATABASE_URI=settings.database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS=(
            {}
            if is_sqlite
            else {
                "pool_pre_ping": True,
                "pool_size": settings.db_pool_size,
                "max_overflow": settings.db_max_overflow,
                "pool_timeout": settings.db_pool_timeout,
            }
        ),
        CELERY=dict(broker_url=settings.celery_broker_url, result_backend=settings.celery_result_backend),
        API_VERSION=settings.version,
        API_KEYS=settings.api_keys,
        TOKEN_TTL_MINUTES=settings.token_ttl_minutes,
        LOG_LEVEL=settings.log_level,
        SMTP_HOST=settings.smtp_host,
        SMTP_PORT=settings.smtp_port,
        SMTP_USERNAME=settings.smtp_username,
        SMTP_PASSWORD=settings.smtp_password,
        SMTP_USE_TLS=settings.smtp_use_tls,
        SMTP_FROM_EMAIL=settings.smtp_from_email,
    )

    cors.init_app(app, resources={r"/api/*": {"origins": settings.cors_origins}})
    db.init_app(app)
    migrate.init_app(app, db)
    register_cli(app)
    register_error_handlers(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    from .api.templates import templates_bp
    app.register_blueprint(templates_bp, url_prefix="/api/templates")
    from .api.campaigns import campaigns_bp
    app.register_blueprint(campaigns_bp, url_prefix="/api/campaigns")

    @app.before_request
    def auth_gate():
        if request.method == "OPTIONS":
            return
        if not request.path.startswith("/api"):
            return
        if request.path in ("/api/healthz", "/api/auth/login", "/api/auth/register"):
            return
        authenticate_request()

    @app.get("/healthz")
    def root_healthz():
        return {
            "status": "ok",
            "service": "api-gateway",
            "version": settings.version,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }

    return app
