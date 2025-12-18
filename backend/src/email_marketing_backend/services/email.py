from __future__ import annotations

import smtplib
from email.message import EmailMessage

from flask import current_app


def send_html_email(*, to_email: str, subject: str, html: str) -> None:
    host = current_app.config.get("SMTP_HOST", "mailhog")
    port = int(current_app.config.get("SMTP_PORT", 1025))
    username = current_app.config.get("SMTP_USERNAME")
    password = current_app.config.get("SMTP_PASSWORD")
    use_tls = bool(current_app.config.get("SMTP_USE_TLS", False))
    from_email = current_app.config.get("SMTP_FROM_EMAIL", "no-reply@constellation.local")

    msg = EmailMessage()
    msg["To"] = to_email
    msg["From"] = from_email
    msg["Subject"] = subject
    msg.set_content("This message contains HTML. Please view in an HTML-capable client.")
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(host, port, timeout=15) as client:
        if use_tls:
            client.starttls()
        if username and password:
            client.login(username, password)
        client.send_message(msg)
    current_app.logger.info("Sent email to=%s subject=%s via %s:%s", to_email, subject, host, port)
