"""Smoke tests for Jira Cloud API examples using mocked HTTP responses."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import responses
from client import AtlassianClient
from examples import (
    add_comment,
    create_customer_request,
    create_issue,
    delete_issue,
    get_issue,
    get_myself,
    get_project,
    get_transitions,
    list_asset_object_types,
    list_asset_schemas,
    list_automation_rules,
    list_custom_fields,
    list_issue_types,
    list_jsm_queues,
    list_projects,
    list_request_types,
    list_service_desks,
    list_users,
    search_assets,
    search_issues,
    transition_issue,
    update_issue,
)


@pytest.fixture
def client():
    """Create an AtlassianClient with dummy credentials for testing."""
    return AtlassianClient("https://test.atlassian.net", "test@example.com", "test-token")


@pytest.fixture(autouse=True)
def mock_responses():
    """Automatically enable responses mocking for all tests."""
    with responses.RequestsMock() as rsps:
        yield rsps


def mock_get(mock, path, json_data, status=200):
    """Helper to mock a GET request."""
    mock.add(responses.GET, f"https://test.atlassian.net{path}", json=json_data, status=status)


def mock_post(mock, path, json_data, status=200):
    """Helper to mock a POST request."""
    if status == 204:
        mock.add(responses.POST, f"https://test.atlassian.net{path}", body="", status=status)
    else:
        mock.add(responses.POST, f"https://test.atlassian.net{path}", json=json_data, status=status)


def mock_put(mock, path, json_data, status=200):
    """Helper to mock a PUT request."""
    if status == 204:
        mock.add(responses.PUT, f"https://test.atlassian.net{path}", body="", status=status)
    else:
        mock.add(responses.PUT, f"https://test.atlassian.net{path}", json=json_data, status=status)


def mock_delete(mock, path, status=204):
    """Helper to mock a DELETE request."""
    mock.add(responses.DELETE, f"https://test.atlassian.net{path}", body="", status=status)


# ── Jira Software / Core Tests ────────────────────────────────────────────

def test_list_projects(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/project/search", {
        "values": [{"key": "TEST", "name": "Test Project", "projectTypeKey": "software"}],
        "total": 1,
    })
    result = list_projects(client, max_results=10)
    assert len(result) == 1
    assert result[0]["key"] == "TEST"
    captured = capsys.readouterr()
    assert "Test Project" in captured.out


def test_get_project(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/project/TEST", {
        "key": "TEST",
        "name": "Test Project",
        "projectTypeKey": "software",
        "style": "classic",
        "lead": {"displayName": "John Doe"},
    })
    result = get_project(client, "TEST")
    assert result["key"] == "TEST"
    captured = capsys.readouterr()
    assert "Test Project" in captured.out


def test_list_issue_types(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/project/TEST", {
        "issueTypes": [
            {"name": "Task", "subtask": False},
            {"name": "Sub-task", "subtask": True},
        ],
    })
    result = list_issue_types(client, "TEST")
    assert len(result) == 2
    captured = capsys.readouterr()
    assert "Task" in captured.out


def test_create_issue(mock_responses, client, capsys):
    mock_post(mock_responses, "/rest/api/3/issue", {
        "key": "TEST-1",
        "fields": {"summary": "Test Issue"},
    })
    result = create_issue(client, "TEST", "Test Issue")
    assert result["key"] == "TEST-1"
    captured = capsys.readouterr()
    assert "Created Issue" in captured.out


def test_get_issue(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/issue/TEST-1", {
        "key": "TEST-1",
        "fields": {
            "summary": "Test Issue",
            "issuetype": {"name": "Task"},
            "status": {"name": "To Do"},
            "assignee": {"displayName": "John Doe"},
        },
    })
    result = get_issue(client, "TEST-1")
    assert result["key"] == "TEST-1"
    captured = capsys.readouterr()
    assert "Test Issue" in captured.out


def test_update_issue(mock_responses, client, capsys):
    mock_put(mock_responses, "/rest/api/3/issue/TEST-1", {}, status=204)
    update_issue(client, "TEST-1", summary="Updated Summary")
    captured = capsys.readouterr()
    assert "Updated" in captured.out


def test_delete_issue(mock_responses, client, capsys):
    mock_delete(mock_responses, "/rest/api/3/issue/TEST-1")
    result = delete_issue(client, "TEST-1")
    assert result is True
    captured = capsys.readouterr()
    assert "Deleted" in captured.out


def test_add_comment(mock_responses, client, capsys):
    mock_post(mock_responses, "/rest/api/3/issue/TEST-1/comment", {
        "id": "12345",
        "body": {"content": [{"content": [{"text": "Test comment"}]}]},
    })
    result = add_comment(client, "TEST-1", "Test comment")
    assert result["id"] == "12345"
    captured = capsys.readouterr()
    assert "Comment added" in captured.out


def test_search_issues(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/search", {
        "total": 2,
        "issues": [
            {"key": "TEST-1", "fields": {"summary": "Issue 1", "status": {"name": "To Do"}, "issuetype": {"name": "Task"}}},
            {"key": "TEST-2", "fields": {"summary": "Issue 2", "status": {"name": "Done"}, "issuetype": {"name": "Bug"}}},
        ],
    })
    result = search_issues(client, "project = TEST", max_results=5)
    assert len(result) == 2
    captured = capsys.readouterr()
    assert "Issue 1" in captured.out


def test_get_transitions(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/issue/TEST-1/transitions", {
        "transitions": [
            {"id": "21", "to": {"name": "In Progress"}},
            {"id": "31", "to": {"name": "Done"}},
        ],
    })
    result = get_transitions(client, "TEST-1")
    assert len(result) == 2
    captured = capsys.readouterr()
    assert "In Progress" in captured.out


def test_transition_issue(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/issue/TEST-1/transitions", {
        "transitions": [{"id": "21", "to": {"name": "In Progress"}}],
    })
    mock_post(mock_responses, "/rest/api/3/issue/TEST-1/transitions", {}, status=204)
    ok, msg = transition_issue(client, "TEST-1", "In Progress")
    assert ok is True
    assert msg == "In Progress"
    captured = capsys.readouterr()
    assert "Transition" in captured.out


def test_transition_issue_not_found(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/issue/TEST-1/transitions", {
        "transitions": [{"id": "21", "to": {"name": "In Progress"}}],
    })
    ok, msg = transition_issue(client, "TEST-1", "Done")
    assert ok is False
    assert "No transition to 'Done'" in msg


def test_list_custom_fields(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/field", [
        {"id": "customfield_10001", "name": "Story Points", "custom": True, "schema": {"type": "number"}},
        {"id": "summary", "name": "Summary", "custom": False},
    ])
    result = list_custom_fields(client)
    assert len(result) == 1
    assert result[0]["id"] == "customfield_10001"
    captured = capsys.readouterr()
    assert "Story Points" in captured.out


def test_list_users(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/users/search", [
        {"accountId": "12345", "displayName": "John Doe"},
    ])
    result = list_users(client, max_results=10)
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "John Doe" in captured.out


def test_get_myself(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/api/3/myself", {
        "displayName": "Test User",
        "emailAddress": "test@example.com",
        "accountId": "12345",
    })
    result = get_myself(client)
    assert result["displayName"] == "Test User"
    captured = capsys.readouterr()
    assert "Test User" in captured.out


# ── Jira Service Management Tests ────────────────────────────────────────

def test_list_service_desks(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/servicedeskapi/servicedesk", {
        "values": [
            {"id": "1", "projectKey": "SD", "projectName": "Service Desk"},
        ],
    })
    result = list_service_desks(client)
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "Service Desk" in captured.out


def test_list_request_types(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/servicedeskapi/servicedesk/1/requesttype", {
        "values": [
            {"id": "10", "name": "Get IT Help"},
        ],
    })
    result = list_request_types(client, "1")
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "Get IT Help" in captured.out


def test_list_jsm_queues(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/servicedeskapi/servicedesk/1/queue", {
        "values": [
            {"id": "5", "name": "Open Requests", "issueCount": 10},
        ],
    })
    result = list_jsm_queues(client, "1")
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "Open Requests" in captured.out


def test_create_customer_request(mock_responses, client, capsys):
    mock_post(mock_responses, "/rest/servicedeskapi/request", {
        "issueKey": "SD-1",
        "requestTypeId": "10",
    })
    result = create_customer_request(client, "1", "10", "Need help")
    assert result["issueKey"] == "SD-1"
    captured = capsys.readouterr()
    assert "JSM Request Created" in captured.out


# ── Jira Assets Tests ────────────────────────────────────────────────────

def test_list_asset_schemas(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/assets/1.0/objectschema/list", {
        "objectschemas": [
            {"id": "1", "name": "IT Assets", "objectCount": 100},
        ],
    })
    result = list_asset_schemas(client)
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "IT Assets" in captured.out


def test_list_asset_object_types(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/assets/1.0/objectschema/1/objecttypes/flat", [
        {"id": "5", "name": "Computer"},
        {"id": "6", "name": "Monitor"},
    ])
    result = list_asset_object_types(client, "1")
    assert len(result) == 2
    captured = capsys.readouterr()
    assert "Computer" in captured.out


def test_search_assets(mock_responses, client, capsys):
    mock_post(mock_responses, "/rest/assets/1.0/object/navlist/aql", {
        "objectEntries": [
            {"id": "100", "label": "Laptop-001"},
        ],
    })
    result = search_assets(client, 'objectType = "Computer"', max_results=10)
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "Laptop-001" in captured.out


# ── Jira Automation Tests ────────────────────────────────────────────────

def test_list_automation_rules(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/cb-automation/latest/project/TEST/rule/export", [
        {"id": "1", "name": "Auto-assign", "enabled": True},
        {"id": "2", "name": "SLAs", "enabled": False},
    ])
    result = list_automation_rules(client, "TEST")
    assert len(result) == 2
    captured = capsys.readouterr()
    assert "Auto-assign" in captured.out
    assert "SLAs" in captured.out


def test_list_automation_rules_not_available(mock_responses, client, capsys):
    mock_get(mock_responses, "/rest/cb-automation/latest/project/TEST/rule/export", {}, status=404)
    result = list_automation_rules(client, "TEST")
    assert result == []
    captured = capsys.readouterr()
    assert "admin scope required" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
