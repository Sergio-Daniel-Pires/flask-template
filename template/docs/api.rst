API
===

Swagger is the only API reference. Start the backend and open
<http://localhost:5000/api/docs>. Do not duplicate request/response schemas in
this documentation; update the Flask-RESTX models and docstrings instead.

Endpoints
---------

``GET /api/home/``
   Small sanity check used by the frontend and monitoring.

``POST /api/echo/string``
   Example endpoint with JSON validation. It accepts ``message`` and
   ``echo_type`` (``None``, ``Reverse``, or ``Mirror``).

``GET /healthz``
   Process health and version. It is outside the ``/api`` prefix.

Error behavior
--------------

- Validation errors return 400 with a JSON message.
- Unknown API routes return 404 JSON.
- Production must not expose stack traces.
- Request bodies are capped at 1 MiB.
