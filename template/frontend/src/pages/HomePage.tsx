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
    <section className="page">
      <header className="hero">
        <p className="eyebrow">Flask + React starter</p>
        <h1>{PROJECT_NAME}</h1>
        <p className="lede">
          A small, working app with a documented API and end-to-end tests. This
          Home is a placeholder: replace it with the requested screen.
        </p>

        <div className="actions">
          <a className="button" href="/api/docs">
            API docs
          </a>
        </div>
      </header>

      <div className="dashboard">
        <article className="card">
          <div className="card-heading">
            <h2>Backend</h2>
            {!status.loading && !status.error ? (
              <span className="badge">Online</span>
            ) : null}
          </div>

          {status.loading ? (
            <p className="muted">Checking the API…</p>
          ) : status.error ? (
            <p className="alert" role="alert">
              {status.error}
            </p>
          ) : (
            <p className="status" data-testid="api-status">
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
              <dt>Health</dt>
              <dd>
                <a href="/healthz">/healthz</a>
              </dd>
            </div>
          </dl>
        </article>

        <article className="card">
          <div className="card-heading">
            <h2>API surface</h2>
            <a className="text-link" href="/api/docs">
              Swagger
            </a>
          </div>

          <ul className="endpoint-list">
            <li>
              <code>GET /api/home/</code>
              <span>Hello World</span>
            </li>
            <li>
              <code>POST /api/echo/string</code>
              <span>Echo example</span>
            </li>
            <li>
              <code>GET /healthz</code>
              <span>Health check</span>
            </li>
          </ul>

          <p className="hint">
            API reference lives in Swagger. Architecture, development, and
            deployment notes live in the Sphinx docs under <code>docs/</code>.
          </p>
        </article>
      </div>
    </section>
  );
}
