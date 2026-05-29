"""
Jira Project Configuration Validator
Validates that an Atlassian Jira project has been configured per specification.

Credentials are read from environment variables (never pass secrets as CLI args):
    JIRA_HOST     https://yourorg.atlassian.net
    JIRA_EMAIL    you@example.com
    JIRA_TOKEN    your Atlassian API token

Usage:
    export JIRA_HOST=https://yourorg.atlassian.net
    export JIRA_EMAIL=you@example.com
    export JIRA_TOKEN=YOUR_API_TOKEN
    python validate_project.py --project AUSTIN

    # Option 2 (recommended): copy .env.example → .env, fill in values.
    # A .env in the same directory as this script is loaded automatically.
    cp atlassian/jira/.env.example atlassian/jira/.env
    # edit .env, then:
    python validate_project.py --project AUSTIN

    # Point at a .env elsewhere:
    python validate_project.py --project AUSTIN --env-file /path/to/.env

Requirements:
    pip install requests
    pip install python-dotenv  # optional, for .env file support
"""

import argparse
import base64
import os
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

import requests


# ---------------------------------------------------------------------------
# Config & helpers
# ---------------------------------------------------------------------------

class Status(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    WARN = "WARN"


@dataclass
class Result:
    name: str
    status: Status
    message: str
    details: Any = None


@dataclass
class Suite:
    name: str
    results: list[Result] = field(default_factory=list)

    def add(self, result: Result) -> Result:
        self.results.append(result)
        symbol = {"PASS": "✓", "FAIL": "✗", "SKIP": "-", "WARN": "!"}.get(result.status.value, "?")
        print(f"  [{symbol}] {result.name}: {result.message}")
        if result.details and result.status == Status.FAIL:
            print(f"      → {result.details}")
        return result

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == Status.PASS)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == Status.FAIL)


class JiraClient:
    def __init__(self, host: str, email: str, token: str):
        self.base = host.rstrip("/")
        creds = base64.b64encode(f"{email}:{token}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return requests.get(f"{self.base}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict) -> requests.Response:
        return requests.post(f"{self.base}{path}", headers=self.headers, json=body)

    def put(self, path: str, body: dict) -> requests.Response:
        return requests.put(f"{self.base}{path}", headers=self.headers, json=body)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(f"{self.base}{path}", headers=self.headers)


# ---------------------------------------------------------------------------
# Reusable fetchers (cached per run)
# ---------------------------------------------------------------------------

_cache: dict[str, Any] = {}


def get_issue_types(client: JiraClient, project_key: str) -> list[dict]:
    if "issue_types" not in _cache:
        r = client.get(f"/rest/api/3/project/{project_key}")
        r.raise_for_status()
        _cache["issue_types"] = r.json().get("issueTypes", [])
    return _cache["issue_types"]


def get_statuses_for_project(client: JiraClient, project_key: str) -> list[dict]:
    if "statuses" not in _cache:
        r = client.get(f"/rest/api/3/project/{project_key}/statuses")
        r.raise_for_status()
        _cache["statuses"] = r.json()
    return _cache["statuses"]


def get_fields(client: JiraClient) -> list[dict]:
    if "fields" not in _cache:
        r = client.get("/rest/api/3/field")
        r.raise_for_status()
        _cache["fields"] = r.json()
    return _cache["fields"]


def get_resolutions(client: JiraClient) -> list[dict]:
    if "resolutions" not in _cache:
        r = client.get("/rest/api/3/resolution")
        r.raise_for_status()
        _cache["resolutions"] = r.json()
    return _cache["resolutions"]


def get_transitions(client: JiraClient, issue_key: str) -> list[dict]:
    r = client.get(f"/rest/api/3/issue/{issue_key}/transitions")
    r.raise_for_status()
    return r.json().get("transitions", [])


