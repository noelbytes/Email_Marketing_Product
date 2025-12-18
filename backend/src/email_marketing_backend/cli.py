from __future__ import annotations

import click

from .services.iam import seed_iam


def register_cli(app):
    @app.cli.command("seed-iam")
    def seed_iam_command():
        """Seed default permissions and roles."""
        seed_iam()
        click.echo("IAM roles and permissions seeded.")
