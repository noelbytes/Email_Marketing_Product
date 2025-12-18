from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sqlalchemy.orm import Session

from ..db.models import Permission, Role, User
from ..extensions import db


DEFAULT_PERMISSIONS = {
    "journeys.build": "Create and edit automation journeys",
    "journeys.publish": "Publish journeys to production audiences",
    "journeys.analyze": "View journey analytics",
    "templates.manage": "Create and manage email templates",
    "emails.send_test": "Send test emails from templates",
    "campaigns.manage": "Create and manage campaigns",
    "campaigns.send": "Send campaigns to audiences",
    "deliverability.view": "Access deliverability dashboards",
    "deliverability.remediate": "Run remediation workflows",
    "compliance.manage": "Manage compliance center settings",
    "compliance.dsar": "Action DSAR requests",
    "data.integrations.manage": "Manage integrations and API keys",
    "iam.manage": "Invite users and manage IAM settings",
    "users.invite": "Invite or deactivate platform users",
}

DEFAULT_ROLES = {
    "org-admin": [
        "iam.manage",
        "users.invite",
        "journeys.publish",
        "journeys.build",
        "templates.manage",
        "emails.send_test",
        "campaigns.manage",
        "campaigns.send",
        "deliverability.view",
        "deliverability.remediate",
        "compliance.manage",
        "compliance.dsar",
        "data.integrations.manage",
    ],
    "journey-architect": [
        "journeys.build",
        "journeys.publish",
        "journeys.analyze",
        "templates.manage",
        "emails.send_test",
        "campaigns.manage",
        "campaigns.send",
    ],
    "deliverability-analyst": ["deliverability.view", "deliverability.remediate"],
    "privacy-officer": ["compliance.manage", "compliance.dsar"],
}


def seed_iam(session: Session | None = None) -> None:
    session = session or db.session
    name_to_perm: dict[str, Permission] = {}
    for perm_name, desc in DEFAULT_PERMISSIONS.items():
        permission = session.query(Permission).filter_by(name=perm_name).first()
        if not permission:
            permission = Permission(name=perm_name, description=desc)
            session.add(permission)
        name_to_perm[perm_name] = permission

    for role_name, perm_names in DEFAULT_ROLES.items():
        role = session.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            session.add(role)
        role.permissions = [name_to_perm[name] for name in perm_names]

    session.commit()


def assign_roles(user: User, role_names: Iterable[str], session: Session | None = None) -> None:
    session = session or db.session
    roles = (
        session.query(Role)
        .filter(Role.name.in_(list(role_names)))
        .all()
    )
    user.roles = roles
    session.add(user)
    session.commit()


def list_permissions_for_user(user: User) -> list[str]:
    perms = {perm.name for role in user.roles for perm in role.permissions}
    return sorted(perms)