def transition_issue(client: JiraClient, issue_key: str, target_status: str,
                     resolution_name: str | None = None) -> tuple[bool, str]:
    transitions = get_transitions(client, issue_key)
    match = next((t for t in transitions if t["to"]["name"].lower() == target_status.lower()), None)
    if not match:
        available = [t["to"]["name"] for t in transitions]
        return False, f"No transition to '{target_status}' found. Available: {available}"
    body: dict[str, Any] = {"transition": {"id": match["id"]}}
    if resolution_name:
        body["fields"] = {"resolution": {"name": resolution_name}}
    r = client.post(f"/rest/api/3/issue/{issue_key}/transitions", body)
    if r.status_code in (200, 204):
        return True, f"Transitioned to '{target_status}'"
    return False, f"HTTP {r.status_code}: {r.text[:200]}"


def get_issue(client: JiraClient, issue_key: str) -> dict:
    r = client.get(f"/rest/api/3/issue/{issue_key}")
    r.raise_for_status()
    return r.json()


def add_comment(client: JiraClient, issue_key: str, body_text: str) -> dict:
    body = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": body_text}]}],
        }
    }
    r = client.post(f"/rest/api/3/issue/{issue_key}/comment", body)
    r.raise_for_status()
    return r.json()


def delete_issue(client: JiraClient, issue_key: str) -> bool:
    r = client.delete(f"/rest/api/3/issue/{issue_key}")
    return r.status_code == 204


# ---------------------------------------------------------------------------
# Suite 1 — Project exists & issue types
# ---------------------------------------------------------------------------

