import tempfile
from pathlib import Path

import pytest

from project.app import create_app
from project.config import BASE_DIR

MAIN_DATABASE = (BASE_DIR / "instance" / "app.db").as_posix()


def test_test_profile_rejects_main_database():
    with pytest.raises(RuntimeError, match="main database"):
        create_app(
            {
                "APP_PROFILE": "test",
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{MAIN_DATABASE}",
            }
        )


def test_preview_profile_rejects_main_database():
    with pytest.raises(RuntimeError, match="main database"):
        create_app(
            {
                "APP_PROFILE": "preview",
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{MAIN_DATABASE}",
            }
        )


def test_test_profile_rejects_non_temp_database():
    outside_temp = (Path(tempfile.gettempdir()).parent / "not-in-temp.db").as_posix()

    with pytest.raises(RuntimeError, match="temp directory"):
        create_app(
            {
                "APP_PROFILE": "test",
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{outside_temp}",
            }
        )


def test_test_profile_accepts_memory_database():
    app = create_app(
        {
            "APP_PROFILE": "test",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    assert app.config["APP_PROFILE"] == "test"


def test_test_profile_accepts_temp_database(tmp_path):
    database = tmp_path / "e2e.db"

    app = create_app(
        {
            "APP_PROFILE": "test",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database.as_posix()}",
        }
    )

    assert app.config["APP_PROFILE"] == "test"
