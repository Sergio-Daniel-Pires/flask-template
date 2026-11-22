# Project instructions

This is a Windows-first full-stack starter for a timed AI-assisted coding
interview. Stack: Flask + React/Vite + pytest + Playwright. The generated SQLite
example (Flask-SQLAlchemy) is present when the project was created with
`--database sqlite`; omit DB-specific steps if it was generated with
`--database none`.

Read `README.md`, `pyproject.toml`, `frontend/package.json`, and the existing
code before changing anything. Prefer the commands in those files over guesses.

## Project map

- `project/` — Flask app factory (`app.py`), settings (`config.py`), services
  (`services/`), and WSGI entrypoint (`wsgi.py`).
- `frontend/` — React + TypeScript + Vite. The Vite dev server proxies `/api`
  and `/healthz` to Flask. In production Flask serves `frontend/dist`.
- `tests/` — pytest API tests. They use an isolated database when persistence
  is involved.
- `frontend/e2e/` — Playwright tests. They run against the built app served by
  Flask on port 5050.
- `instance/` — runtime SQLite data when the database option is enabled. Never
  commit it.
- `deploy/`, `Dockerfile`, `docker-compose.yml` — production/deploy only.

Useful commands:

```bash
uv sync --extra dev
uv run flask --app project.app run --debug
uv run pytest
uv run ruff check .
uv run ruff format --check .

cd frontend
npm install
npm run dev
npm run typecheck
npm run build
npm run test:e2e       # production path; builds and serves on 5050
npm run test:e2e:dev   # reuses already-running dev servers
```

`gunicorn` is Linux/production only; use Flask's dev server on Windows.

## Working loop

1. Confirm the user flow and its main business rule in 1–3 bullets. Ask only if
   the answer would change what you build next. State reasonable, reversible
   assumptions and proceed.
2. Build the smallest working slice from UI to API and, when used, storage.
   Reuse existing patterns and keep the diff focused.
3. Run the smallest relevant test first. Verify the main flow and the most
   important failure case, then run broader checks as time allows.
4. Report exactly what passed, what failed, and what was not run. Keep test
   expectations intact when fixing implementation bugs.
5. Work locally. Create branches, commits, pushes, or PRs when requested.
   Preserve unrelated changes and ask only if they block the requested edit.

## Skills and when to use them

Load the skill by its exact ID before starting the part of the work it covers
(for example, load `owasp-review` before reviewing the diff). Naming a skill in
the plan is not the same as using it.

- **`design-taste-frontend` (Taste)** — use when the user asks for visual
  options. Propose two compact directions in text, including layout, density,
  and the main action. If the user already asked for implementation and the flow
  is clear, proceed with a simple layout that prioritizes the main action.
- **`impeccable`** — use to build or review the requested screen. Prioritize
  hierarchy, forms, focus, and error/success states.
- **`owasp-review`** — use when the user asks, or before the demo if the diff
  touched permissions, sensitive data, or critical writes. Review the diff and
  the code needed to confirm each finding. Record any finding you accept in
  `SECURITY.md` under **Accepted risks (ACK)**; do not silently ignore it.
- If a skill is unavailable, say so and apply the same checklist manually.

## Backend and data

- Validate inputs on the server using the project's existing validation
  mechanism. If Flask-RESTX models are used, verify validation is actually
  enabled (for example, `@ns.expect(model, validate=True)`); declaring a model
  alone is not validation. Return clear 4xx responses; do not leak stack traces.
- When the project uses persistence, use SQLAlchemy ORM queries or bound
  parameters. Never concatenate user input into SQL.
- When multiple writes belong to one business operation, commit them together
  and roll back on failure. Test the database state after a rejected request.
- If the feature handles money, store integer cents and validate bounds and
  precision before writing.
- If user identity is introduced, enforce record ownership on the server to
  prevent IDOR.
- If cookie sessions are used, add CSRF protection to state-changing routes.
- Keep secrets and sensitive data out of responses and logs.
- The generated database example uses `db.create_all()` intentionally for the
  starter. If the schema starts to evolve, propose migrations instead of
  destructive resets.

## Frontend and UI

- Make the main action obvious and prevent accidental duplicate submissions.
- Keep labels, focus states, and error messages accessible. Use semantic
  buttons and form elements.
- Show explicit loading, empty, error, and success states.
- For financial screens, make amounts easy to compare and show the result of
  each action clearly. Use a restrained visual style suited to the workflow.
- Reuse existing components and styles. Keep animation minimal.
- Do not introduce a new UI framework, state manager, or CSS system unless the
  user asks.

## Tests

- pytest for business rules, validation, persistence, and failure cases.
- Playwright for one key user journey; add a rejection path when it matters.
- Use a separate test database so runs are repeatable and do not depend on
  manual state.
- When persistence is involved, after a failed write assert both the error
  response and the database state.
- Run `npm run typecheck` and the build when the frontend changes.

## Definition of done

- The requested flow works end to end.
- The main business rule and its most important failure case were checked.
- When a failed operation could leave partial writes, verify the stored state.
- Report the commands run, their results, and any gaps that matter for the demo.