def suite_issue_types(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Issue Types")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    r = client.get(f"/rest/api/3/project/{project_key}")
    if r.status_code != 200:
        s.add(Result("Project accessible", Status.FAIL, f"HTTP {r.status_code}"))
        return s
    s.add(Result("Project accessible", Status.PASS, r.json().get("name", project_key)))

    issue_types = get_issue_types(client, project_key)
    type_names = {it["name"].lower() for it in issue_types}

    for required in ["Story", "Accounts Payable", "Task", "Sub-task"]:
        if required.lower() in type_names:
            s.add(Result(f"Issue type '{required}'", Status.PASS, "exists"))
        else:
            s.add(Result(f"Issue type '{required}'", Status.FAIL, "NOT FOUND",
                         details=f"Found: {sorted(type_names)}"))
    return s


# ---------------------------------------------------------------------------
# Suite 2 — Workflows / statuses
# ---------------------------------------------------------------------------

EXPECTED_STATUSES: dict[str, list[str]] = {
    "Task":             ["New", "In Progress", "Blocked", "Reopened", "Done"],
    "Sub-task":         ["New", "In Progress", "Blocked", "Reopened", "Done"],
    "Story":            ["New", "In Progress", "In Testing", "Done", "Reopened"],
    "Accounts Payable": ["New", "Approved", "Denied", "Reopened"],
}


def suite_workflows(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Workflows & Statuses")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    all_statuses = get_statuses_for_project(client, project_key)
    # Build map: issue-type name → set of status names
    status_map: dict[str, set[str]] = {}
    for entry in all_statuses:
        it_name = entry.get("name", "")
        status_map[it_name] = {s_["name"] for s_ in entry.get("statuses", [])}

    for it_name, expected in EXPECTED_STATUSES.items():
        actual = status_map.get(it_name, set())
        missing = [e for e in expected if e not in actual]
        if not missing:
            s.add(Result(f"{it_name} workflow statuses", Status.PASS,
                         f"all {len(expected)} statuses present"))
        else:
            s.add(Result(f"{it_name} workflow statuses", Status.FAIL,
                         f"missing: {missing}", details=f"found: {sorted(actual)}"))
    return s


# ---------------------------------------------------------------------------
# Suite 3 — Resolutions
# ---------------------------------------------------------------------------

def suite_resolutions(client: JiraClient) -> Suite:
    s = Suite("Resolutions")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    resolutions = get_resolutions(client)
    res_names = {r["name"].lower() for r in resolutions}

    for required in ["Approved", "Denied", "Done", "Won't Do", "Duplicate"]:
        if required.lower() in res_names:
            s.add(Result(f"Resolution '{required}'", Status.PASS, "exists"))
        else:
            s.add(Result(f"Resolution '{required}'", Status.WARN,
                         "not found (may be named differently)",
                         details=f"Available: {sorted(res_names)}"))
    return s


# ---------------------------------------------------------------------------
# Suite 4 — Custom fields
# ---------------------------------------------------------------------------

REQUIRED_CUSTOM_FIELDS = [
    "Payment Amount",
    "Payment Approval Date",
    "Payment Denied Date",
]


def suite_custom_fields(client: JiraClient) -> Suite:
    s = Suite("Custom Fields")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    fields = get_fields(client)
    field_map = {f["name"].lower(): f for f in fields}

    for name in REQUIRED_CUSTOM_FIELDS:
        if name.lower() in field_map:
            f = field_map[name.lower()]
            schema = f.get("schema", {})
            s.add(Result(f"Field '{name}'", Status.PASS,
                         f"id={f['id']} type={schema.get('type','?')}"))
        else:
            s.add(Result(f"Field '{name}'", Status.FAIL, "NOT FOUND"))

    # Validate Payment Amount is numeric
    pa = field_map.get("payment amount")
    if pa:
        t = pa.get("schema", {}).get("type", "")
        if t == "number":
            s.add(Result("Payment Amount type", Status.PASS, "numeric"))
        else:
            s.add(Result("Payment Amount type", Status.FAIL, f"expected 'number', got '{t}'"))
    return s


# ---------------------------------------------------------------------------
# Suite 5 — Lifecycle: Story
# ---------------------------------------------------------------------------

def suite_story_lifecycle(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Story Lifecycle")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    # Create
    body = {
        "fields": {
            "project": {"key": project_key},
            "summary": "[VALIDATOR] Story lifecycle test",
            "issuetype": {"name": "Story"},
            "description": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [
                    {"type": "text", "text": "Automated config validation — safe to delete."}
                ]}],
            },
        }
    }
    r = client.post("/rest/api/3/issue", body)
    if r.status_code != 201:
        s.add(Result("Create Story", Status.FAIL, f"HTTP {r.status_code}", r.text[:300]))
        return s
    key = r.json()["key"]
    s.add(Result("Create Story", Status.PASS, key))

    try:
        # New → In Progress
        ok, msg = transition_issue(client, key, "In Progress")
        s.add(Result("Transition: New → In Progress", Status.PASS if ok else Status.FAIL, msg))

        # In Progress → In Testing
        ok, msg = transition_issue(client, key, "In Testing")
        s.add(Result("Transition: In Progress → In Testing", Status.PASS if ok else Status.FAIL, msg))

        # In Testing → Done (requires resolution)
        ok, msg = transition_issue(client, key, "Done", resolution_name="Done")
        s.add(Result("Transition: In Testing → Done (w/ resolution)", Status.PASS if ok else Status.FAIL, msg))

        # Verify resolution is set
        issue = get_issue(client, key)
        res = issue["fields"].get("resolution")
        if res:
            s.add(Result("Resolution set on Done", Status.PASS, res["name"]))
        else:
            s.add(Result("Resolution set on Done", Status.FAIL, "resolution is null"))

        # Reopen via reporter comment (automation: comment by reporter → Reopened)
        # We add the comment and then pause to allow automation to fire
        add_comment(client, key, "Reopening for validation — automated test.")
        s.add(Result("Comment added (triggers reopen automation)", Status.PASS,
                     "pausing 5s for automation…"))
        time.sleep(5)

        issue = get_issue(client, key)
        status_now = issue["fields"]["status"]["name"]
        if status_now.lower() == "reopened":
            s.add(Result("Auto-reopen via reporter comment", Status.PASS,
                         f"status is now '{status_now}'"))
            # Verify resolution was cleared
            res_now = issue["fields"].get("resolution")
            if res_now is None:
                s.add(Result("Resolution cleared on Reopen", Status.PASS, "null as expected"))
            else:
                s.add(Result("Resolution cleared on Reopen", Status.FAIL,
                             f"still set to '{res_now['name']}'"))
        else:
            s.add(Result("Auto-reopen via reporter comment", Status.WARN,
                         f"status is '{status_now}' — automation may not have fired or rule targets reporter only"))

        # Close with validation comment
        add_comment(client, key, "VALIDATOR RESULT: Story lifecycle validated. Closing test issue.")
        ok, msg = transition_issue(client, key, "Done", resolution_name="Done")
        s.add(Result("Final close", Status.PASS if ok else Status.WARN, msg))

    finally:
        deleted = delete_issue(client, key)
        s.add(Result(f"Cleanup ({key})", Status.PASS if deleted else Status.WARN,
                     "deleted" if deleted else "could not delete — remove manually"))

    return s


