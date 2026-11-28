Architecture
============

Stack
-----

- Flask app factory in ``project/app.py``
- Flask-RESTX namespaces under ``project/services/``
- React 19 + TypeScript + Vite in ``frontend/``
- pytest for the API and Playwright for browser flows
[[#if database]]
- SQLite through Flask-SQLAlchemy
[[/if]]

Request flow
------------

Development:

::

   browser -> Vite :5173 -> /api and /healthz proxy -> Flask :5000

Production:

::

   browser -> nginx/TLS -> Flask/Gunicorn :8000
                         -> /api and /healthz
                         -> frontend/dist (SPA fallback)

The container listens on ``127.0.0.1`` only. nginx/Caddy terminates TLS and
applies rate limits; that is outside this package by design.

Backend layout
--------------

- ``project/app.py`` — factory, API registration, health check, SPA serving.
- ``project/config.py`` — environment settings and production secret checks.
- ``project/wsgi.py`` — Gunicorn entrypoint.
- ``project/services/`` — one namespace per feature.
- ``tests/`` — API tests; persistence tests use an isolated database.

API conventions
---------------

- All HTTP routes live under ``/api``.
- Swagger UI is at ``/api/docs``; it is the single API reference.
- ``/healthz`` stays outside the API prefix for probes.
- Errors return JSON with a clear 4xx status and no stack traces.
- Validate payloads with the existing Flask-RESTX models before domain logic.

Frontend layout
---------------

- ``frontend/src/pages/`` — app surfaces. The starter ships a Home placeholder;
  remove or replace it if the task does not ask for a landing page.
- ``frontend/src/lib/api.ts`` — typed API client.
- ``frontend/e2e/`` — Playwright tests for the real browser flow.
- In development Vite proxies ``/api`` and ``/healthz``; in production Flask
  serves ``frontend/dist`` and falls back to ``index.html`` for SPA routes.

Related
-------

- `Development <development.rst>`_ — setup, commands, and tests.
- `API <api.rst>`_ — where the API reference lives.
- `Deployment <deployment.rst>`_ — Docker, nginx, and VPS deployment.
[[#if database]]
- `Database <database.rst>`_ — SQLite/SQLAlchemy wiring.
[[/if]]
