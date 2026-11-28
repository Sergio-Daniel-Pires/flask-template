Development
===========

Requirements
------------

- Python 3.11+
- Node.js 20+ (22 recommended)
- ``uv`` recommended; ``pip`` also works
- Docker only for production/deploy

Setup and activation
--------------------

Create the environment and install dependencies once:

::

   uv sync --extra dev

Activation is optional with ``uv run`` but useful for editors and direct
commands.

Windows PowerShell:

::

   .\.venv\Scripts\Activate.ps1
   # If script execution is blocked:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Linux/macOS:

::

   source .venv/bin/activate

Without ``uv``:

::

   python -m venv .venv
   # activate as above
   pip install -e ".[dev]"

Run
---

Backend:

::

   uv run flask --app project.app run --debug

Frontend, in another terminal:

::

   cd frontend
   npm install
   npm run dev

Open <http://localhost:5173>. The API runs at <http://localhost:5000>.

Ports:

[[#if database]]
- **Demo (user + main agent):** backend ``5000``, frontend ``5173``, database
  ``instance/app.db``.
- **Agent preview:** backend ``5051``, frontend ``5273``, database
  ``instance/preview.db``.
- **Playwright E2E:** backend ``5050``, build served by Flask, temp SQLite per
  run.
[[/if]]
[[#unless database]]
- **Demo (user + main agent):** backend ``5000``, frontend ``5173``.
- **Agent preview:** backend ``5051``, frontend ``5273``.
- **Playwright E2E:** backend ``5050``, build served by Flask.
[[/unless]]

Agent preview:

::

   cd frontend
   npm run preview:agent

Do not use ``5000/5173`` for preview. Playwright never reuses the demo or
preview servers.
[[#if database]]
It also never opens ``instance/app.db``.
[[/if]]

Tests
-----

Backend:

::

   uv run ruff check .
   uv run ruff format --check .
   uv run pytest --cov=project --cov-report=term-missing

Frontend:

::

   cd frontend
   npm run typecheck
   npm run build

Playwright:

::

   cd frontend
   npx playwright install --only-shell chromium   # first time
   npm run test:e2e

``test:e2e`` builds the frontend, serves it through Flask on port 5050, and
creates a temp SQLite that is removed at the end. In test mode the app refuses
to open ``instance/app.db`` or a test database outside the OS temp directory.

Docs
----

Read the ``docs/*.rst`` files directly in the editor or on GitHub. No Sphinx
build is required; the API reference is Swagger at ``/api/docs``.

Port cleanup
------------

Use ``Ctrl+C`` in each terminal. If a port is stuck on Windows:

::

   Get-NetTCPConnection -LocalPort 5000,5173 -State Listen
   Stop-Process -Id <PID> -Force

On Linux/macOS:

::

   lsof -i :5000
   lsof -i :5173
   kill <PID>
