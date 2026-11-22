---
name: owasp-review
description: Review changed Flask, SQLite, and React code for concrete security issues before a PR or demo.
---

Review the current diff and read adjacent code when needed to verify a finding.
Report findings **before** making edits. State the scope you reviewed: files,
routes, and whether the backend, frontend, or both were covered. If code was
added after the review started, say it was not reviewed.

## What to inspect

- Server-side validation for every field used in a database write.
- SQL built with bound parameters/ORM, never string interpolation.
- Access to a specific record (IDOR) when the app has user identity. A
  client-controlled header is a demo shortcut, not authentication; a filter
  using the ID you sent is not authorization.
- CSRF protection on state-changing routes when cookie sessions are used.
- Failure paths that can leave partial writes; transaction boundaries and rollback.
- Idempotency and duplicate submission: replay, conflict, key scope, missing
  key, and retry after rejection. Say when only sequential replay was tested.
- Real concurrency: threads/processes and a file-backed database. Sequential
  tests do not demonstrate race-condition safety.
- Secrets, tokens, passwords, and sensitive data exposed in responses or logs.
- XSS: unsafe HTML rendering, unescaped user content, dangerous URLs.
- Money handling: integer cents, bounds, precision, and server-side checks.
- File uploads/path traversal when the feature accepts files.

## Output

Report security findings separately from product decisions and operational
notes.

Security findings:

- **Severity**: high, medium, or low.
- **Location**: `file:line` (and the route or component when useful).
- **Impact**: what an attacker can actually do.
- **Smallest fix**: the least invasive change that removes the risk.
- **ACK**: if accepted, link the row in `SECURITY.md`.

Product decisions and operational notes:

- Items such as automatic approval, pagination, or retention policy are not
  security severities. List them separately with their rationale.

Verify each finding in the code; do not report speculative issues. If there are
no concrete findings, list what you checked and any residual risks. Distinguish
what the code implements from what the tests demonstrate:

- “The guard is implemented, but only sequential behavior was tested.”
- “The backend was reviewed; frontend files added afterwards were not.”
- “The identity header is a demo shortcut; real authorization was not tested.”

Do not edit code during the review unless the user asks you to apply the fixes.
If a finding will be accepted instead of fixed, add an ACK row to `SECURITY.md`
with the reason, current mitigation, and a trigger to revisit. Never ignore a
finding silently.
