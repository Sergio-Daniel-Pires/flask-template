Database
========

SQLite is the default, stored at ``instance/app.db``, through
Flask-SQLAlchemy. The starter wires the extension and app initialization but
ships **no example model**.

Switch databases
----------------

Use ``DATABASE_URL`` without changing code:

.. code-block:: bash

   # SQLite relative to the instance/ directory
   DATABASE_URL=sqlite:///app.db

   # PostgreSQL (install the driver, for example: uv add psycopg[binary])
   DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/app

Adding models
-------------

Add SQLAlchemy models under ``project/`` and import them before
``db.create_all()`` runs, or switch to migrations. Keep writes transactional
and validate every field on the server.

Schema changes
--------------

The starter calls ``db.create_all()`` on startup to keep the first run simple.
When the schema starts to evolve, replace it with migrations (Flask-Migrate or
Alembic) instead of destructive resets.

Tests
-----

Pytest uses an in-memory database, so tests are repeatable and never touch
``instance/app.db``. Add tests for the persistence behavior you introduce,
including the main rejection path and the stored state after failure.
