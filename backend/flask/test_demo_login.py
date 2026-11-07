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
    monkeypatch.delenv("FLASK_ENV", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    app = flask_app.create_app(TestConfig)
    with app.app_context():
        flask_app.db.create_all()
        yield app.test_client()


def login(client, email, password="password"):
    return client.post("/auth/login", json={"email": email, "password": password})


def test_other_email_rejected_and_not_created(client):
    assert login(client, "someone@else.com").status_code == 401
    from sqlalchemy import select
    assert flask_app.db.session.scalar(
        select(flask_app.User).where(flask_app.User.email == "someone@else.com")
    ) is None


def test_demo_email_ok(client):
    r = login(client, "user@example.com")
    assert r.status_code == 200
    assert r.get_json()["access_token"]


def test_wrong_password_rejected(client):
    assert login(client, "user@example.com", "nope").status_code == 401


def test_demo_email_override(client, monkeypatch):
    monkeypatch.setenv("DEMO_EMAIL", "demo@corp.example.com")
    assert login(client, "demo@corp.example.com").status_code == 200
    assert login(client, "user@example.com").status_code == 401


@pytest.mark.parametrize("value", ["false", "False", "FALSE", "0", "no", "off", " false "])
def test_disabled(client, monkeypatch, value):
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", value)
    assert login(client, "user@example.com").status_code == 401


def test_existing_mixed_case_demo_account_is_reused(client):
    user = flask_app.User(email="User@Example.com", name="user")
    flask_app.db.session.add(user)
    flask_app.db.session.commit()
    assert login(client, "user@example.com").status_code == 200
    from sqlalchemy import func, select
    count = flask_app.db.session.scalar(
        select(func.count()).select_from(flask_app.User).where(func.lower(flask_app.User.email) == "user@example.com")
    )
    assert count == 1


@pytest.mark.parametrize("var", ["FLASK_ENV", "APP_ENV"])
def test_off_by_default_in_production(client, monkeypatch, var):
    monkeypatch.setenv(var, "production")
    assert login(client, "user@example.com").status_code == 401


@pytest.mark.parametrize("value", ["true", "True", "1", "yes", "on", " ON "])
def test_production_with_explicit_enable(client, monkeypatch, value):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", value)
    assert login(client, "user@example.com").status_code == 200


def test_production_with_unrecognised_value_stays_off(client, monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEMO_LOGIN_ENABLED", "maybe")
    assert login(client, "user@example.com").status_code == 401


def test_development_stays_on(client, monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "development")
    assert login(client, "user@example.com").status_code == 200


@pytest.mark.parametrize(
    ("env", "expected"),
    [({}, "enabled"), ({"FLASK_ENV": "production"}, "disabled"),
     ({"APP_ENV": "production", "DEMO_LOGIN_ENABLED": "true"}, "enabled")],
)
def test_startup_line(monkeypatch, capsys, env, expected):
    for k in ("FLASK_ENV", "APP_ENV", "DEMO_LOGIN_ENABLED"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    flask_app.create_app(TestConfig)
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.startswith("Demo login")]
    assert lines == [f"Demo login: {expected}"]
