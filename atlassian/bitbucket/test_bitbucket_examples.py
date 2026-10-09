"""Smoke tests for Bitbucket Cloud API examples using mocked HTTP responses."""

# ruff: noqa: E402

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import pytest
import requests
import responses
from client import BitbucketClient

# Load by path: every service has a module named "examples", so avoid sys.modules clashes.
_spec = importlib.util.spec_from_file_location(
    "bitbucket_examples", os.path.join(HERE, "examples.py")
)
ex = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ex)

API = "https://api.bitbucket.org/2.0/repositories/example-ws"


@pytest.fixture
def client():
    return BitbucketClient("example-ws", "user@example.com", "dummy-app-password")


@pytest.fixture(autouse=True)
def mock_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_list_repos(mock_responses, client, capsys):
    mock_responses.add(responses.GET, API, json={
        "values": [{"slug": "demo-repo", "scm": "git", "is_private": True}],
    })
    result = ex.list_repos(client)
    assert result[0]["slug"] == "demo-repo"
    assert "demo-repo" in capsys.readouterr().out


def test_get_repo(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo", json={
        "full_name": "example-ws/demo-repo", "scm": "git",
        "is_private": False, "updated_on": "2026-01-01T00:00:00Z",
    })
    assert ex.get_repo(client, "demo-repo")["full_name"] == "example-ws/demo-repo"
    assert "example-ws/demo-repo" in capsys.readouterr().out


def test_create_and_delete_repo(mock_responses, client):
    mock_responses.add(responses.POST, f"{API}/demo-repo", json={"full_name": "example-ws/demo-repo"})
    mock_responses.add(responses.DELETE, f"{API}/demo-repo", body="", status=204)
    assert ex.create_repo(client, "demo-repo")["full_name"] == "example-ws/demo-repo"
    assert ex.delete_repo(client, "demo-repo") is True


def test_list_branches(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo/refs/branches", json={
        "values": [{"name": "main", "target": {"hash": "abcdef1234567890"}}],
    })
    assert ex.list_branches(client, "demo-repo")[0]["name"] == "main"
    assert "abcdef12" in capsys.readouterr().out


def test_list_commits(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo/commits/main", json={
        "values": [{
            "hash": "1234567890abcdef", "message": "Initial commit\nbody",
            "author": {"user": {"display_name": "Jane Doe"}},
        }],
    })
    assert len(ex.list_commits(client, "demo-repo")) == 1
    assert "Initial commit" in capsys.readouterr().out


def test_list_pull_requests(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo/pullrequests", json={
        "values": [{
            "id": 7, "title": "Add feature",
            "author": {"display_name": "Jane Doe"},
            "source": {"branch": {"name": "feature"}},
            "destination": {"branch": {"name": "main"}},
        }],
    })
    assert ex.list_pull_requests(client, "demo-repo")[0]["id"] == 7
    assert "Add feature" in capsys.readouterr().out


def test_get_and_create_pull_request(mock_responses, client):
    pr = {
        "id": 7, "title": "Add feature", "state": "OPEN",
        "author": {"display_name": "Jane Doe"},
        "source": {"branch": {"name": "feature"}},
        "destination": {"branch": {"name": "main"}},
    }
    mock_responses.add(responses.GET, f"{API}/demo-repo/pullrequests/7", json=pr)
    mock_responses.add(responses.POST, f"{API}/demo-repo/pullrequests", json=pr)
    assert ex.get_pull_request(client, "demo-repo", 7)["state"] == "OPEN"
    assert ex.create_pull_request(client, "demo-repo", "Add feature", "feature")["id"] == 7


def test_list_pipelines(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo/pipelines", json={
        "values": [{
            "build_number": 3, "state": {"name": "COMPLETED", "result": {"name": "SUCCESSFUL"}},
            "target": {"ref_name": "main"},
        }],
    })
    assert ex.list_pipelines(client, "demo-repo")[0]["build_number"] == 3
    assert "SUCCESSFUL" in capsys.readouterr().out


def test_list_pipelines_not_enabled(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo/pipelines", json={}, status=404)
    assert ex.list_pipelines(client, "demo-repo") == []
    assert "Not enabled" in capsys.readouterr().out


def test_trigger_pipeline(mock_responses, client):
    mock_responses.add(responses.POST, f"{API}/demo-repo/pipelines", json={"build_number": 4})
    assert ex.trigger_pipeline(client, "demo-repo")["build_number"] == 4


def test_list_issues_not_enabled(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo/issues", json={}, status=404)
    assert ex.list_issues(client, "demo-repo") == []
    assert "Not enabled" in capsys.readouterr().out


def test_issue_lifecycle(mock_responses, client):
    mock_responses.add(responses.GET, f"{API}/demo-repo/issues", json={
        "values": [{"id": 1, "status": "new", "title": "Bug"}],
    })
    mock_responses.add(responses.POST, f"{API}/demo-repo/issues", json={"id": 2})
    mock_responses.add(responses.DELETE, f"{API}/demo-repo/issues/2", body="", status=200)
    assert ex.list_issues(client, "demo-repo")[0]["id"] == 1
    assert ex.create_issue(client, "demo-repo", "Another bug")["id"] == 2
    assert ex.delete_issue(client, "demo-repo", 2) is True


def test_list_webhooks(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/demo-repo/hooks", json={
        "values": [{
            "uuid": "{abc}", "active": True,
            "url": "https://hooks.example.com/bb", "events": ["repo:push"],
        }],
    })
    assert len(ex.list_webhooks(client, "demo-repo")) == 1
    assert "repo:push" in capsys.readouterr().out


def test_http_error_raises(mock_responses, client):
    mock_responses.add(responses.GET, f"{API}/missing", json={}, status=404)
    with pytest.raises(requests.HTTPError):
        ex.get_repo(client, "missing")
