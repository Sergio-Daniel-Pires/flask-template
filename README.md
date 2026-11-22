# Flask + React template

Template that generates a complete project with **Flask**, **React/Vite**,
optional **SQLite**, tests, and automatic deployment to a VPS via GitHub
Actions.

This repository is not the application itself: it generates a **new project
folder** already configured with the project name, author, port, and VPS host.
The generator uses only the Python standard library, so no setup is required to
create a project.

> There is no MongoDB by default (or any database). The default is **SQLite** via
> Flask-SQLAlchemy; `--database none` generates the project without a database.

## Requirements

- Python 3.11+ (to generate and run the backend)
- Node.js 20+ (for the frontend)
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`
- Docker + Docker Compose (production/deploy only)
- Git (optional, to initialize the project)

## Create a project

```bash
python create_project.py \
  --name my-api \
  --vps-host 203.0.113.10 \
  --port 8000
```

On Windows (PowerShell), in one line:

```powershell
python create_project.py --name my-api --vps-host 203.0.113.10 --port 8000
```

This creates `../my-api` (a sibling folder of the template) with:

- a local `.env` already filled with a random secret key
- a Git repository initialized on `main`
- VPS host, user, path, and port applied to the deploy workflow
- frontend, backend, tests, and CI ready to run

### Options

| Option | Default | Description |
| --- | --- | --- |
| `-n, --name` | required | Kebab-case project name (`my-api`) |
| `--path` | `../<name>` | Destination folder |
| `-a, --author` | `git config user.name` | Author in `pyproject.toml` |
| `-e, --email` | `git config user.email` | Author email in `pyproject.toml` |
| `--vps-host` | required | Host/IP embedded in the deploy workflow |
| `--vps-user` | `root` | SSH user for deployment |
| `--vps-path` | `/opt/<name>` | Project folder on the VPS |
| `--port` | `8000` | Host port for the app; bound to `127.0.0.1` |
| `--repo-url` | inferred from `origin` | URL used by the VPS setup script |
| `--database` | `sqlite` | `sqlite` includes the CRUD example; `none` removes it |
| `--no-git-init` | off | Skip `git init` |

## Run the generated project

Backend:

```bash
cd ../my-api
uv sync --extra dev
uv run flask --app project.app run --debug
```

Frontend (another terminal):

```bash
cd frontend
npm install
npm run dev
```

- Frontend: <http://localhost:5173>
- API: <http://localhost:5000>
- Swagger: <http://localhost:5000/api/docs>
- Health: <http://localhost:5000/healthz>

Without `uv`, use `python -m venv .venv`, activate it, and run
`pip install -e ".[dev]"`. The generated README has the steps for Windows and
Linux.

## What the generated project includes

- **Backend**: app factory, environment settings, versioned `/api`, proper HTTP
  errors, Swagger, and `/healthz`.
- **Frontend**: React 19 + TypeScript + React Router, example pages, and an
  `/api` proxy in Vite.
- **Database**: SQLite at `instance/app.db` (Flask-SQLAlchemy) with a small notes
  CRUD example; `DATABASE_URL` switches to Postgres/MySQL.
- **Tests**: pytest for the API and Playwright (headless Chromium) for the real
  browser flow.
- **Docker**: multi-stage image (React build + Gunicorn), non-root user,
  healthcheck, and a persistent volume for SQLite.
- **CI**: lint, typecheck, tests, Playwright, and a Docker build/smoke test.
- **Deploy**: SSH + `docker compose up -d --build`, with a health check.
- **Security**: `SECURITY.md` with the baseline and explicit accepted risks
  (ACK); the OWASP skill requires an ACK instead of silently ignoring a finding.
- **Agent instructions**: `AGENTS.md` with the project map, commands, and working
  loop; a local `owasp-review` skill; optional Impeccable/TasteSkill for UI.

### Fast Playwright

The suite has 3 tests and runs in headless Chromium:

```bash
cd frontend
npx playwright install --only-shell chromium   # first time
npm run test:e2e        # build + Flask on port 5050 (production path)
npm run test:e2e:dev    # reuses running Flask + Vite servers (fast loop)
```

`test:e2e` validates the real build served by Flask, including SPA deep links.
`test:e2e:dev` is the fastest loop: if both dev servers are already running,
there is no build or startup wait.

## Working on the template

The generated content lives in [`template/`](template/). To test a change:

```bash
python create_project.py -n sample-app --vps-host 203.0.113.10 --no-git-init
cd ../sample-app
uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run pytest
cd frontend && npm ci && npm run typecheck && npm run test:e2e
```

[`template-ci.yml`](.github/workflows/template-ci.yml) generates the project with
and without a database and runs backend, frontend, and Playwright.

## Deploy

The generated workflow (`.github/workflows/deploy.yml`) already contains the
host, user, directory, and port. Configure these in GitHub:

- `VPS_SSH_KEY` (required secret): SSH private key
- `VPS_FINGERPRINT` (optional secret, recommended): host fingerprint

On the VPS, run `bash deploy/setup-vps.sh` once; after that, every push to `main`
updates the project. The VPS `.env` is preserved across deploys. The container
binds to `127.0.0.1`; nginx/Caddy should terminate TLS and apply rate limits.

## Agents and skills

- Root `AGENTS.md`: rules for working on the template itself (generate both
  variants, validate, update the PR).
- `template/AGENTS.md`: instructions that land at the root of every generated
  project — stack, commands, scope/implementation/test loop, and definition of
  done.
- `.opencode/skills/owasp-review`: local security-review skill for the diff.
- Accepted findings are recorded in `template/SECURITY.md` (ACK), never silently
  ignored.
- UI: **Taste** only to explore two directions; **Impeccable** to implement the
  chosen direction. Installation instructions are in the generated README.

## Structure

```text
.
├── AGENTS.md                # instructions for agents in this repo
├── create_project.py        # generator (no dependencies)
├── .opencode/skills/        # local OWASP review skill
├── template/                # files copied into the new project
│   ├── AGENTS.md            # generated project instructions
│   ├── SECURITY.md          # baseline + accepted risks (ACK)
│   ├── project/             # Flask backend (factory + services)
│   ├── frontend/            # React + Vite + Playwright
│   ├── tests/
│   ├── deploy/              # VPS bootstrap
│   └── .github/workflows/   # generated project CI and deploy
└── .github/workflows/       # template CI
```
