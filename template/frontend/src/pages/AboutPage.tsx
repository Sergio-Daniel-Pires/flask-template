import { PROJECT_NAME } from "../config";

const STACK = [
  ["Backend", "Flask 3 + Flask-RESTX, factory de app e Swagger em /api/docs"],
  ["Frontend", "React 19 + Vite + TypeScript, com proxy de /api no dev"],
  ["Testes", "pytest para a API e Playwright (Chromium headless) para o fluxo real"],
  ["Deploy", "Docker Compose na VPS, acionado por GitHub Actions"],
];

export default function AboutPage() {
  return (
    <section className="stack narrow">
      <header>
        <p className="eyebrow">{PROJECT_NAME}</p>
        <h1>Sobre</h1>
        <p className="lede">
          Template enxuto para projetos pequenos, feito para rodar no Windows e no
          Linux sem depender de Docker no dia a dia.
        </p>
      </header>

      <div className="card">
        <h2>Stack</h2>
        <dl className="stacked">
          {STACK.map(([title, description]) => (
            <div key={title}>
              <dt>{title}</dt>
              <dd>{description}</dd>
            </div>
          ))}
        </dl>
      </div>

      <div className="card">
        <h2>Links úteis</h2>
        <ul className="link-list">
          <li>
            <a href="/api/docs">Swagger UI</a>
          </li>
          <li>
            <a href="/healthz">Health check</a>
          </li>
          <li>
            <a href="https://flask.palletsprojects.com/" rel="noreferrer">
              Documentação do Flask
            </a>
          </li>
          <li>
            <a href="https://vite.dev/" rel="noreferrer">
              Documentação do Vite
            </a>
          </li>
        </ul>
      </div>
    </section>
  );
}
