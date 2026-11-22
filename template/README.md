# [[ project_name ]]

Flask backend + React/Vite frontend, generated from a lean starter template.

- API documented at `/api/docs` (Swagger)
- React 19 + TypeScript frontend, served by Flask in production
[[#if database]]
- SQLite via Flask-SQLAlchemy (notes CRUD example)
[[/if]]
- pytest for the API and Playwright for the real browser flow
- Docker Compose for the VPS and automatic deployment via GitHub Actions

## Requirements

- Python 3.11+ ([uv](https://docs.astral.sh/uv/) is recommended)
- Node.js 20+ (22 is the target)
- Docker + Docker Compose only for production/deploy
- Git

## Run on Windows and Linux

The project already comes with a local `.env` (random secret key) and runs
without Docker. Open two terminals.

### 1. Backend

```bash
uv sync --extra dev
uv run flask --app project.app run --debug
```

Without `uv`:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

pip install -e ".[dev]"
flask --app project.app run --debug
```

API at <http://localhost:5000>, docs at
<http://localhost:5000/api/docs>, and health check at
<http://localhost:5000/healthz>.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>. Vite proxies `/api` and `/healthz` to Flask on
port 5000.

### Local production with Docker (optional)

The project already has `.env` and a random secret key. If you are starting from
a clone without `.env`, create it from the example and replace
`FLASK_SECRET_KEY`:

```bash
cp .env.example .env   # Windows: Copy-Item .env.example .env
docker compose up -d --build
```

The app is available at <http://localhost:[[ app_port ]]>.

[[#if database]]
## Database

SQLite is the default, stored at `instance/app.db`, via Flask-SQLAlchemy. Set
`DATABASE_URL` to switch databases without changing code:

```bash
# SQLite relative to the instance/ folder (default)
DATABASE_URL=sqlite:///app.db

# PostgreSQL (install the driver, for example: uv add psycopg[binary])
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/app
```

Example routes:

- `GET /api/notes/` lists notes
- `POST /api/notes/` creates a note with `{"text": "..."}`

The starter uses `db.create_all()` on startup to keep the first run simple. When
the schema starts to evolve, replace it with migrations (Flask-Migrate or
Alembic).

Do not use the example database for sensitive data: it exists to demonstrate the
end-to-end integration.
[[/if]]

## Tests

Backend:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=project --cov-report=term-missing
```

Frontend:

```bash
cd frontend
npm run typecheck
npm run build
```

Playwright (headless Chromium):

```bash
cd frontend
npx playwright install --only-shell chromium   # first time
npm run test:e2e
```

`npm run test:e2e` tests the production path: the Vite build served by Flask on
an isolated port (5050), including SPA fallback.

For the fastest loop, keep `uv run flask ...` and `npm run dev` running and use:

```bash
npm run test:e2e:dev
```

In this mode the development servers are reused, with no rebuild.

## Agent skills (OpenCode)

This project includes `AGENTS.md` with the working loop (scope → end-to-end
slice → tests → review → demo) and the local
`.opencode/skills/owasp-review/SKILL.md`.

For UI work, install the skills once at the project root (if you already
installed them globally with `--global`/`-g`, skip this step):

```powershell
npx.cmd impeccable install
npx.cmd skills add https://github.com/Leonxlnx/taste-skill --list
npx.cmd skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend -a opencode
```

On Linux/macOS, use `npx` instead of `npx.cmd`.

- **Taste (`design-taste-frontend`)**: only when the visual direction is still
  open. Proposes two options and waits for a choice.
- **Impeccable**: implements the chosen direction and reviews layout, typography,
  forms, focus, and states.
- **`owasp-review`**: reviews the diff when asked or before the demo if it
  touches permissions, sensitive data, or critical writes.

Call examples:

1. “Use `design-taste-frontend` to propose two compact directions for this
   screen. Describe the layout, density, and main action. Wait for my choice.”
2. “Use `impeccable` to implement the chosen direction. Connect the main action
   to the API and show success or error clearly. Run the relevant test.”
3. “Use `owasp-review` on the current diff. Report concrete findings with file
   and line.”

Ask for skills by name in OpenCode. If a skill is not installed, the agent must
say so and apply the same checklist manually.

## Security

The baseline and consciously accepted risks (**ACK**) live in
[`SECURITY.md`](SECURITY.md). Rate limiting, TLS, and proxy headers are the
responsibility of nginx; the container listens only on `127.0.0.1`.

## Deploy to the VPS

The workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)
already contains these values:

| Item | Value |
| --- | --- |
| Host | `[[ vps_host ]]` |
| SSH user | `[[ vps_user ]]` |
| Directory | `[[ vps_path ]]` |
| Upstream port | `[[ app_port ]]` (bound to `127.0.0.1`) |

1. Generate an SSH key for deployment and authorize the public key on the VPS:

   ```bash
   ssh-keygen -t ed25519 -C "github-actions-[[ project_name ]]" -f deploy_key
   ssh-copy-id -i deploy_key.pub [[ vps_user ]]@[[ vps_host ]]
   ```

2. In GitHub, under **Settings → Secrets and variables → Actions**, create:

   - `VPS_SSH_KEY`: the private key contents (`deploy_key`)
   - `VPS_FINGERPRINT` (optional, recommended): host fingerprint. On the VPS:

     ```bash
     ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
     ```

3. On the VPS, run setup once:

   ```bash
   git clone [[ repo_url ]] [[ vps_path ]]
   cd [[ vps_path ]]
   bash deploy/setup-vps.sh
   ```

   The script installs Docker when needed, creates `.env` with a random secret
   key, and starts the containers.

4. After that, every push to `main` runs `git fetch/reset`, rebuilds the image,
   and checks health. The workflow uses the `production` environment; you can
   require manual approval in the repository settings.

Notes:

- The VPS `.env` is not versioned and survives `git reset --hard`.
- Private repository: configure a read-only deploy key on the VPS (or clone via
  HTTPS with a token) so `git fetch` works.
- The container listens on `127.0.0.1:[[ app_port ]]`; put nginx/Caddy with TLS
  in front and do not expose that port directly in the firewall. Rate limiting
  and TLS are the proxy's responsibility.
[[#if database]]
- For another database, set `DATABASE_URL` in the VPS `.env`.
[[/if]]

## Structure

```text
.
├── AGENTS.md               # agent instructions
├── SECURITY.md             # baseline + accepted risks (ACK)
├── .opencode/skills/       # local owasp-review skill
├── project/
│   ├── app.py              # factory + frontend build serving
│   ├── config.py           # environment settings
│   ├── wsgi.py             # Gunicorn entrypoint
│   └── services/           # home, echo
[[#if database]]
│       └── notes/          # SQLite example
[[/if]]
├── frontend/
│   ├── src/                # React pages and components
│   └── e2e/                # Playwright tests
├── tests/                  # pytest API tests
├── deploy/setup-vps.sh
├── .github/workflows/      # CI and deploy
├── Dockerfile
└── docker-compose.yml
```

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `FLASK_ENV` | `development` | `production` requires a strong `FLASK_SECRET_KEY` |
| `FLASK_SECRET_KEY` | — | required in production (at least 32 chars) |
[[#if database]]
| `DATABASE_URL` | `sqlite:///.../instance/app.db` | SQLAlchemy connection |
[[/if]]
| `FRONTEND_DIST` | `frontend/dist` | build folder served by Flask |
| `GUNICORN_BIND` | `0.0.0.0:8000` | Gunicorn bind |
| `GUNICORN_WORKERS` | `2` | workers |
| `GUNICORN_TIMEOUT` | `60` | timeout in seconds |

The frontend accepts `VITE_API_URL` if you want to point it at another API; the
default is `/api`.

---

Generated by `flask-template` — [[ year ]].
