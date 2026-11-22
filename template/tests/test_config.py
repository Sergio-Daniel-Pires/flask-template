import pytest

from project.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_rejects_unknown_environment(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "prod")

    with pytest.raises(RuntimeError, match="FLASK_ENV"):
        get_settings()


def test_production_rejects_placeholder_secret(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("FLASK_SECRET_KEY", "change-me")

    with pytest.raises(RuntimeError, match="FLASK_SECRET_KEY"):
        get_settings()


def test_production_rejects_short_secret(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("FLASK_SECRET_KEY", "a" * 31)

    with pytest.raises(RuntimeError, match="FLASK_SECRET_KEY"):
        get_settings()


def test_production_accepts_strong_secret(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("FLASK_SECRET_KEY", "a" * 32)

    settings = get_settings()

    assert settings.env == "production"
    assert settings.debug is False
