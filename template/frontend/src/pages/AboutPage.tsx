import { PROJECT_NAME } from "../config";

const STACK = [
  ["Backend", "Flask 3 + Flask-RESTX, app factory and Swagger at /api/docs"],
  ["Frontend", "React 19 + Vite + TypeScript, with an /api proxy in development"],
  ["Tests", "pytest for the API and Playwright (headless Chromium) for the real flow"],
  ["Deploy", "Docker Compose on the VPS, triggered by GitHub Actions"],
];

export default function AboutPage() {
  return (
    <section className="stack narrow">
      <header>
        <p className="eyebrow">{PROJECT_NAME}</p>
        <h1>About</h1>
        <p className="lede">
          A lean starter for small projects, built to run on Windows and Linux
          without Docker in daily development.
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
        <h2>Useful links</h2>
        <ul className="link-list">
          <li>
            <a href="/api/docs">Swagger UI</a>
          </li>
          <li>
            <a href="/healthz">Health check</a>
          </li>
          <li>
            <a href="https://flask.palletsprojects.com/" rel="noreferrer">
              Flask documentation
            </a>
          </li>
          <li>
            <a href="https://vite.dev/" rel="noreferrer">
              Vite documentation
            </a>
          </li>
        </ul>
      </div>
    </section>
  );
}
