from pathlib import Path

import pytest

from project.app import create_app


@pytest.fixture()
def app():
    application = create_app(
        {
            "TESTING": True,
            "APP_PROFILE": "test",
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            # Keep API tests independent from a local `npm run build`.
            "FRONTEND_DIST": str(Path(__file__).parent / "_no_frontend"),
        }
    )
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()
