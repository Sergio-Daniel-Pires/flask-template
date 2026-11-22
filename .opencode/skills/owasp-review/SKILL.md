---
name: owasp-review
description: Review changed Flask, SQLite, and React code for concrete security issues before a PR or demo.
---

Review the current diff and read adjacent code when needed to verify a finding.
Report findings **before** making edits.

## What to inspect

- Server-side validation for every field used in a database write.
- SQL built with bound parameters/ORM, never string interpolation.
- Access to a specific record (IDOR) when the app has user identity.
- CSRF protection on state-changing routes when cookie sessions are used.
- Failure paths that can leave partial writes; transaction boundaries and rollback.
- Secrets, tokens, passwords, and sensitive data exposed in responses or logs.
- XSS: unsafe HTML rendering, unescaped user content, dangerous URLs.
- Money handling: integer cents, bounds, precision, and server-side checks.
- File uploads/path traversal when the feature accepts files.

## Output

For each finding, report:

- **Severity**: high, medium, or low.
- **Location**: `file:line` (and the route or component when useful).
- **Impact**: what an attacker can actually do.
- **Smallest fix**: the least invasive change that removes the risk.

Verify each finding in the code; do not report speculative issues. If there are
no concrete findings, list what you checked and any residual risks. Do not edit
code during the review unless the user asks you to apply the fixes.
