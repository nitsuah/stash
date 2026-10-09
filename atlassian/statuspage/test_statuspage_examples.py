"""Smoke tests for Statuspage API examples using mocked HTTP responses."""

# ruff: noqa: E402

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import pytest
import requests
import responses
from client import StatuspageClient

# Load by path: every service has a module named "examples", so avoid sys.modules clashes.
_spec = importlib.util.spec_from_file_location(
    "statuspage_examples", os.path.join(HERE, "examples.py")
)
ex = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ex)

API = "https://api.statuspage.io/v1"
PAGE = f"{API}/pages/page123"


@pytest.fixture
def client():
    return StatuspageClient("dummy-api-key", "page123")


@pytest.fixture(autouse=True)
def mock_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_auth_header(mock_responses, client):
    mock_responses.add(responses.GET, f"{API}/pages", json=[])
    ex.list_pages(client)
    assert mock_responses.calls[0].request.headers["Authorization"] == "OAuth dummy-api-key"


def test_list_and_get_page(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{API}/pages", json=[
        {"id": "page123", "name": "Example Status", "subdomain": "example"},
    ])
    mock_responses.add(responses.GET, PAGE, json={"id": "page123", "name": "Example Status"})
    assert ex.list_pages(client)[0]["name"] == "Example Status"
    assert ex.get_page(client)["id"] == "page123"
    assert "Example Status" in capsys.readouterr().out


def test_list_components(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{PAGE}/components", json=[
        {"id": "c1", "name": "API", "status": "operational", "group": False},
    ])
    assert ex.list_components(client)[0]["id"] == "c1"
    assert "API" in capsys.readouterr().out


def test_component_lifecycle(mock_responses, client):
    mock_responses.add(responses.POST, f"{PAGE}/components", json={"id": "c2", "name": "Web"})
    mock_responses.add(responses.PATCH, f"{PAGE}/components/c2", json={
        "id": "c2", "name": "Web", "status": "major_outage",
    })
    mock_responses.add(responses.DELETE, f"{PAGE}/components/c2", body="", status=200)
    assert ex.create_component(client, "Web")["id"] == "c2"
    assert ex.update_component_status(client, "c2", "major_outage")["status"] == "major_outage"
    assert ex.delete_component(client, "c2") is True


def test_list_incidents_unresolved_vs_all(mock_responses, client):
    mock_responses.add(responses.GET, f"{PAGE}/incidents/unresolved", json=[
        {"id": "i1", "status": "investigating", "name": "Outage"},
    ])
    mock_responses.add(responses.GET, f"{PAGE}/incidents", json=[])
    assert len(ex.list_incidents(client)) == 1
    assert ex.list_incidents(client, status="all") == []


def test_get_incident(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{PAGE}/incidents/i1", json={
        "id": "i1", "name": "Outage", "status": "identified", "impact": "minor",
        "incident_updates": [{"status": "identified", "body": "Found it"}],
    })
    assert ex.get_incident(client, "i1")["status"] == "identified"
    assert "Found it" in capsys.readouterr().out


def test_incident_lifecycle(mock_responses, client):
    mock_responses.add(responses.POST, f"{PAGE}/incidents", json={
        "id": "i2", "name": "Degraded", "status": "investigating",
    })
    mock_responses.add(responses.PATCH, f"{PAGE}/incidents/i2", json={
        "id": "i2", "name": "Degraded", "status": "resolved",
    })
    mock_responses.add(responses.DELETE, f"{PAGE}/incidents/i2", body="", status=200)
    assert ex.create_incident(client, "Degraded", component_ids=["c1"])["id"] == "i2"
    assert b'"major_outage"' in mock_responses.calls[0].request.body
    assert ex.update_incident(client, "i2", "resolved")["status"] == "resolved"
    assert ex.delete_incident(client, "i2") is True


def test_list_scheduled_maintenances(mock_responses, client, capsys):
    mock_responses.add(responses.GET, f"{PAGE}/incidents/scheduled", json=[{
        "id": "m1", "status": "scheduled", "name": "DB upgrade",
        "scheduled_for": "2026-01-01T00:00:00Z", "scheduled_until": "2026-01-01T02:00:00Z",
    }])
    assert ex.list_scheduled_maintenances(client)[0]["id"] == "m1"
    assert "DB upgrade" in capsys.readouterr().out


def test_http_error_raises(mock_responses, client):
    mock_responses.add(responses.GET, f"{PAGE}/incidents/nope", json={}, status=404)
    with pytest.raises(requests.HTTPError):
        ex.get_incident(client, "nope")
