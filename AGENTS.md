# Repository instructions

This repository is a **project generator**, not the running application. The
application lives in `template/` and is rendered by `create_project.py` into a
new directory.

## Map

- `create_project.py` — stdlib generator. Renders `[[ token ]]` and
  `[[#if feature]]...[[/if]]` blocks. Supports `--database sqlite|none`.
- `template/` — source copied into every generated project. Its `README.md`,
  `AGENTS.md`, and `.opencode/` land at the root of the generated project.
- `template/project/` — Flask backend (app factory, services, SQLite example).
- `template/frontend/` — React/Vite frontend and Playwright tests.
- `.github/workflows/template-ci.yml` — generates both variants and validates
  backend, frontend, and Playwright.

## Before coding

1. Confirm the scope in 3–6 bullets and ask blocking questions. Do not guess on
   product behavior, data model, API contract, or visual direction.
2. Create a branch from `main`: `feat/...`, `fix/...`, `docs/...`, or
   `chore/...`. Never commit directly to `main`; if the working tree has
   unrelated changes, ask before touching them. Exception: the user explicitly
   asks for a direct meta/docs change.
3. For multi-step changes, write a short todo list. Keep the first slice
   end-to-end before polishing.

## Changing the template

- Edit files under `template/` (or the generator when the change is structural).
- Keep placeholders and conditional blocks consistent. If the change touches
  the database, validate both `--database sqlite` and `--database none`.
- Do not run app commands from the repository root: generate a project first.
- Prefer the existing stack and dependencies. New dependencies need a concrete
  reason and a mention in the PR.

## Validate

Generate both variants in a sibling directory:

```bash
python create_project.py -n review-db --path ../review-db --vps-host 203.0.113.10 --no-git-init
python create_project.py -n review-nodb --path ../review-nodb --vps-host 203.0.113.10 --database none --no-git-init
```

For each generated project:

```bash
uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run pytest

cd frontend
npm ci
npm run typecheck
npm run build
npm run test:e2e
```

Docker build/smoke test when Docker is available. If Docker or the VPS is not
available, state that explicitly instead of claiming it was tested.

## Skills

Load each skill by its exact ID before the task it covers; do not just mention
it in the plan.

- `impeccable` — implement and review UI in `template/frontend`.
- `design-taste-frontend` — only when the visual direction is open. Propose two
  text options (layout, density, main action), wait for a choice, then use
  Impeccable to build it.
- `owasp-review` — local skill in `.opencode/skills/owasp-review` (also installed
  globally). Review the current diff before opening or updating a PR. Accepted
  findings must be recorded in `template/SECURITY.md` (ACK), not ignored.

If a skill is unavailable, say so and apply the same checklist manually.

## Commits and PR

- Use small, conventional commits.
- Push the branch and open a draft PR against `main` with a summary, test
  evidence, and known risks. Do not merge without explicit approval.
- Iterate on the same branch and PR. Never force-push a branch under review; if
  the scope changes materially, propose a new branch/PR.
