"""Regression tests for Jira validation no-op request guards."""

from unittest.mock import Mock

from atlassian.jira.validate_project import (
    Result,
    Status,
    Suite,
    comment_failures,
    transition_issue,
)


def test_transition_issue_without_matching_target_does_not_post():
    client = Mock()
    response = Mock()
    response.json.return_value = {
        "transitions": [{"id": "21", "to": {"name": "In Progress"}}],
    }
    client.get.return_value = response

    ok, message = transition_issue(client, "TEST-1", "Done")

    assert ok is False
    assert "No transition to 'Done' found" in message
    assert "In Progress" in message
    client.get.assert_called_once_with("/rest/api/3/issue/TEST-1/transitions")
    client.post.assert_not_called()


def test_comment_failures_does_not_post_for_clean_suite():
    client = Mock()
    suite = Suite("clean", results=[Result("validator", Status.PASS, "ok")])

    comment_failures(client, "TEST-1", suite)

    client.post.assert_not_called()
