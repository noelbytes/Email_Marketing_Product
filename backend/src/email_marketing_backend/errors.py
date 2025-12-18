from __future__ import annotations

import logging

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        payload = {
            "error": {
                "message": exc.description if exc.description else exc.name,
                "code": exc.code,
            }
        }
        return jsonify(payload), exc.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(exc: Exception):
        logger.exception("Unhandled exception", exc_info=exc)
        payload = {"error": {"message": "Internal server error", "code": 500}}
        return jsonify(payload), 500

