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
- `docs/` — readable reStructuredText implementation docs (requirements,
  architecture, development, testing, deployment, database). No build step.
- `tests/` — pytest API tests. They use an isolated database when persistence
  is involved.
- `frontend/e2e/` — Playwright tests. They run against the real Flask app
  served on port 5050.
- `instance/` — runtime SQLite data when the database option is enabled. Never
  commit it.
- `deploy/`, `Dockerfile`, `docker-compose.yml` — production/deploy only.

## Documentation map

- `README.md` — short quick start and links; do not duplicate implementation
  docs there.
- `docs/*.rst` — requirements, architecture, development, testing, deployment,
  and database details. Read them directly; no Sphinx build.
- Swagger at `/api/docs` — the **only** API reference; do not duplicate schemas
  in `.rst`.
- `SECURITY.md` — security baseline and accepted risks (ACK).
- `docs/testing.rst` — what each test covers and what it does not cover.

Docs-first: before implementing, update the relevant `.rst` page (usually
`docs/requirements.rst`) with a short note on scope, API/data changes, and
decisions. Keep it concise so the user can review it while you implement.

## Environments and server ownership

[[#if database]]
| Role | Backend | Frontend | Database |
| --- | --- | --- | --- |
| Demo (user + main agent) | `5000` | `5173` | `instance/app.db` |
| Agent preview | `5051` | `5273` | `instance/preview.db` |
| Playwright E2E | `5050` | build served by Flask | temp SQLite per run |
[[/if]]
[[#unless database]]
| Role | Backend | Frontend |
| --- | --- | --- |
| Demo (user + main agent) | `5000` | `5173` |
| Agent preview | `5051` | `5273` |
| Playwright E2E | `5050` | build served by Flask |
[[/unless]]

- The demo stack belongs to the user and the main agent. Both may start, see
  logs, stop, and restart it in visible Windows terminals.
- The agent may use the preview stack (`npm run preview:agent` from
  `frontend/`) on `5051/5273`. It must not use `5000/5173` for preview.
[[#if database]]
- Playwright owns `5050` and creates/removes its own temp SQLite. It must not
  reuse demo or preview servers.
[[/if]]
[[#unless database]]
- Playwright owns `5050`. It must not reuse demo or preview servers.
[[/unless]]
- Never use `Start-Process`, `&`, `nohup`, or another background mechanism for
  dev servers. If a server must stay up, the user or main agent runs it in a
  visible terminal and owns the process.
- Do not kill processes you did not start. Check ports before starting.
- During a presentation, preserve the demo processes and code. The agent may
  run isolated tests in parallel without waiting for an OK. If it finds a bug,
  report it and hold the fix until the presentation ends.

## Feature workflow

1. **Clarify** the user flow and acceptance criteria with the user. No code.
2. **Roadmap:** list the slices (docs, API/data, frontend, tests) and include an
   explicit art-direction decision: **create a new direction (preferred)** or
   **reuse the starter's cream+green system** (only when the user asks for
   continuity or an existing design system must be preserved). Prefer a new
   direction; reuse needs a concrete reason.
3. **Docs first:** write a short `docs/requirements.rst` and wait for review
   while implementation starts.
4. **Two subagents in parallel when useful:**
   - Backend: `project/**`, `tests/**`, API/database contract. No servers.
   - Frontend: `frontend/src/**`, UI components/styles. No servers, no E2E.
   - The main agent owns `docs/**`, integration, servers, and E2E.
5. **Integrate** and run pytest/typecheck. The user presents the frontend.
6. **Tests in parallel:** the agent may write/run isolated E2E while the user
   presents. Do not change demo code or processes during the presentation.
7. After the user gives the OK, finish fixes and update docs/tests.

The starter theme is scaffolding, not the product's identity. Before UI work,
the roadmap states the art-direction decision in one sentence. Prioritize a new
direction (palette, type, density, main action); use Taste when the direction is
open and Impeccable to implement. Reuse the cream+green system only with a
concrete reason, never as an unexamined default.

## Working loop

1. Confirm the user flow and its main business rule in 1–3 bullets. Ask only if
   the answer would change what you build next. State reasonable, reversible
   assumptions and proceed.
2. Update `docs/*.rst` first with the short scope/API/decision note.
3. Build the smallest working slice from UI to API and, when used, storage.
   Reuse existing patterns and keep the diff focused.
4. Run the smallest relevant test first. For UI/API changes, run
   `npm run test:e2e` against the real backend before reporting done. Verify the
   main flow and the most important failure case, then broader checks as time
   allows.
5. Report exactly what passed, what failed, what was not run, and which coverage
   gaps remain. Keep test expectations intact when fixing implementation bugs.
6. Work locally. Create branches, commits, pushes, or PRs when requested.
   Preserve unrelated changes and ask only if they block the requested edit.

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
[[#if database]]
npm run test:e2e       # E2E on 5050 with temp SQLite
npm run preview:agent  # preview on 5051/5273 with preview.db
[[/if]]
[[#unless database]]
npm run test:e2e       # E2E on 5050
npm run preview:agent  # preview on 5051/5273
[[/unless]]
```

`gunicorn` is Linux/production only; use Flask's dev server on Windows.

## Skills and when to use them

Load the skill by its exact ID before starting the part of the work it covers
(for example, load `owasp-review` before reviewing the diff). Naming a skill in
the plan is not the same as using it.

- **`design-taste-frontend` (Taste)** - use when the art direction is open or a
  new one is needed. State the create-vs-reuse decision first, then propose two
  compact new directions in text (layout, density, main action) when the user
  wants options. If the flow is clear, pick the stronger new direction and
  proceed instead of silently reusing the starter theme.
- **`impeccable`** — use to build or review the requested screen. Prioritize
  hierarchy, forms, focus, and error/success states.
- **`owasp-review`** — use when the user asks, or before the demo if the diff
  touched permissions, sensitive data, or critical writes. Review the diff and
  the code needed to confirm each finding. Record any finding you accept in
  `SECURITY.md` under **Accepted risks (ACK)**; do not silently ignore it.
- This is an **Operate** app (dashboard/form), not a marketing page. Use
  Impeccable's restraint; do not apply Taste marketing sections, effects, or
  photography to these screens.
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
- For state-changing endpoints, decide whether retries are safe. If they are,
  add an idempotency key or a unique constraint and test two identical
  requests. If the endpoint is intentionally non-idempotent, state that.
- When concurrent writes matter, test the transaction boundary or document why
  it cannot be tested here; check for partial writes.
- If the feature handles money, store integer cents and validate bounds and
  precision before writing.
- If user identity is introduced, enforce record ownership on the server to
  prevent IDOR.
- If cookie sessions are used, add CSRF protection to state-changing routes.
- Keep secrets and sensitive data out of responses and logs.
- The database wiring uses `db.create_all()` intentionally for the starter. It
  creates no example model. Add models and migrations when the feature needs
  persistence instead of destructive resets.

## Frontend and UI

- The starter ships a single **Home** placeholder. If the task does not ask for
  a landing/home screen, remove or replace it; do not force it into the flow.
- Make the main action obvious and prevent accidental duplicate submissions.
- Keep labels, focus states, and error messages accessible. Use semantic
  buttons and form elements.
- Show explicit loading, empty, error, and success states.
- For financial screens, make amounts easy to compare and show the result of
  each action clearly. Use a restrained visual style suited to the workflow.
- Reuse existing components and patterns, but do not inherit the starter
  palette without an explicit choice. The roadmap's art-direction decision
  controls the visual system. Keep animation minimal.
- Do not introduce a new UI framework, state manager, or CSS system unless the
  user asks.

## Tests

- pytest for business rules, validation, persistence, and failure cases.
- Playwright for one key user journey; add a rejection path when it matters.
- **E2E must use the real Flask backend.** Never mock `/api` with
  `page.route`, MSW, `route.fulfill`, or `route.abort` in `frontend/e2e/`.
  `npm run test:e2e:guard` fails the suite if you do. Mock only in
  unit/component tests outside `e2e/`, and label those as UI tests, not E2E.
[[#if database]]
- **E2E isolation:** Playwright owns `5050` and a temp SQLite created per run.
  It must not reuse the demo (`5000/5173`) or preview (`5051/5273`) servers and
  must never open `instance/app.db`. There is no `test:e2e:dev` shortcut.
- pytest uses `:memory:` when sufficient; use a temp file only when multiple
  connections are needed. Test mode must fail before opening `instance/app.db`.
[[/if]]
[[#unless database]]
- **E2E isolation:** Playwright owns `5050`. It must not reuse the demo
  (`5000/5173`) or preview (`5051/5273`) servers. There is no `test:e2e:dev`
  shortcut.
[[/unless]]
- Invalid inputs: assert 4xx and that the database did not change.
- Idempotency: if a write can be retried, test replay, conflict (same key,
  different payload), key scope, missing key, and retry after rejection. A
  sequential duplicate request is **not** a concurrency test.
- Race conditions: real concurrency needs a file-backed database and two
  threads/processes. If tests are sequential, say "real concurrency not
  tested." Do not claim race-condition coverage from sequential tests.
- If identity is a client-controlled header or demo shortcut, say so. A filter
  using the ID you sent is not authorization/IDOR protection; only claim IDOR
  coverage with an authenticated identity and a server-side ownership check.
- Run `npm run typecheck` and the build when the frontend changes.
- Run `npm run test:e2e` before reporting UI/API work as done. If it cannot run,
  say exactly why.
- Update `docs/testing.rst` when coverage changes.

## Evidence and reporting

Separate **what the code does** from **what the tests demonstrate**. Never
claim a property is covered unless a test actually exercises it.

Report:

1. **Scope** — files/routes changed, and what was reviewed (backend, frontend,
   or both).
2. **Commands** — exact commands and results. For Playwright, state that it
   used the real Flask backend.
3. **Coverage table** — `Area | Covered? | What is tested | What is not tested`.
4. **Gaps** — idempotency, concurrency, auth/authorization, rate limiting,
   cross-browser, load, or anything not run.
5. **Security review** — scope and findings separately from product decisions
   and operational notes.

Use precise language:

- “Sequential replay is tested; simultaneous same-key requests are not.”
- “The employee header is a demo identity shortcut; ownership filtering is
  tested, real authorization is not.”
- “The backend was reviewed; files added afterwards were not.”
- “The logic is implemented, but only sequential behavior was verified.”
- “This is a product decision, not a security finding.”

Do not say “tests pass” without naming the commands and the layer. Do not put
product decisions (for example, automatic approval) or operational notes
(pagination, retention) in a security severity table. Do not present a mocked
API test as backend coverage.

## Definition of done

- The requested flow works end to end.
- The main business rule and its most important failure case were checked.
- When a failed operation could leave partial writes, verify the stored state.
- UI/API changes: `npm run test:e2e` ran against the real backend, or the
  reason it could not run is stated.
- Relevant docs in `docs/*.rst` were updated (readable directly; no build).
- The final report includes commands, evidence, scope of any security review,
  and gaps that matter for the demo.
