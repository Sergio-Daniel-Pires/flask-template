# Security

This project is a demo starter for fast iteration. This document records what
has been fixed and what has been **consciously accepted** (ACK).

## Applied baseline

- `FLASK_ENV` is validated against `development`, `test`, and `production`;
  unknown values fail instead of silently falling back to development.
- Production requires `FLASK_SECRET_KEY` with at least 32 characters and rejects
  placeholders such as `change-me`.
- Request bodies are limited to 1 MiB; echo is limited to 10,000 characters and
  notes to 500 characters.
- The container publishes its port only on `127.0.0.1`; TLS and rate limiting
  live in nginx/proxy.
- Basic headers: `X-Content-Type-Options`, `X-Frame-Options`, and
  `Referrer-Policy`.
- SQLAlchemy/ORM, with no string-concatenated SQL. React escapes note content.
- Docker runs as a non-root user; the VPS setup generates `.env` with a random
  secret and applies `chmod 600`.

## Accepted risks (ACK)

| ID | Item | Decision | Reason | Current mitigation | Revisit when |
| --- | --- | --- | --- | --- | --- |
| ACK-001 | Rate limiting | Outside the app; nginx/proxy responsibility. | Avoids a dependency and complexity in the starter. | Port bound to `127.0.0.1`; proxy in front. | If the proxy is removed or the app is exposed directly. |
| ACK-002 | SSH deploy as `root` | Accepted; it is machine configuration and will not change here. | The VPS environment already works this way. | Dedicated key, `VPS_SSH_KEY` in secrets, fingerprint when configured. | If the VPS allows a deploy user with Docker access. |
| ACK-003 | Public notes API | Accepted for the demo. | The starter has no identity layer. | Do not store personal or sensitive data; use locally or for demos. | Before any real use or third-party data. |
| ACK-004 | TLS | Outside the app; terminated at nginx/proxy. | The package should not embed a proxy. | Container is not exposed directly. | Before public internet access. |
| ACK-005 | Public Swagger | Accepted for the demo. | Helps inspect the API during the interview. | No privileged writes; endpoints are examples. | In real production, protect or disable `/api/docs`. |
| ACK-006 | CSP/HSTS | Delegated to nginx/proxy. | CSP needs the domain and proxy asset policy. | Basic headers in Flask. | When configuring the domain and TLS. |
| ACK-007 | GitHub Actions by tag | Accepted in the template. | Automatic security updates are desirable. | `permissions: contents: read`; isolated secrets. | In a high-assurance repository, pin by SHA. |
| ACK-008 | Docker via `curl \| sh` | Accepted for VPS bootstrap. | Fast setup for a demo machine. | Script runs once during initial setup. | In a hardened environment, use a package or verified checksum. |
| ACK-009 | Docker uses `pip`, not `uv.lock` | Accepted for simplicity. | The starter prioritizes fast iteration. | Dependencies have ranges in `pyproject.toml`. | When strict reproducibility is required. |
| ACK-010 | Notes without pagination | Accepted for the demo. | Small volume, no real users. | Limit of 500 characters per note. | Before data volume grows. |
| ACK-011 | No authentication/identity | Out of scope for the starter. | Fast interview setup, no real data. | Do not store PII; the API is an example. | Before any user-data feature. |
| ACK-012 | Optional SSH fingerprint | Accepted for the demo. | Not every VPS has the secret configured initially. | `VPS_FINGERPRINT` is documented; configure it for real deploys. | Before any production deployment. |

## How to add a new ACK

When you decide not to fix a finding, add a row to the table above with:

- sequential ID;
- item and affected file/route;
- reason for the decision;
- current mitigation;
- trigger to revisit.

Security findings **must not be silently ignored**. If the decision is to fix,
record the test that covers the fix. If accepted, record the ACK. Never include
secrets, tokens, or personal data in this file.

## Review

Last reviewed: 2026-11-22. Review before storing personal data, adding
authentication, exposing the service publicly, or increasing data volume.
