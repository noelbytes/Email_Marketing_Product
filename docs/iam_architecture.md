# Identity & Access Architecture

## Objectives

- Enforce least-privilege access with composable roles across marketing, engineering, and compliance personas.
- Support enterprise requirements: SSO (SAML/OIDC), SCIM provisioning, audit trails, and consent-aware data boundaries.
- Provide API-first IAM so customers can automate provisioning and policy enforcement.

## Model

### Core entities

| Entity | Description |
| --- | --- |
| `Organization` | Tenant boundary; controls policies, data residency, legal holds. |
| `User` | Person with profile, MFA state, authentication method links. |
| `Role` | Named bundle of permissions (e.g., `org-admin`, `journey-architect`, `analyst-readonly`). |
| `Permission` | Atomic capability (e.g., `journeys.publish`, `deliverability.view`, `iam.manage`). |
| `RolePermission` | Many-to-many mapping between roles and permissions. |
| `UserRole` | Assignment of roles to users (scoped globally or to workspace segments). |

### Permission taxonomy

- **Journey Studio** – build, edit, publish workflows (`journeys.*`).
- **Messaging & Deliverability** – domain verification, warm-up, inbox diagnostics (`deliverability.*`).
- **Compliance & Privacy** – DSAR fulfillment, consent exports (`compliance.*`).
- **Data & Integrations** – API keys, webhooks, catalog management (`data.*`).
- **IAM & Security** – invite users, manage roles, configure SSO/SCIM, audit exports (`iam.*`).

### Authentication & Federation

1. **Primary Auth** – email + password with WebAuthn MFA.
2. **SSO Providers** – SAML 2.0, OIDC (Azure AD, Okta, Google Workspace). Organization stores IdP metadata and enforcement policies.
3. **Tokens** – Access tokens are short-lived JWTs signed by our auth service with org + role claims; refresh tokens stored with rotation counter.

### Provisioning & Lifecycle

- **SCIM 2.0** endpoint to sync users/groups from IdPs. SCIM groups map to platform roles.
- **Just-in-Time (JIT) provisioning** optionally allowed for IdP-sourced users.
- **Access Requests** – optional approval flow for joining workspaces, integrated with Slack/Teams bots.

### Enforcement

- Backend blueprints enforce permission requirements via decorators (e.g., `@requires_permission("iam.manage")`).
- Policies cached in Redis with short TTL; invalidated on role updates.
- Audit trail captures `who/what/when/where` for all privileged actions.
- Frontend uses role/permission claims to hide routes/components and drive decisioning.

### Next Steps

1. Implement auth service blueprint (token issuance, refresh, passwordless).
2. Add `/api/iam/roles` and `/api/iam/users` endpoints with CRUD + audit logging.
3. Integrate feature flags (e.g., LaunchDarkly) to gate high-risk actions behind approvals.
4. Build compliance dashboard summarizing IAM posture (MFA adoption, stale accounts, SCIM sync health).
