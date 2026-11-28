Deployment
==========

Model
-----

The VPS runs Docker Compose. The container binds only to
``127.0.0.1:APP_PORT``; nginx/Caddy terminates TLS and applies rate limits.
Do not expose the container port directly.

First setup
-----------

On the VPS:

::

   git clone REPO_URL /opt/PROJECT
   cd /opt/PROJECT
   bash deploy/setup-vps.sh

The script installs Docker when needed, creates ``.env`` with a random
``FLASK_SECRET_KEY``, applies ``chmod 600``, and starts the containers.

GitHub configuration
--------------------

In **Settings → Secrets and variables → Actions**:

- ``VPS_SSH_KEY`` — private SSH key for the deploy user.
- ``VPS_FINGERPRINT`` — recommended host fingerprint:
  ``ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub``.

The workflow already contains the host, user, path, and upstream port. Every
push to ``main`` runs ``git fetch/reset``, rebuilds the image, and checks
``/healthz``.

Environment
-----------

``.env`` on the VPS is not versioned and survives ``git reset --hard``. It must
contain at least:

::

   FLASK_ENV=production
   FLASK_SECRET_KEY=<random 32+ characters>
[[#if database]]
   # Optional: DATABASE_URL=postgresql+psycopg://...
[[/if]]

Production rejects an empty secret, a short secret, or placeholders such as
``change-me``.

Operations
----------

::

   docker compose ps
   docker compose logs -f
   docker compose up -d --build
   curl -fsS http://127.0.0.1:APP_PORT/healthz

Security
--------

The accepted risks (ACK) and the current mitigations are in ``SECURITY.md``.
Rate limiting and TLS belong to the reverse proxy, not this application.
