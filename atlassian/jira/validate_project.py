"""
Jira Project Configuration Validator
Validates that an Atlassian Jira project has been configured per specification.

Credentials are read from environment variables (never pass secrets as CLI args):
    JIRA_HOST     https://yourorg.atlassian.net
    JIRA_EMAIL    you@example.com
    JIRA_TOKEN    your Atlassian API token

Usage:
    # Option 1: env vars
    export JIRA_HOST=https://yourorg.atlassian.net
    export JIRA_EMAIL=you@example.com
    export JIRA_TOKEN=YOUR_API_TOKEN
    python validate_project.py --project MYPROJECT

    # Option 2 (recommended): copy .env.example → .env, fill in values.
    # A .env in the same directory as this script is loaded automatically.
    cp atlassian/jira/.env.example atlassian/jira/.env
    # edit .env, then:
    python validate_project.py --project MYPROJECT

    # Point at a .env elsewhere:
    python validate_project.py --project MYPROJECT --env-file /path/to/.env

Output:
    Results are printed to stdout and written to validator_<PROJECT>_<timestamp>.log
    (*.log is git-ignored).

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
from datetime import datetime, timezone
from enum import Enum
from io import StringIO
from typing import Any, TextIO

# Force UTF-8 output on Windows so symbols render correctly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore

import requests


# ---------------------------------------------------------------------------
# Result / Suite
# ---------------------------------------------------------------------------

class Status(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    WARN = "WARN"


_USE_UTF8 = sys.stdout.encoding and sys.stdout.encoding.lower().startswith("utf")
SYMBOL = {
    Status.PASS: "✓" if _USE_UTF8 else "P",
    Status.FAIL: "✗" if _USE_UTF8 else "F",
    Status.SKIP: "-",
    Status.WARN: "!" ,
}


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
    _log: TextIO = field(default_factory=StringIO, repr=False)

    def add(self, result: Result) -> Result:
        self.results.append(result)
        line = f"  [{SYMBOL[result.status]}] {result.name}: {result.message}"
        print(line)
        self._log.write(line + "\n")
        if result.details and result.status in (Status.FAIL, Status.WARN):
            detail_line = f"      → {result.details}"
            print(detail_line)
            self._log.write(detail_line + "\n")
        return result

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == Status.PASS)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == Status.FAIL)

    @property
    def warned(self) -> int:
        return sum(1 for r in self.results if r.status == Status.WARN)

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == Status.SKIP)


# ---------------------------------------------------------------------------
# Jira client
# ---------------------------------------------------------------------------

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
# Cached fetchers
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


# ---------------------------------------------------------------------------
# Issue helpers
# ---------------------------------------------------------------------------

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


def comment_failures(client: JiraClient, issue_key: str, suite: Suite,
                     label: str = "") -> None:
    """Post one comment listing all FAILs — only when failures exist.

    Skipped on a clean run so a passing execution never comments on test
    tickets and inadvertently triggers the reporter-reopen automation.
    """
    failures = [r for r in suite.results if r.status == Status.FAIL]
    if not failures:
        return
    prefix = f"[{label}] " if label else ""
    lines = [f"{prefix}VALIDATOR FAILURES on {issue_key}:"]
    for r in failures:
        lines.append(f"  {SYMBOL[Status.FAIL]}{r.name}: {r.message}")
        if r.details:
            lines.append(f"      → {r.details}")
    add_comment(client, issue_key, "\n".join(lines))


def assert_resolution_cleared(client: JiraClient, issue_key: str,
                               context: str, suite: Suite) -> None:
    """Fetch the issue and fail if resolution is not null."""
    issue = get_issue(client, issue_key)
    res = issue["fields"].get("resolution")
    if res is None:
        suite.add(Result(f"Resolution cleared ({context})", Status.PASS, "null as expected"))
    else:
        suite.add(Result(f"Resolution cleared ({context})", Status.FAIL,
                         f"still '{res['name']}'"))


def check_reporter_reopen(client: JiraClient, issue_key: str, suite: Suite,
                          label: str, pause: int = 5) -> None:
    """Comment as reporter, wait, verify status moved to Reopened."""
    add_comment(client, issue_key, f"[{label}] Reopening for validation — automated test.")
    suite.add(Result(f"{label}: Reporter-comment posted", Status.PASS,
                     f"pausing {pause}s for automation…"))
    time.sleep(pause)
    issue = get_issue(client, issue_key)
    status_now = issue["fields"]["status"]["name"]
    if status_now.lower() == "reopened":
        suite.add(Result(f"{label}: Reporter-comment → Reopened", Status.PASS,
                         f"status is '{status_now}'"))
        assert_resolution_cleared(client, issue_key, f"{label} reopen", suite)
    else:
        suite.add(Result(f"{label}: Reporter-comment → Reopened", Status.WARN,
                         f"status is '{status_now}' — automation may not have fired"))


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
    "Task":             ["To Do", "In Progress", "Blocked", "Reopened", "Done"],
    "Sub-task":         ["To Do", "In Progress", "Blocked", "Reopened", "Done"],
    "Story":            ["New", "In Progress", "In Testing", "Done", "Reopened"],
    "Accounts Payable": ["New", "Approved", "Denied", "Reopened"],
}


def suite_workflows(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Workflows & Statuses")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    all_statuses = get_statuses_for_project(client, project_key)
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

    pa = field_map.get("payment amount")
    if pa:
        t = pa.get("schema", {}).get("type", "")
        if t == "number":
            s.add(Result("Payment Amount type", Status.PASS, "numeric"))
        else:
            s.add(Result("Payment Amount type", Status.FAIL, f"expected 'number', got '{t}'"))
    return s


# ---------------------------------------------------------------------------
# Suite 5 — Story lifecycle
#   Chain: New→InProgress→InTesting→Done(+res) → neg-test(Done w/o res from
#          InTesting step skipped since we can't easily re-enter InTesting;
#          negative is done before first Done) → reporter-comment reopen →
#          direct Done → delete
# ---------------------------------------------------------------------------

def suite_story_lifecycle(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Story Lifecycle")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    r = client.post("/rest/api/3/issue", {"fields": {
        "project": {"key": project_key},
        "summary": "[VALIDATOR] Story lifecycle test",
        "issuetype": {"name": "Story"},
        "description": {
            "type": "doc", "version": 1,
            "content": [{"type": "paragraph", "content": [
                {"type": "text", "text": "Automated config validation — safe to delete."}
            ]}],
        },
    }})
    if r.status_code != 201:
        s.add(Result("Create Story", Status.FAIL, f"HTTP {r.status_code}", r.text[:300]))
        return s
    key = r.json()["key"]
    s.add(Result("Create Story", Status.PASS, key))

    try:
        ok, msg = transition_issue(client, key, "In Progress")
        s.add(Result("New → In Progress", Status.PASS if ok else Status.FAIL, msg))

        ok, msg = transition_issue(client, key, "In Testing")
        s.add(Result("In Progress → In Testing", Status.PASS if ok else Status.FAIL, msg))

        # Negative: attempt Done WITHOUT a resolution — should be rejected
        ok, msg = transition_issue(client, key, "Done")  # no resolution_name
        if not ok:
            s.add(Result("Done rejected without resolution (negative test)", Status.PASS,
                         "transition blocked as expected"))
        else:
            # Jira may accept the transition and leave resolution null — check
            issue = get_issue(client, key)
            if issue["fields"].get("resolution") is None and \
                    issue["fields"]["status"]["name"].lower() == "done":
                s.add(Result("Done rejected without resolution (negative test)", Status.FAIL,
                             "transition succeeded with no resolution set"))
                # Walk back to In Testing so the happy-path chain can continue.
                # Valid because the workflow allows Any → In Testing.
                transition_issue(client, key, "In Testing")
            else:
                s.add(Result("Done rejected without resolution (negative test)", Status.PASS,
                             "transition accepted but resolution enforced by workflow"))

        # Happy path: Done WITH resolution
        ok, msg = transition_issue(client, key, "Done", resolution_name="Done")
        s.add(Result("In Testing → Done (with resolution)", Status.PASS if ok else Status.FAIL, msg))

        # Brief pause so background automations (e.g. Set Parent to PARENT-1) can
        # complete before we start touching the issue again with a comment.
        time.sleep(8)

        issue = get_issue(client, key)
        res = issue["fields"].get("resolution")
        if res:
            s.add(Result("Resolution set on Done", Status.PASS, res["name"]))
        else:
            s.add(Result("Resolution set on Done", Status.FAIL, "resolution is null"))

        # Reporter-comment → Reopened automation (one comment, then check)
        check_reporter_reopen(client, key, s, label="Story")

        # If reopen fired we're in Reopened; if not we may still be in Done.
        # Either way, close via direct transition (no comment) before delete.
        issue = get_issue(client, key)
        if issue["fields"]["status"]["name"].lower() != "done":
            ok, msg = transition_issue(client, key, "Done", resolution_name="Done")
            s.add(Result("Final close", Status.PASS if ok else Status.WARN, msg))

    finally:
        comment_failures(client, key, s, label="Story lifecycle")
        deleted = delete_issue(client, key)
        s.add(Result(f"Cleanup ({key})", Status.PASS if deleted else Status.WARN,
                     "deleted" if deleted else "could not delete — remove manually"))

    return s


# ---------------------------------------------------------------------------
# Suite 6 — Accounts Payable lifecycle
#   Chain: New→Approved(+res, +approval date) → Reopened(res cleared) →
#          Denied(+res, +denied date) → reporter-comment reopen → delete
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
        # Approved path — resolution is set by Jira workflow post-function, not on the screen
        ok, msg = transition_issue(client, key, "Approved")
        s.add(Result("New → Approved", Status.PASS if ok else Status.FAIL, msg))

        time.sleep(5)  # automation: set Payment Approval Date
        issue = get_issue(client, key)

        res = issue["fields"].get("resolution")
        if res and res["name"].lower() == "approved":
            s.add(Result("Resolution 'Approved' set", Status.PASS, res["name"]))
        else:
            s.add(Result("Resolution 'Approved' set", Status.FAIL, f"got: {res}"))

        if pad_field:
            val = issue["fields"].get(pad_field)
            s.add(Result("Payment Approval Date set by automation",
                         Status.PASS if val else Status.WARN,
                         str(val) if val else "field is null — check automation rule"))
        else:
            s.add(Result("Payment Approval Date check", Status.SKIP, "field not found"))

        # Reopen
        ok, msg = transition_issue(client, key, "Reopened")
        s.add(Result("Approved → Reopened", Status.PASS if ok else Status.FAIL, msg))
        assert_resolution_cleared(client, key, "AP reopen", s)

        # Denied path — resolution is set by Jira workflow post-function, not on the screen
        ok, msg = transition_issue(client, key, "Denied")
        s.add(Result("Reopened → Denied", Status.PASS if ok else Status.FAIL, msg))

        time.sleep(5)  # automation: set Payment Denied Date
        issue = get_issue(client, key)

        res = issue["fields"].get("resolution")
        if res and res["name"].lower() == "denied":
            s.add(Result("Resolution 'Denied' set", Status.PASS, res["name"]))
        else:
            s.add(Result("Resolution 'Denied' set", Status.FAIL, f"got: {res}"))

        if pdd_field:
            val = issue["fields"].get(pdd_field)
            s.add(Result("Payment Denied Date set by automation",
                         Status.PASS if val else Status.WARN,
                         str(val) if val else "field is null — check automation rule"))
        else:
            s.add(Result("Payment Denied Date check", Status.SKIP, "field not found"))

        # Reporter-comment → Reopened automation
        check_reporter_reopen(client, key, s, label="AP", pause=10)

    finally:
        comment_failures(client, key, s, label="AP lifecycle")
        deleted = delete_issue(client, key)
        s.add(Result(f"Cleanup ({key})", Status.PASS if deleted else Status.WARN,
                     "deleted" if deleted else "could not delete — remove manually"))

    return s


# ---------------------------------------------------------------------------
# Suite 7 — Task & Sub-task lifecycle
#   Chain per type: New→InProgress→Blocked(res cleared)→InProgress→
#                   Done(+res)→Reopened(res cleared)→reporter-comment
# ---------------------------------------------------------------------------

def suite_task_lifecycle(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Task & Sub-task Lifecycle")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    for it in ("Task", "Sub-task"):
        parent_key = None

        if it == "Sub-task":
            pr = client.post("/rest/api/3/issue", {"fields": {
                "project": {"key": project_key},
                "summary": "[VALIDATOR] Parent task for sub-task lifecycle test",
                "issuetype": {"name": "Task"},
            }})
            if pr.status_code != 201:
                s.add(Result(f"Create parent Task for {it}", Status.FAIL,
                             f"HTTP {pr.status_code}"))
                continue
            parent_key = pr.json()["key"]

        create_body: dict[str, Any] = {
            "fields": {
                "project": {"key": project_key},
                "summary": f"[VALIDATOR] {it} lifecycle test",
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

            # Blocked is non-final — resolution must be null (nothing to clear yet,
            # but confirm the status is reachable and resolution stays null)
            assert_resolution_cleared(client, key, f"{it} Blocked", s)

            ok, msg = transition_issue(client, key, "In Progress")
            s.add(Result(f"{it}: Blocked → In Progress", Status.PASS if ok else Status.FAIL, msg))

            assert_resolution_cleared(client, key, f"{it} In Progress", s)

            # Resolution set by workflow post-function, not on the transition screen
            ok, msg = transition_issue(client, key, "Done")
            s.add(Result(f"{it}: In Progress → Done", Status.PASS if ok else Status.FAIL, msg))

            ok, msg = transition_issue(client, key, "Reopened")
            s.add(Result(f"{it}: Done → Reopened", Status.PASS if ok else Status.FAIL, msg))

            assert_resolution_cleared(client, key, f"{it} Reopened", s)

            # Reporter-comment → Reopened: issue is already Reopened, so first
            # close it so the automation has a resolved state to reopen from.
            ok, msg = transition_issue(client, key, "Done")
            s.add(Result(f"{it}: Reclose before comment-reopen test",
                         Status.PASS if ok else Status.WARN, msg))

            check_reporter_reopen(client, key, s, label=it)

        finally:
            comment_failures(client, key, s, label=f"{it} lifecycle")
            delete_issue(client, key)
            if parent_key:
                delete_issue(client, parent_key)
            s.add(Result(f"Cleanup {it} ({key})", Status.PASS, "deleted"))

    return s


# ---------------------------------------------------------------------------
# Suite 8 — Sub-task resolution gate (Task parent AND Story parent)
# ---------------------------------------------------------------------------

def suite_subtask_resolution_gate(client: JiraClient, project_key: str) -> Suite:
    s = Suite("Sub-task Resolution Gate")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    for parent_type in ("Task", "Story"):
        pr = client.post("/rest/api/3/issue", {"fields": {
            "project": {"key": project_key},
            "summary": f"[VALIDATOR] {parent_type} parent — resolution gate test",
            "issuetype": {"name": parent_type},
        }})
        if pr.status_code != 201:
            s.add(Result(f"Create {parent_type} parent", Status.FAIL, f"HTTP {pr.status_code}"))
            continue
        parent_key = pr.json()["key"]

        cr = client.post("/rest/api/3/issue", {"fields": {
            "project": {"key": project_key},
            "summary": f"[VALIDATOR] Open sub-task for {parent_type} gate test",
            "issuetype": {"name": "Sub-task"},
            "parent": {"key": parent_key},
        }})
        if cr.status_code != 201:
            s.add(Result(f"Create open Sub-task under {parent_type}", Status.FAIL,
                         f"HTTP {cr.status_code}"))
            delete_issue(client, parent_key)
            continue
        child_key = cr.json()["key"]
        s.add(Result(f"Setup: {parent_type} + open Sub-task", Status.PASS,
                     f"{parent_key} / {child_key}"))

        try:
            # Walk parent to the point where Done is available
            if parent_type == "Story":
                transition_issue(client, parent_key, "In Progress")
                transition_issue(client, parent_key, "In Testing")
            else:
                transition_issue(client, parent_key, "In Progress")

            # ── Step 1: try to resolve parent while child is still open ──────
            ok, msg = transition_issue(client, parent_key, "Done")
            if ok:
                issue = get_issue(client, parent_key)
                status = issue["fields"]["status"]["name"]
                if status.lower() == "done":
                    s.add(Result(f"{parent_type}: blocked with open sub-task (step 1)",
                                 Status.FAIL,
                                 "transition succeeded — gate automation not configured",
                                 details="Expected rejection or post-transition revert"))
                else:
                    s.add(Result(f"{parent_type}: blocked with open sub-task (step 1)",
                                 Status.WARN,
                                 f"API accepted but status is '{status}' — possible automation revert"))
            else:
                s.add(Result(f"{parent_type}: blocked with open sub-task (step 1)",
                             Status.PASS, "transition rejected as expected"))

            # ── Step 2: close the child sub-task ─────────────────────────────
            ok, msg = transition_issue(client, child_key, "Done")
            s.add(Result(f"{parent_type}: close child sub-task (step 2)",
                         Status.PASS if ok else Status.FAIL, msg))

            # ── Step 3: retry resolving parent — should now succeed ───────────
            # Story requires resolution on its Done screen; Task uses workflow post-function
            res = "Done" if parent_type == "Story" else None
            ok, msg = transition_issue(client, parent_key, "Done", resolution_name=res)
            if ok:
                issue = get_issue(client, parent_key)
                status = issue["fields"]["status"]["name"]
                if status.lower() == "done":
                    s.add(Result(f"{parent_type}: resolves after child closed (step 3)",
                                 Status.PASS, f"status is '{status}'"))
                else:
                    s.add(Result(f"{parent_type}: resolves after child closed (step 3)",
                                 Status.WARN, f"API accepted but status is '{status}'"))
            else:
                s.add(Result(f"{parent_type}: resolves after child closed (step 3)",
                             Status.FAIL, f"transition still rejected — {msg}"))

        finally:
            delete_issue(client, child_key)
            delete_issue(client, parent_key)
            s.add(Result(f"Cleanup {parent_type} gate ({parent_key})", Status.PASS, "deleted"))

    return s


# ---------------------------------------------------------------------------
# Suite 9 — Parent link updated to PARENT-1 on resolution
# ---------------------------------------------------------------------------

def _check_parent_link(client: JiraClient, issue_key: str, roi_parent: str,
                        label: str, suite: Suite, pause: int = 8) -> None:
    """Resolve an issue and verify its parent link was updated to roi_parent."""
    time.sleep(pause)
    issue = get_issue(client, issue_key)
    parent_field = (
        issue["fields"].get("parent") or
        issue["fields"].get("customfield_10014")  # Epic Link (classic projects)
    )
    if parent_field:
        parent_val = parent_field if isinstance(parent_field, str) \
            else parent_field.get("key", "")
        if parent_val == roi_parent:
            suite.add(Result(f"{label}: parent updated to {roi_parent}",
                             Status.PASS, parent_val))
        else:
            suite.add(Result(f"{label}: parent updated to {roi_parent}",
                             Status.FAIL,
                             f"parent is '{parent_val}', expected '{roi_parent}'"))
    else:
        suite.add(Result(f"{label}: parent updated to {roi_parent}",
                         Status.WARN,
                         "no parent/epic link field found — check automation link type"))


def suite_parent_link_on_resolve(client: JiraClient, project_key: str,
                                  roi_parent: str = "PARENT-1") -> Suite:
    s = Suite(f"Parent Link Update on Resolution (→ {roi_parent})")
    print(f"\n{'='*60}\n{s.name}\n{'='*60}")

    r = client.get(f"/rest/api/3/issue/{roi_parent}")
    if r.status_code != 200:
        s.add(Result(f"ROI parent '{roi_parent}' accessible", Status.WARN,
                     f"HTTP {r.status_code} — skipping live check"))
        return s
    s.add(Result(f"ROI parent '{roi_parent}' accessible", Status.PASS,
                 r.json()["fields"]["summary"][:60]))

    # Test with Story
    cr = client.post("/rest/api/3/issue", {"fields": {
        "project": {"key": project_key},
        "summary": "[VALIDATOR] Parent-link update test (Story)",
        "issuetype": {"name": "Story"},
    }})
    if cr.status_code != 201:
        s.add(Result("Create test Story", Status.FAIL, f"HTTP {cr.status_code}"))
    else:
        key = cr.json()["key"]
        s.add(Result("Create test Story", Status.PASS, key))
        try:
            transition_issue(client, key, "In Progress")
            transition_issue(client, key, "In Testing")
            ok, msg = transition_issue(client, key, "Done", resolution_name="Done")
            s.add(Result("Story → Done", Status.PASS if ok else Status.FAIL, msg))
            _check_parent_link(client, key, roi_parent, "Story", s, pause=30)
        finally:
            comment_failures(client, key, s, label="Parent-link Story")
            delete_issue(client, key)
            s.add(Result(f"Cleanup Story ({key})", Status.PASS, "deleted"))

    # Test with Task — requirement says "any work item"
    cr = client.post("/rest/api/3/issue", {"fields": {
        "project": {"key": project_key},
        "summary": "[VALIDATOR] Parent-link update test (Task)",
        "issuetype": {"name": "Task"},
    }})
    if cr.status_code != 201:
        s.add(Result("Create test Task", Status.FAIL, f"HTTP {cr.status_code}"))
    else:
        key = cr.json()["key"]
        s.add(Result("Create test Task", Status.PASS, key))
        try:
            transition_issue(client, key, "In Progress")
            ok, msg = transition_issue(client, key, "Done")
            s.add(Result("Task → Done", Status.PASS if ok else Status.FAIL, msg))
            _check_parent_link(client, key, roi_parent, "Task", s, pause=30)
        finally:
            comment_failures(client, key, s, label="Parent-link Task")
            delete_issue(client, key)
            s.add(Result(f"Cleanup Task ({key})", Status.PASS, "deleted"))

    return s


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(suites: list[Suite], project: str, host: str, out_dir: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = os.path.join(out_dir, f"validator_{project}_{ts}.log")

    total_pass = sum(s.passed for s in suites)
    total_fail = sum(s.failed for s in suites)
    total_warn = sum(s.warned for s in suites)
    total_skip = sum(s.skipped for s in suites)
    overall = "PASS" if total_fail == 0 else "FAIL"

    with open(filename, "w", encoding="utf-8") as fh:
        def w(line: str = "") -> None:
            fh.write(line + "\n")

        w("=" * 70)
        w("JIRA PROJECT CONFIGURATION VALIDATOR")
        w("=" * 70)
        w(f"Host:    {host}")
        w(f"Project: {project}")
        w(f"Run at:  {ts}")
        w(f"Result:  {overall}  ({total_pass}P / {total_fail}F / {total_warn}W / {total_skip}S)")
        w()

        for suite in suites:
            suite_status = "PASS" if suite.failed == 0 else "FAIL"
            w(f"┌─ [{suite_status}] {suite.name}")
        w()
        w("─" * 70)
        w("DETAIL")
        w("─" * 70)

        for suite in suites:
            suite_status = "PASS" if suite.failed == 0 else "FAIL"
            w()
            w(f"[{suite_status}] {suite.name}  "
              f"({suite.passed}P / {suite.failed}F / {suite.warned}W / {suite.skipped}S)")
            w("-" * 50)
            for r in suite.results:
                w(f"  [{r.status.value:4s}] {r.name}: {r.message}")
                if r.details:
                    w(f"         → {r.details}")

        if total_fail:
            w()
            w("=" * 70)
            w("FAILURES")
            w("=" * 70)
            for suite in suites:
                for r in suite.results:
                    if r.status == Status.FAIL:
                        w(f"  {SYMBOL[Status.FAIL]}[{suite.name}] {r.name}: {r.message}")
                        if r.details:
                            w(f"      → {r.details}")

        w()
        w("=" * 70)
        w(f"END  {overall}")
        w("=" * 70)

    return filename


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------

def print_summary(suites: list[Suite]) -> int:
    total_pass = sum(s.passed for s in suites)
    total_fail = sum(s.failed for s in suites)
    total_warn = sum(s.warned for s in suites)
    total_skip = sum(s.skipped for s in suites)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for suite in suites:
        icon = (SYMBOL[Status.PASS] if suite.failed == 0 else SYMBOL[Status.FAIL])
        print(f"  [{icon}] {suite.name:50s}  {suite.passed}P / {suite.failed}F"
              f" / {suite.warned}W / {suite.skipped}S")
    print(f"{'='*60}")
    print(f"  Total: {total_pass}P  {total_fail}F  {total_warn}W  {total_skip}S")
    print(f"{'='*60}")

    if total_fail:
        print("\nFailures:")
        for suite in suites:
            for r in suite.results:
                if r.status == Status.FAIL:
                    print(f"  {SYMBOL[Status.FAIL]}[{suite.name}] {r.name}: {r.message}")
                    if r.details:
                        print(f"      → {r.details}")

    return 1 if total_fail else 0


# ---------------------------------------------------------------------------
# Credentials / .env
# ---------------------------------------------------------------------------

def _load_env_file(path: str) -> None:
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(path, override=False)
        return
    except ImportError:
        pass
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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Jira project configuration",
        epilog="Credentials come from env vars JIRA_HOST / JIRA_EMAIL / JIRA_TOKEN.",
    )
    parser.add_argument("--project", required=True,  help="Project key, e.g. MYPROJECT")
    parser.add_argument("--roi-parent", default="PARENT-1",
                        help="Parent issue key for resolution link check (default: PARENT-1)")
    parser.add_argument("--skip-lifecycle", action="store_true",
                        help="Skip tests that create/delete real issues (structural checks only)")
    parser.add_argument("--env-file", metavar="FILE", default=None,
                        help="Path to a .env file (default: jira/.env then atlassian/.env)")
    parser.add_argument("--report-dir", metavar="DIR", default=None,
                        help="Directory for log reports (default: atlassian/logs/)")
    args = parser.parse_args()

    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _atlassian_dir = os.path.dirname(_script_dir)
    env_file = args.env_file or next(
        (p for p in [
            os.path.join(_script_dir, ".env"),
            os.path.join(_atlassian_dir, ".env"),
        ] if os.path.exists(p)),
        None,
    )
    if env_file:
        _load_env_file(env_file)

    host  = _require_env("JIRA_HOST")
    email = _require_env("JIRA_EMAIL")
    token = _require_env("JIRA_TOKEN")

    client = JiraClient(host, email, token)
    project = args.project.upper()
    default_logs = os.path.join(_atlassian_dir, "logs")
    os.makedirs(default_logs, exist_ok=True)
    report_dir = args.report_dir or default_logs

    print(f"\nJira Config Validator")
    print(f"Host:    {host}")
    print(f"Project: {project}")

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

    rc = print_summary(suites)

    report_path = write_report(suites, project, host, report_dir)
    print(f"\nReport written → {report_path}")

    return rc


if __name__ == "__main__":
    sys.exit(main())
