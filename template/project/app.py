from __future__ import annotations

import tempfile
from pathlib import Path

from flask import Flask, abort, jsonify, send_from_directory
from flask_restx import Api

from project._version import __version__
from project.config import BASE_DIR, VALID_PROFILES, get_settings
[[#if database]]
from project.extensions import db
[[/endif]]
from project.services.echo.views import echo_ns
from project.services.home.views import home_ns

API_PREFIX = "/api"
MAX_CONTENT_LENGTH = 1 * 1024 * 1024


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory used by the dev server, Gunicorn and tests."""
    settings = get_settings()

    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        APP_PROFILE=settings.profile,
        DEBUG=settings.debug,
        TESTING=False,
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
        FRONTEND_DIST=str(settings.frontend_dist),
    )
    if test_config:
        app.config.update(test_config)

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        return response

    [[#if database]]
    database_uri = (test_config or {}).get("SQLALCHEMY_DATABASE_URI") or settings.database_url
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    _validate_database_profile(app, database_uri)
    db.init_app(app)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    with app.app_context():
        db.create_all()

    [[/endif]]
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

    _register_frontend(app, Path(app.config["FRONTEND_DIST"]))
    return app


def _validate_database_profile(app: Flask, database_uri: str) -> None:
    """Refuse to open the main database from a test or preview profile."""
    profile = str(app.config.get("APP_PROFILE", "demo")).strip().lower()
    if profile not in VALID_PROFILES:
        raise RuntimeError(f"APP_PROFILE must be one of {sorted(VALID_PROFILES)}")

    if profile == "demo":
        return

    if not database_uri:
        raise RuntimeError(f"APP_PROFILE={profile} requires an explicit SQLALCHEMY_DATABASE_URI")

    if not database_uri.startswith("sqlite:///"):
        if profile == "test":
            raise RuntimeError("APP_PROFILE=test requires a SQLite database")
        return

    raw_path = database_uri.removeprefix("sqlite:///")
    if raw_path == ":memory:" or raw_path.startswith("file::memory:"):
        return

    database_path = Path(raw_path)
    if not database_path.is_absolute():
        database_path = Path(app.instance_path) / database_path
    database_path = database_path.resolve()

    main_database = (BASE_DIR / "instance" / "app.db").resolve()
    if database_path == main_database:
        raise RuntimeError(
            f"APP_PROFILE={profile} cannot use the main database "
            f"({main_database}); use a separate test/preview database."
        )

    if profile == "test":
        temp_root = Path(tempfile.gettempdir()).resolve()
        if database_path != temp_root and temp_root not in database_path.parents:
            raise RuntimeError(
                "APP_PROFILE=test requires a database path inside the OS temp "
                f"directory ({temp_root})."
            )


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