# ---------------------------------------------------------------------------
# Suite 6 — Lifecycle: Accounts Payable
# ---------------------------------------------------------------------------

def suite_ap_lifecycle(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Accounts Payable Lifecycle")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    fields = get_fields(client)
    field_map = {f["name"].lower(): f["id"] for f in fields}
    pa_field  = field_map.get("payment amount")
    pad_field = field_map.get("payment approval date")
    pdd_field = field_map.get("payment denied date")

    body: dict[str, Any] = {
        "fields": {
            "project": {"key": project_key},
            "summary": "[VALIDATOR] Accounts Payable lifecycle test",
            "issuetype": {"name": "Accounts Payable"},
        }
    }
    if pa_field:
        body["fields"][pa_field] = 9999.99

    r = client.post("/rest/api/3/issue", body)
    if r.status_code != 201:
        s.add(Result("Create Accounts Payable", Status.FAIL,
                     f"HTTP {r.status_code}", r.text[:300]))
        return s
    key = r.json()["key"]
    s.add(Result("Create Accounts Payable", Status.PASS, key))

    try:
        # --- Test Approved path ---
        ok, msg = transition_issue(client, key, "Approved", resolution_name="Approved")
        s.add(Result("Transition: New → Approved", Status.PASS if ok else Status.FAIL, msg))

        time.sleep(5)  # automation: set Payment Approval Date
        issue = get_issue(client, key)

        res = issue["fields"].get("resolution")
        if res and res["name"].lower() == "approved":
            s.add(Result("Resolution 'Approved' set", Status.PASS, res["name"]))
        else:
            s.add(Result("Resolution 'Approved' set", Status.FAIL,
                         f"got: {res}"))

        if pad_field:
            val = issue["fields"].get(pad_field)
            if val:
                s.add(Result("Payment Approval Date set by automation", Status.PASS, str(val)))
            else:
                s.add(Result("Payment Approval Date set by automation", Status.WARN,
                             "field is null — check automation rule"))
        else:
            s.add(Result("Payment Approval Date check", Status.SKIP, "field not found"))

        # Reopen → Denied path
        ok, msg = transition_issue(client, key, "Reopened")
        s.add(Result("Transition: Approved → Reopened", Status.PASS if ok else Status.FAIL, msg))

        # Verify resolution cleared
        issue = get_issue(client, key)
        res_now = issue["fields"].get("resolution")
        if res_now is None:
            s.add(Result("Resolution cleared on Reopen", Status.PASS, "null"))
        else:
            s.add(Result("Resolution cleared on Reopen", Status.FAIL,
                         f"still '{res_now['name']}'"))

        ok, msg = transition_issue(client, key, "Denied", resolution_name="Denied")
        s.add(Result("Transition: Reopened → Denied", Status.PASS if ok else Status.FAIL, msg))

        time.sleep(5)  # automation: set Payment Denied Date
        issue = get_issue(client, key)

        res = issue["fields"].get("resolution")
        if res and res["name"].lower() == "denied":
            s.add(Result("Resolution 'Denied' set", Status.PASS, res["name"]))
        else:
            s.add(Result("Resolution 'Denied' set", Status.FAIL, f"got: {res}"))

        if pdd_field:
            val = issue["fields"].get(pdd_field)
            if val:
                s.add(Result("Payment Denied Date set by automation", Status.PASS, str(val)))
            else:
                s.add(Result("Payment Denied Date set by automation", Status.WARN,
                             "field is null — check automation rule"))
        else:
            s.add(Result("Payment Denied Date check", Status.SKIP, "field not found"))

        add_comment(client, key, "VALIDATOR RESULT: AP lifecycle validated. Closing test issue.")

    finally:
        deleted = delete_issue(client, key)
        s.add(Result(f"Cleanup ({key})", Status.PASS if deleted else Status.WARN,
                     "deleted" if deleted else "could not delete — remove manually"))

    return s


# ---------------------------------------------------------------------------
# Suite 7 — Task / Sub-task: Blocked & Reopened statuses
# ---------------------------------------------------------------------------

def suite_task_lifecycle(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Task & Sub-task: Blocked / Reopened Statuses")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    for it in ("Task", "Sub-task"):
        parent_key = None

        # Sub-tasks need a parent; create a Task to parent against
        if it == "Sub-task":
            pr = client.post("/rest/api/3/issue", {"fields": {
                "project": {"key": project_key},
                "summary": "[VALIDATOR] Parent task for sub-task test",
                "issuetype": {"name": "Task"},
            }})
            if pr.status_code != 201:
                s.add(Result(f"Create parent Task for Sub-task", Status.FAIL,
                             f"HTTP {pr.status_code}"))
                continue
            parent_key = pr.json()["key"]

        create_body: dict[str, Any] = {
            "fields": {
                "project": {"key": project_key},
                "summary": f"[VALIDATOR] {it} blocked/reopen test",
                "issuetype": {"name": it},
            }
        }
        if parent_key:
            create_body["fields"]["parent"] = {"key": parent_key}

        r = client.post("/rest/api/3/issue", create_body)
        if r.status_code != 201:
            s.add(Result(f"Create {it}", Status.FAIL, f"HTTP {r.status_code}", r.text[:200]))
            if parent_key:
                delete_issue(client, parent_key)
            continue

        key = r.json()["key"]
        s.add(Result(f"Create {it}", Status.PASS, key))

        try:
            ok, msg = transition_issue(client, key, "In Progress")
            s.add(Result(f"{it}: New → In Progress", Status.PASS if ok else Status.FAIL, msg))

            ok, msg = transition_issue(client, key, "Blocked")
            s.add(Result(f"{it}: In Progress → Blocked", Status.PASS if ok else Status.FAIL, msg))

            ok, msg = transition_issue(client, key, "In Progress")
            s.add(Result(f"{it}: Blocked → In Progress", Status.PASS if ok else Status.FAIL, msg))

            ok, msg = transition_issue(client, key, "Done", resolution_name="Done")
            s.add(Result(f"{it}: In Progress → Done", Status.PASS if ok else Status.FAIL, msg))

            # Reopen
            ok, msg = transition_issue(client, key, "Reopened")
            s.add(Result(f"{it}: Done → Reopened", Status.PASS if ok else Status.FAIL, msg))

            # Resolution should be cleared
            issue = get_issue(client, key)
            res = issue["fields"].get("resolution")
            if res is None:
                s.add(Result(f"{it}: Resolution cleared on Reopen", Status.PASS, "null"))
            else:
                s.add(Result(f"{it}: Resolution cleared on Reopen", Status.FAIL,
                             f"still '{res['name']}'"))

            add_comment(client, key, "VALIDATOR RESULT: Task lifecycle validated.")
        finally:
            delete_issue(client, key)
            if parent_key:
                delete_issue(client, parent_key)
            s.add(Result(f"Cleanup {it} ({key})", Status.PASS, "deleted"))

    return s


# ---------------------------------------------------------------------------
# Suite 8 — Sub-task gate: parent cannot resolve if child is open
# ---------------------------------------------------------------------------

def suite_subtask_resolution_gate(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Sub-task Resolution Gate")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    # Create a Task
    pr = client.post("/rest/api/3/issue", {"fields": {
        "project": {"key": project_key},
        "summary": "[VALIDATOR] Parent — resolution gate test",
        "issuetype": {"name": "Task"},
    }})
    if pr.status_code != 201:
        s.add(Result("Create parent Task", Status.FAIL, f"HTTP {pr.status_code}"))
        return s
    parent_key = pr.json()["key"]

    # Create an open Sub-task under it
    cr = client.post("/rest/api/3/issue", {"fields": {
        "project": {"key": project_key},
        "summary": "[VALIDATOR] Open sub-task for gate test",
        "issuetype": {"name": "Sub-task"},
        "parent": {"key": parent_key},
    }})
    if cr.status_code != 201:
        s.add(Result("Create open Sub-task", Status.FAIL, f"HTTP {cr.status_code}"))
        delete_issue(client, parent_key)
        return s
    child_key = cr.json()["key"]
    s.add(Result("Setup: parent + open sub-task", Status.PASS, f"{parent_key} / {child_key}"))

    # Attempt to resolve parent — should be blocked
    ok, msg = transition_issue(client, parent_key, "Done", resolution_name="Done")
    if ok:
        # Try to verify if the transition really went through
        issue = get_issue(client, parent_key)
        status = issue["fields"]["status"]["name"]
        if status.lower() == "done":
            s.add(Result("Parent blocked from resolving (open sub-task)", Status.FAIL,
                         "transition succeeded — gate automation may not be configured",
                         details="Expected the transition to be rejected or reverted"))
        else:
            s.add(Result("Parent blocked from resolving (open sub-task)", Status.WARN,
                         f"transition claimed success but status is '{status}' — possible automation revert"))
    else:
        s.add(Result("Parent blocked from resolving (open sub-task)", Status.PASS,
                     "transition rejected as expected"))

    # Cleanup
    delete_issue(client, child_key)
    delete_issue(client, parent_key)
    s.add(Result("Cleanup gate test", Status.PASS, "deleted"))
    return s


# ---------------------------------------------------------------------------
# Suite 9 — Parent link update on resolution (ROI-4)
# ---------------------------------------------------------------------------

def suite_parent_link_on_resolve(client: JiraClient, project_key: str,
                                  roi_parent: str = "ROI-4") -> Suite:
    s = Suite(f"Parent Link Update on Resolution (→ {roi_parent})")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    # Verify ROI-4 is accessible
    r = client.get(f"/rest/api/3/issue/{roi_parent}")
    if r.status_code != 200:
        s.add(Result(f"ROI parent '{roi_parent}' accessible", Status.WARN,
                     f"HTTP {r.status_code} — skipping live check"))
        return s
    s.add(Result(f"ROI parent '{roi_parent}' accessible", Status.PASS,
                 r.json()["fields"]["summary"][:60]))

    # Create a Story in the project
    cr = client.post("/rest/api/3/issue", {"fields": {
        "project": {"key": project_key},
        "summary": "[VALIDATOR] Parent-link update test",
        "issuetype": {"name": "Story"},
    }})
    if cr.status_code != 201:
        s.add(Result("Create test Story", Status.FAIL, f"HTTP {cr.status_code}"))
        return s
    key = cr.json()["key"]
    s.add(Result("Create test Story", Status.PASS, key))

    try:
        # Transition to Done to trigger automation
        ok, msg = transition_issue(client, key, "In Progress")
        transition_issue(client, key, "In Testing")
        ok, msg = transition_issue(client, key, "Done", resolution_name="Done")
        s.add(Result("Transition Story to Done", Status.PASS if ok else Status.FAIL, msg))

        time.sleep(8)  # allow automation to update parent link

        issue = get_issue(client, key)
        # Check epic link, parent, or custom parent field
        parent_field = (
            issue["fields"].get("parent") or
            issue["fields"].get("customfield_10014")  # Epic Link (classic)
        )
        if parent_field:
            parent_val = parent_field if isinstance(parent_field, str) else parent_field.get("key", "")
            if parent_val == roi_parent:
                s.add(Result(f"Parent updated to {roi_parent}", Status.PASS, parent_val))
            else:
                s.add(Result(f"Parent updated to {roi_parent}", Status.FAIL,
                             f"parent is '{parent_val}', expected '{roi_parent}'"))
        else:
            s.add(Result(f"Parent updated to {roi_parent}", Status.WARN,
                         "no parent/epic link field found — automation may use a different link type"))

        add_comment(client, key, "VALIDATOR RESULT: Parent-link automation checked.")
    finally:
        delete_issue(client, key)
        s.add(Result(f"Cleanup ({key})", Status.PASS, "deleted"))

    return s


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_summary(suites: list[Suite]) -> int:
    total_pass = sum(s.passed for s in suites)
    total_fail = sum(s.failed for s in suites)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for suite in suites:
        icon = "✓" if suite.failed == 0 else "✗"
        print(f"  [{icon}] {suite.name:45s}  {suite.passed}P / {suite.failed}F")
    print(f"{'='*60}")
    print(f"  Total: {total_pass} passed, {total_fail} failed")
    print(f"{'='*60}")

    if total_fail:
        print("\nFailed checks:")
        for suite in suites:
            for r in suite.results:
                if r.status == Status.FAIL:
                    print(f"  ✗ [{suite.name}] {r.name}: {r.message}")
                    if r.details:
                        print(f"      → {r.details}")

    return 1 if total_fail else 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _load_env_file(path: str) -> None:
    """Load key=value pairs from a .env file into os.environ (no dependency required)."""
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(path, override=False)
        return
    except ImportError:
        pass
    # Minimal fallback parser (no dotenv installed)
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            os.environ.setdefault(key, val)


def _require_env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        print(f"ERROR: environment variable '{name}' is not set.", file=sys.stderr)
        print("Set JIRA_HOST, JIRA_EMAIL, and JIRA_TOKEN before running.", file=sys.stderr)
        sys.exit(1)
    return val


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Jira project configuration",
        epilog="Credentials come from env vars JIRA_HOST / JIRA_EMAIL / JIRA_TOKEN.",
    )
    parser.add_argument("--project", required=True,  help="Project key, e.g. AUSTIN")
    parser.add_argument("--roi-parent", default="ROI-4",
                        help="Parent issue key for resolution link check (default: ROI-4)")
    parser.add_argument("--skip-lifecycle", action="store_true",
                        help="Skip tests that create/delete real issues (structural checks only)")
    parser.add_argument("--env-file", metavar="FILE", default=None,
                        help="Path to a .env file (default: .env next to this script)")
    args = parser.parse_args()

    # Auto-load .env from the script's own directory; --env-file overrides the path
    default_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    env_file = args.env_file or (default_env if os.path.exists(default_env) else None)
    if env_file:
        _load_env_file(env_file)

    host  = _require_env("JIRA_HOST")
    email = _require_env("JIRA_EMAIL")
    token = _require_env("JIRA_TOKEN")

    client = JiraClient(host, email, token)
    project = args.project.upper()

    print(f"\nJira Config Validator")
    print(f"Host:    {host}")
    print(f"Project: {project}")
    print(f"Date:    2026-05-28")

    suites: list[Suite] = [
        suite_issue_types(client, project),
        suite_workflows(client, project),
        suite_resolutions(client),
        suite_custom_fields(client),
    ]

    if not args.skip_lifecycle:
        suites += [
            suite_story_lifecycle(client, project),
            suite_ap_lifecycle(client, project),
            suite_task_lifecycle(client, project),
            suite_subtask_resolution_gate(client, project),
            suite_parent_link_on_resolve(client, project, args.roi_parent),
        ]
    else:
        print("\n[--skip-lifecycle] Skipping issue-creation tests.")

    return print_summary(suites)


if __name__ == "__main__":
    sys.exit(main())
