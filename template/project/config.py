from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env once, without overriding real environment variables.
load_dotenv(BASE_DIR / ".env", override=False)


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    env: str
    debug: bool
    secret_key: str
    frontend_dist: Path

    @property
    def is_production(self) -> bool:
        return self.env == "production"


@lru_cache
def get_settings() -> Settings:
    env = os.getenv("FLASK_ENV", "development").strip().lower()
    debug = _env_bool("FLASK_DEBUG", env != "production")

    secret_key = os.getenv("FLASK_SECRET_KEY", "").strip()
    if not secret_key:
        if env == "production":
            raise RuntimeError("FLASK_SECRET_KEY must be set when FLASK_ENV=production")
        secret_key = "dev-only-insecure-secret-key"
        logging.getLogger(__name__).warning(
            "FLASK_SECRET_KEY is not set; using an insecure development key."
        )

    frontend_dist = Path(
        os.getenv("FRONTEND_DIST", str(BASE_DIR / "frontend" / "dist"))
    ).expanduser()

    return Settings(
        env=env,
        debug=debug,
        secret_key=secret_key,
        frontend_dist=frontend_dist,
    )
