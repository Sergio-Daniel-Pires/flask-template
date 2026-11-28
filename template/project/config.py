from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

VALID_ENVS = frozenset({"development", "test", "production"})
VALID_PROFILES = frozenset({"demo", "preview", "test"})
MIN_PRODUCTION_SECRET_LENGTH = 32
INSECURE_SECRETS = frozenset(
    {
        "change-me",
        "changeme",
        "secret",
        "super secret key",
        "dev-only-insecure-secret-key",
    }
)

# Load .env once, without overriding real environment variables.
load_dotenv(BASE_DIR / ".env", override=False)


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_env() -> str:
    env = os.getenv("FLASK_ENV", "development").strip().lower()
    if env not in VALID_ENVS:
        raise RuntimeError(f"FLASK_ENV must be one of {sorted(VALID_ENVS)}; got {env!r}")
    return env


def _get_profile() -> str:
    profile = os.getenv("APP_PROFILE", "demo").strip().lower()
    if profile not in VALID_PROFILES:
        raise RuntimeError(f"APP_PROFILE must be one of {sorted(VALID_PROFILES)}; got {profile!r}")
    return profile


def _get_secret_key(env: str) -> str:
    secret_key = os.getenv("FLASK_SECRET_KEY", "").strip()

    if env == "production":
        if not secret_key:
            raise RuntimeError("FLASK_SECRET_KEY must be set when FLASK_ENV=production")
        if (
            secret_key.casefold() in INSECURE_SECRETS
            or len(secret_key) < MIN_PRODUCTION_SECRET_LENGTH
        ):
            raise RuntimeError(
                "FLASK_SECRET_KEY is too weak for production; use at least "
                f"{MIN_PRODUCTION_SECRET_LENGTH} characters and no placeholder."
            )
        return secret_key

    if not secret_key:
        logging.getLogger(__name__).warning(
            "FLASK_SECRET_KEY is not set; using an insecure development key."
        )
        return "dev-only-insecure-secret-key"

    if secret_key.casefold() in INSECURE_SECRETS or len(secret_key) < MIN_PRODUCTION_SECRET_LENGTH:
        logging.getLogger(__name__).warning(
            "FLASK_SECRET_KEY looks weak; this is acceptable only for development."
        )
    return secret_key


@dataclass(frozen=True)
class Settings:
    env: str
    profile: str
    debug: bool
    secret_key: str
    database_url: str
    frontend_dist: Path

    @property
    def is_production(self) -> bool:
        return self.env == "production"


@lru_cache
def get_settings() -> Settings:
    env = _get_env()
    profile = _get_profile()
    debug = _env_bool("FLASK_DEBUG", env == "development")
    secret_key = _get_secret_key(env)

    frontend_dist = Path(
        os.getenv("FRONTEND_DIST", str(BASE_DIR / "frontend" / "dist"))
    ).expanduser()

    default_database = BASE_DIR / "instance" / "app.db"
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{default_database.as_posix()}")

    return Settings(
        env=env,
        profile=profile,
        debug=debug,
        secret_key=secret_key,
        database_url=database_url,
        frontend_dist=frontend_dist,
    )
