Testing
~~~~~~~

Test matrix
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 38 32

   * - File
     - Covers
     - Does not cover
   * - ``tests/test_config.py``
     - Unknown ``FLASK_ENV``, weak/placeholder secrets, strong production
       secret.
     - Secret rotation or external secret managers.
   * - ``tests/test_security.py``
     - Security headers and oversized request body (413).
     - Full header policy (CSP/HSTS are proxy concerns).
   * - ``tests/health/test_ping.py``
     - Known routes, 404s, health payload.
     - Load or readiness under dependency failures.
   * - ``tests/test_api/test_home.py``
     - Home JSON contract.
     - —
   * - ``tests/test_api/test_echo.py``
     - Normal/reverse/mirror, missing fields, invalid enum, max length.
     - Idempotency and concurrency (read-only endpoint).
   * - ``frontend/e2e/home.spec.ts``
     - Home loads the real backend status and the API docs link.
     - Cross-browser behavior.

The E2E suite always runs against the real Flask backend. ``npm run
test:e2e:guard`` scans ``frontend/e2e`` and fails on ``page.route``, MSW, or
``route.fulfill``. Mocking is allowed only in unit/component tests outside
``e2e/`` and must not be reported as backend coverage.

Coverage gaps
-------------

These are intentionally not covered by the starter; add them when a feature
needs them:

- **Idempotency** — the starter ships no write endpoint. When one is added and
  can be retried, add an idempotency key or unique constraint and test replay,
  conflict, key scope, missing key, and retry after rejection. Sequential
  replay is not a concurrency test.
- **Race conditions** — concurrent writes are not tested. SQLite serializes
  writers; if a feature adds concurrent writes or external state, use a
  file-backed database plus two threads/processes and document the transaction
  boundary. Do not claim race coverage from sequential tests.
- **Authentication/authorization** — not implemented. A client-controlled
  header is a demo identity shortcut, not authentication. A filter using the ID
  you sent is not IDOR protection; only claim IDOR coverage with an
  authenticated identity and a server-side ownership check.
- **Rate limiting** — delegated to nginx/proxy (ACK-001 in ``SECURITY.md``).
- **Load/performance** — not tested.
- **Cross-browser** — Playwright runs Chromium only.

Testing layers
--------------

- **API integration** — pytest + Flask test client, real validation and
  database logic, no HTTP server.
- **E2E** — Playwright + real Flask backend + real database. No mocked
  ``/api`` routes; ``npm run test:e2e:guard`` enforces this.
- **Component/UI** — mocked API, if added. It is not backend coverage.

What to report
--------------

When reporting tests, include:

1. Scope: files/routes changed and the layer reviewed.
2. Exact commands run and their results.
3. Which backend the E2E suite exercised (it must be the real Flask app).
4. A coverage table: ``Area | Covered? | What is tested | What is not tested``.
5. What was not run and why.
6. Gaps that matter for the demo — especially idempotency, concurrency, auth,
   and rate limiting.
7. Security findings separately from product decisions and operational notes.

Use precise language:

- “Sequential replay is tested; simultaneous same-key requests are not.”
- “The employee header is a demo identity shortcut; ownership filtering is
  tested, real authorization is not.”
- “The backend was reviewed; frontend files added afterwards were not.”
- “The logic is implemented, but only sequential behavior was verified.”

Do not write “tests pass” without naming the commands and the layer they
covered. A mocked API test is a UI/component test, not backend coverage. Do not
put product decisions (for example, automatic approval) or operational notes
(pagination, retention) in a security severity table.
