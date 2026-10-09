"""Smoke tests for Confluence Cloud API examples using mocked HTTP responses."""

# ruff: noqa: E402

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import pytest
import requests
import responses
from client import AtlassianClient

# Load by path: every service has a module named "examples", so avoid sys.modules clashes.
_spec = importlib.util.spec_from_file_location(
    "confluence_examples", os.path.join(HERE, "examples.py")
)
ex = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ex)

WIKI = "https://test.atlassian.net/wiki/rest/api"


@pytest.fixture
def client():
    return AtlassianClient("https://test.atlassian.net", "test@example.com", "test-token")


@pytest.fixture(autouse=True)
def mock_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_list_spaces(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{WIKI}/space", json={
        "results": [{"key": "DOCS", "name": "Documentation"}], "size": 1,
    })
    assert ex.list_spaces(client)[0]["key"] == "DOCS"
    assert "Documentation" in capsys.readouterr().out


def test_get_space(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{WIKI}/space/DOCS", json={
        "key": "DOCS", "name": "Documentation", "type": "global",
    })
    assert ex.get_space(client, "DOCS")["name"] == "Documentation"
    assert "DOCS" in capsys.readouterr().out


def test_list_pages_in_space(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{WIKI}/space/DOCS/content/page", json={
        "results": [{"id": "100", "title": "Home", "version": {"number": 2}}],
    })
    assert ex.list_pages_in_space(client, "DOCS")[0]["id"] == "100"
    assert "Home" in capsys.readouterr().out


def test_get_page(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{WIKI}/content/100", json={
        "id": "100", "title": "Home", "version": {"number": 2},
        "body": {"storage": {"value": "<p>hi</p>"}},
    })
    assert ex.get_page(client, "100")["title"] == "Home"
    assert "Body length: 9" in capsys.readouterr().out


def test_create_page(mock_responses, client):
    mock_responses.add(responses.POST, f"{WIKI}/content", json={"id": "101", "title": "New"})
    assert ex.create_page(client, "DOCS", "New", parent_id="100")["id"] == "101"
    assert b'"ancestors"' in mock_responses.calls[0].request.body


def test_update_page_bumps_version(mock_responses, client):
    mock_responses.add(responses.PUT, f"{WIKI}/content/101", json={
        "id": "101", "title": "New", "version": {"number": 3},
    })
    result = ex.update_page(client, "101", "New", "<p>x</p>", current_version=2)
    assert result["version"]["number"] == 3
    assert b'"number": 3' in mock_responses.calls[0].request.body


def test_delete_page(mock_responses, client):
    mock_responses.add(responses.DELETE, f"{WIKI}/content/101", body="", status=204)
    assert ex.delete_page(client, "101") is True


def test_delete_page_failure(mock_responses, client):
    mock_responses.add(responses.DELETE, f"{WIKI}/content/101", body="", status=403)
    assert ex.delete_page(client, "101") is False


def test_search_content(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{WIKI}/search", json={
        "results": [{"content": {"id": "100", "type": "page"}, "title": "Home"}],
        "totalSize": 1,
    })
    assert len(ex.search_content(client, 'type = page AND title ~ "Home"')) == 1
    assert "Home" in capsys.readouterr().out


def test_labels(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{WIKI}/content/100/label", json={
        "results": [{"name": "draft"}],
    })
    mock_responses.add(responses.POST, f"{WIKI}/content/100/label", json={
        "results": [{"name": "draft"}, {"name": "reviewed"}],
    })
    assert ex.get_page_labels(client, "100")[0]["name"] == "draft"
    assert len(ex.add_label(client, "100", "reviewed")["results"]) == 2
    assert "reviewed" in capsys.readouterr().out


def test_http_error_raises(mock_responses, client):
    mock_responses.add(responses.GET, f"{WIKI}/space/NOPE", json={}, status=404)
    with pytest.raises(requests.HTTPError):
        ex.get_space(client, "NOPE")
