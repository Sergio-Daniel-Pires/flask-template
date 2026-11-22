import { NavLink, Outlet } from "react-router-dom";

import { PROJECT_NAME } from "../config";

function linkClass({ isActive }: { isActive: boolean }) {
  return isActive ? "nav-link active" : "nav-link";
}

export default function Layout() {
  return (
    <div className="app-shell">
      <header className="site-header">
        <NavLink to="/" className="brand">
          <span className="brand-mark" aria-hidden="true" />
          {PROJECT_NAME}
        </NavLink>

        <nav aria-label="Main navigation">
          <NavLink to="/" end className={linkClass}>
            Home
          </NavLink>
          <NavLink to="/echo" className={linkClass}>
            Echo
          </NavLink>
          [[#if database]]
          <NavLink to="/notes" className={linkClass}>
            Notes
          </NavLink>
          [[/endif]]
          <NavLink to="/about" className={linkClass}>
            About
          </NavLink>
        </nav>
      </header>

      <main className="site-main">
        <Outlet />
      </main>

      <footer className="site-footer">
        <span>{PROJECT_NAME}</span>
        <a href="/api/docs">API docs</a>
      </footer>
    </div>
  );
}
