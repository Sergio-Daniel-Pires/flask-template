from __future__ import annotations

from pathlib import Path

from flask import Flask, abort, jsonify, send_from_directory
from flask_restx import Api

from project._version import __version__
from project.config import get_settings
from project.services.echo.views import echo_ns
from project.services.home.views import home_ns

API_PREFIX = "/api"


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory used by the dev server, Gunicorn and tests."""
    settings = get_settings()

    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        DEBUG=settings.debug,
        TESTING=False,
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    api = Api(
        title="[[ project_name ]] API",
        version=__version__,
        description="Flask backend with Swagger documentation.",
        doc=f"{API_PREFIX}/docs",
        prefix=API_PREFIX,
    )
    api.add_namespace(home_ns, path="/home")
    api.add_namespace(echo_ns, path="/echo")
    api.init_app(app)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "version": __version__}

    _register_frontend(app, settings.frontend_dist)
    return app


def _register_frontend(app: Flask, dist: Path) -> None:
    """Serve the Vite build in production and a helpful hint in development."""
    dist = dist.resolve()

    if not (dist / "index.html").is_file():

        @app.get("/")
        def frontend_not_built():
            return jsonify(
                {
                    "message": (
                        "Frontend not built. Run 'npm run build' inside frontend/ "
                        "or use the Vite dev server."
                    ),
                    "docs": f"{API_PREFIX}/docs",
                }
            )

        return

    @app.get("/", defaults={"path": ""})
    @app.get("/<path:path>")
    def spa(path: str):
        if path.startswith("api/"):
            return jsonify({"message": "Not found"}), 404
        if path == "healthz":
            abort(404)

        requested = (dist / path).resolve()
        if path and requested.is_file() and requested.is_relative_to(dist):
            response = send_from_directory(dist, path)
            if path.startswith("assets/"):
                response.cache_control.public = True
                response.cache_control.max_age = 31536000
            return response

        response = send_from_directory(dist, "index.html")
        response.cache_control.no_cache = True
        return response
