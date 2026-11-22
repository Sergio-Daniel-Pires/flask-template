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

.. code-block:: bash

   uv sync --extra dev

Activation is optional with ``uv run`` but useful for editors and direct
commands.

Windows PowerShell:

.. code-block:: powershell

   .\.venv\Scripts\Activate.ps1
   # If script execution is blocked:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Linux/macOS:

.. code-block:: bash

   source .venv/bin/activate

Without ``uv``:

.. code-block:: bash

   python -m venv .venv
   # activate as above
   pip install -e ".[dev]"

Run
---

Backend:

.. code-block:: bash

   uv run flask --app project.app run --debug

Frontend, in another terminal:

.. code-block:: bash

   cd frontend
   npm install
   npm run dev

Open <http://localhost:5173>. The API runs at <http://localhost:5000>.

Tests
-----

Backend:

.. code-block:: bash

   uv run ruff check .
   uv run ruff format --check .
   uv run pytest --cov=project --cov-report=term-missing

Frontend:

.. code-block:: bash

   cd frontend
   npm run typecheck
   npm run build

Playwright:

.. code-block:: bash

   cd frontend
   npx playwright install --only-shell chromium   # first time
   npm run test:e2e

``test:e2e`` builds the frontend and serves it through Flask on port 5050. For
the fast loop, keep Flask and Vite running and use ``npm run test:e2e:dev``.

Docs
----

.. code-block:: bash

   uv sync --extra docs
   uv run sphinx-build -W -b html docs docs/_build/html

Open ``docs/_build/html/index.html``.

Port cleanup
------------

Use ``Ctrl+C`` in each terminal. If a port is stuck on Windows:

.. code-block:: powershell

   Get-NetTCPConnection -LocalPort 5000,5173 -State Listen
   Stop-Process -Id <PID> -Force

On Linux/macOS:

.. code-block:: bash

   lsof -i :5000
   lsof -i :5173
   kill <PID>
