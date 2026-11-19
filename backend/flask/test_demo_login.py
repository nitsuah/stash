import os
import subprocess
import sys
from pathlib import Path

import app as flask_app
import pytest


class TestConfig(flask_app.Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "test-secret-" + "x" * 32


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.delenv("DEMO_EMAIL", raising=False)
    monkeypatch.delenv("DEMO_LOGIN_ENABLED", raising=False)
    monkeypatch.delenv("DEMO_PASSWORD", raising=False)
    monkeypatch.delenv("FLASK_ENV", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    app = flask_app.create_app(TestConfig)
    with app.app_context():
        flask_app.db.create_all()
        yield app.test_client()


@pytest.fixture()
def demo_on(monkeypatch):
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", "true")


def login(client, email, password="password"):
    return client.post("/auth/login", json={"email": email, "password": password})


def test_other_email_rejected_and_not_created(client, demo_on):
    assert login(client, "someone@else.com").status_code == 401
    from sqlalchemy import select
    assert flask_app.db.session.scalar(
        select(flask_app.User).where(flask_app.User.email == "someone@else.com")
    ) is None


def test_demo_email_ok(client, demo_on):
    r = login(client, "user@example.com")
    assert r.status_code == 200
    assert r.get_json()["access_token"]


def test_wrong_password_rejected(client, demo_on):
    assert login(client, "user@example.com", "nope").status_code == 401


def test_demo_email_override(client, demo_on, monkeypatch):
    monkeypatch.setenv("DEMO_EMAIL", "demo@corp.example.com")
    assert login(client, "demo@corp.example.com").status_code == 200
    assert login(client, "user@example.com").status_code == 401


def test_existing_mixed_case_demo_account_is_reused(client, demo_on):
    user = flask_app.User(email="User@Example.com", name="user")
    flask_app.db.session.add(user)
    flask_app.db.session.commit()
    assert login(client, "user@example.com").status_code == 200
    from sqlalchemy import func, select
    count = flask_app.db.session.scalar(
        select(func.count()).select_from(flask_app.User).where(func.lower(flask_app.User.email) == "user@example.com")
    )
    assert count == 1


def test_off_by_default_with_no_env(client):
    assert login(client, "user@example.com").status_code == 401


@pytest.mark.parametrize("value", ["", "false", "0", "yes", "on", "True", "TRUE", " true", "true ", "maybe"])
def test_only_exact_true_or_1_enables(client, monkeypatch, value):
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", value)
    assert login(client, "user@example.com").status_code == 401


@pytest.mark.parametrize("value", ["true", "1"])
def test_enabled_with_flag_regardless_of_env(client, monkeypatch, value):
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", value)
    for mode in ("development", "staging", ""):
        monkeypatch.setenv("FLASK_ENV", mode)
        assert login(client, "user@example.com").status_code == 200


@pytest.mark.parametrize("var", ["FLASK_ENV", "APP_ENV"])
def test_production_refuses_default_password(client, monkeypatch, var):
    monkeypatch.setenv(var, "production")
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", "true")
    assert login(client, "user@example.com").status_code == 401


def test_production_allows_custom_password(client, monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", "true")
    monkeypatch.setenv("DEMO_PASSWORD", "s3cret-demo-pw")
    assert login(client, "user@example.com", "s3cret-demo-pw").status_code == 200
    assert login(client, "user@example.com", "password").status_code == 401


def test_custom_password_outside_production(client, demo_on, monkeypatch):
    monkeypatch.setenv("DEMO_PASSWORD", "other-pw")
    assert login(client, "user@example.com", "other-pw").status_code == 200
    assert login(client, "user@example.com", "password").status_code == 401


@pytest.mark.parametrize(
    ("env", "expected"),
    [({}, "disabled"), ({"DEMO_LOGIN_ENABLED": "true"}, "enabled"),
     ({"DEMO_LOGIN_ENABLED": "true", "FLASK_ENV": "production"}, "disabled")],
)
def test_startup_line(monkeypatch, capsys, env, expected):
    for k in ("FLASK_ENV", "APP_ENV", "DEMO_LOGIN_ENABLED", "DEMO_PASSWORD"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    flask_app.create_app(TestConfig)
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.startswith("Demo login:")]
    assert lines == [f"Demo login: {expected}"]


def test_create_app_fails_without_jwt_secret():
    class NoSecret(TestConfig):
        JWT_SECRET_KEY = None

    with pytest.raises(RuntimeError, match="JWT_SECRET must be set"):
        flask_app.create_app(NoSecret)


def test_default_config_has_no_fallback_secret():
    env = {k: v for k, v in os.environ.items() if k != "JWT_SECRET"}
    env["DATABASE_URL"] = "sqlite://"
    code = "import app; app.create_app()"
    r = subprocess.run([sys.executable, "-c", code], cwd=Path(__file__).parent,
                       env=env, capture_output=True, text=True)
    assert r.returncode != 0
    assert "JWT_SECRET must be set" in r.stderr
