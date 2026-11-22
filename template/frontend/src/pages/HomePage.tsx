import { useEffect, useState } from "react";

import { PROJECT_NAME } from "../config";
import { api, fetchHealth } from "../lib/api";

type Status = {
  loading: boolean;
  message: string | null;
  version: string | null;
  error: string | null;
};

export default function HomePage() {
  const [status, setStatus] = useState<Status>({
    loading: true,
    message: null,
    version: null,
    error: null,
  });

  useEffect(() => {
    let active = true;

    Promise.all([api.home(), fetchHealth()])
      .then(([home, health]) => {
        if (!active) return;
        setStatus({
          loading: false,
          message: home.result,
          version: health.version,
          error: null,
        });
      })
      .catch((error: unknown) => {
        if (!active) return;
        setStatus({
          loading: false,
          message: null,
          version: null,
          error: error instanceof Error ? error.message : "Unknown error",
        });
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="stack">
      <header className="hero">
        <p className="eyebrow">Flask + React + Vite</p>
        <h1>{PROJECT_NAME}</h1>
        <p className="lede">
          A starter built for fast iteration: a documented API, a typed frontend,
          and end-to-end tests.
        </p>
      </header>

      <div className="grid">
        <article className="card">
          <h2>Backend</h2>
          {status.loading ? (
            <p className="muted">Checking the API…</p>
          ) : status.error ? (
            <p className="error" role="alert">
              {status.error}
            </p>
          ) : (
            <p className="success" data-testid="api-status">
              <span className="dot" aria-hidden="true" />
              {status.message}
            </p>
          )}

          <dl className="meta">
            <div>
              <dt>Version</dt>
              <dd>{status.version ?? "—"}</dd>
            </div>
            <div>
              <dt>Health check</dt>
              <dd>
                <a href="/healthz">/healthz</a>
              </dd>
            </div>
          </dl>
        </article>

        <article className="card">
          <h2>Endpoints</h2>
          <ul className="endpoint-list">
            <li>
              <code>GET /api/home/</code>
              <span>Hello World</span>
            </li>
            <li>
              <code>POST /api/echo/string</code>
              <span>Echo messages</span>
            </li>
            [[#if database]]
            <li>
              <code>GET /api/notes/</code>
              <span>Notes list</span>
            </li>
            [[/endif]]
            <li>
              <code>GET /api/docs</code>
              <span>Swagger UI</span>
            </li>
          </ul>
        </article>

        <article className="card accent">
          <h2>Next step</h2>
          <p>
            Edit <code>project/services/</code> on the backend and{" "}
            <code>frontend/src/pages/</code> on the frontend. Vite proxies{" "}
            <code>/api</code> to Flask in development.
          </p>
          <a className="button" href="/echo">
            Try the echo
          </a>
        </article>
      </div>
    </section>
  );
}
