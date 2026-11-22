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
          error: error instanceof Error ? error.message : "Erro desconhecido",
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
          Base pronta para iterar rápido: API documentada, frontend tipado e testes
          de ponta a ponta.
        </p>
      </header>

      <div className="grid">
        <article className="card">
          <h2>Backend</h2>
          {status.loading ? (
            <p className="muted">Consultando a API…</p>
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
              <dt>Versão</dt>
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
              <span>Echo de mensagens</span>
            </li>
            [[#if database]]
            <li>
              <code>GET /api/notes/</code>
              <span>Lista de notas</span>
            </li>
            [[/endif]]
            <li>
              <code>GET /api/docs</code>
              <span>Swagger UI</span>
            </li>
          </ul>
        </article>

        <article className="card accent">
          <h2>Próximo passo</h2>
          <p>
            Edite <code>project/services/</code> no backend e{" "}
            <code>frontend/src/pages/</code> no front. O Vite faz proxy de{" "}
            <code>/api</code> para o Flask em desenvolvimento.
          </p>
          <a className="button" href="/echo">
            Testar o echo
          </a>
        </article>
      </div>
    </section>
  );
}
