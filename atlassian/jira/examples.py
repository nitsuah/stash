"""
Jira Cloud API Examples
Covers: Jira Software / Core, Jira Service Management (JSM), Jira Assets

Auth:  JIRA_HOST, JIRA_EMAIL, JIRA_TOKEN  (env vars or atlassian/.env)
Docs:  https://developer.atlassian.com/cloud/jira/platform/rest/v3/
       https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-servicedesk/
       https://developer.atlassian.com/cloud/assets/rest/

Usage:
    # Read-only demo (safe — no issues created):
    python atlassian/jira/examples.py --project MYPROJECT

    # Include write operations (creates then deletes a test issue):
    python atlassian/jira/examples.py --project MYPROJECT --demo-write
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import AtlassianClient, load_env


# ---------------------------------------------------------------------------
# Jira Software / Core
# ---------------------------------------------------------------------------

def list_projects(client: AtlassianClient, max_results: int = 10) -> list[dict]:
    """GET /rest/api/3/project/search"""
    r = client.get("/rest/api/3/project/search", params={"maxResults": max_results})
    r.raise_for_status()
    projects = r.json().get("values", [])
    print(f"\n[Projects] {len(projects)} returned (of {r.json().get('total', '?')} total):")
    for p in projects:
        print(f"  {p['key']:12s}  {p['name']}  ({p.get('projectTypeKey', '')})")
    return projects


def get_project(client: AtlassianClient, project_key: str) -> dict:
    """GET /rest/api/3/project/{projectKey}"""
    r = client.get(f"/rest/api/3/project/{project_key}")
    r.raise_for_status()
    p = r.json()
    print(f"\n[Project] {p['key']}: {p['name']}")
    print(f"  Type: {p.get('projectTypeKey')}  Style: {p.get('style','?')}"
          f"  Lead: {p.get('lead', {}).get('displayName', 'n/a')}")
    return p


def list_issue_types(client: AtlassianClient, project_key: str) -> list[dict]:
    """GET /rest/api/3/project/{projectKey} → issueTypes"""
    r = client.get(f"/rest/api/3/project/{project_key}")
    r.raise_for_status()
    types = r.json().get("issueTypes", [])
    print(f"\n[Issue Types for {project_key}] {len(types)} found:")
    for t in types:
        print(f"  {t['name']:20s}  subtask:{t.get('subtask', False)}")
    return types


def create_issue(client: AtlassianClient, project_key: str, summary: str,
                 issue_type: str = "Task", description: str = "") -> dict:
    """POST /rest/api/3/issue"""
    body: dict = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
        }
    }
    if description:
        body["fields"]["description"] = {
            "type": "doc", "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}],
        }
    r = client.post("/rest/api/3/issue", body)
    r.raise_for_status()
    issue = r.json()
    print(f"\n[Created Issue] {issue['key']}: {summary}")
    return issue


def get_issue(client: AtlassianClient, issue_key: str) -> dict:
    """GET /rest/api/3/issue/{issueKey}"""
    r = client.get(f"/rest/api/3/issue/{issue_key}")
    r.raise_for_status()
    issue = r.json()
    f = issue["fields"]
    print(f"\n[Issue] {issue['key']}: {f['summary']}")
    print(f"  Type: {f['issuetype']['name']:12s}  Status: {f['status']['name']}")
    if f.get("assignee"):
        print(f"  Assignee: {f['assignee']['displayName']}")
    return issue


def update_issue(client: AtlassianClient, issue_key: str, **fields) -> None:
    """PUT /rest/api/3/issue/{issueKey}"""
    r = client.put(f"/rest/api/3/issue/{issue_key}", {"fields": fields})
    if r.status_code == 204:
        print(f"\n[Updated] {issue_key}")
    else:
        print(f"\n[Update failed] {issue_key}: HTTP {r.status_code} — {r.text[:200]}")


def delete_issue(client: AtlassianClient, issue_key: str) -> bool:
    """DELETE /rest/api/3/issue/{issueKey}"""
    r = client.delete(f"/rest/api/3/issue/{issue_key}")
    ok = r.status_code == 204
    print(f"\n[{'Deleted' if ok else 'Delete failed'}] {issue_key}")
    return ok


def add_comment(client: AtlassianClient, issue_key: str, text: str) -> dict:
    """POST /rest/api/3/issue/{issueKey}/comment"""
    body = {
        "body": {
            "type": "doc", "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}],
        }
    }
    r = client.post(f"/rest/api/3/issue/{issue_key}/comment", body)
    r.raise_for_status()
    print(f"\n[Comment added] {issue_key}")
    return r.json()


def search_issues(client: AtlassianClient, jql: str, max_results: int = 10) -> list[dict]:
    """GET /rest/api/3/search — JQL query"""
    r = client.get("/rest/api/3/search", params={"jql": jql, "maxResults": max_results,
                                                  "fields": "summary,status,issuetype"})
    r.raise_for_status()
    data = r.json()
    issues = data.get("issues", [])
    print(f"\n[Search] '{jql}'")
    print(f"  {data['total']} total — showing {len(issues)}:")
    for i in issues:
        f = i["fields"]
        print(f"  {i['key']:12s}  [{f['status']['name']:12s}]  {f['summary'][:55]}")
    return issues


def get_transitions(client: AtlassianClient, issue_key: str) -> list[dict]:
    """GET /rest/api/3/issue/{issueKey}/transitions"""
    r = client.get(f"/rest/api/3/issue/{issue_key}/transitions")
    r.raise_for_status()
    transitions = r.json().get("transitions", [])
    print(f"\n[Transitions for {issue_key}]:")
    for t in transitions:
        print(f"  ID:{t['id']:4s}  → {t['to']['name']}")
    return transitions


def transition_issue(client: AtlassianClient, issue_key: str,
                     target_status: str) -> tuple[bool, str]:
    """POST /rest/api/3/issue/{issueKey}/transitions"""
    transitions = get_transitions(client, issue_key)
    match = next((t for t in transitions
                  if t["to"]["name"].lower() == target_status.lower()), None)
    if not match:
        return False, f"No transition to '{target_status}' available"
    r = client.post(f"/rest/api/3/issue/{issue_key}/transitions",
                    {"transition": {"id": match["id"]}})
    ok = r.status_code in (200, 204)
    print(f"\n[Transition] {issue_key} → '{target_status}': {'OK' if ok else f'HTTP {r.status_code}'}")
    return ok, target_status if ok else r.text[:200]


def list_custom_fields(client: AtlassianClient) -> list[dict]:
    """GET /rest/api/3/field — returns all fields, filters to custom only"""
    r = client.get("/rest/api/3/field")
    r.raise_for_status()
    all_fields = r.json()
    custom = [f for f in all_fields if f.get("custom")]
    print(f"\n[Fields] {len(all_fields)} total, {len(custom)} custom:")
    for f in custom[:15]:
        schema = f.get("schema", {})
        print(f"  {f['id']:30s}  {f['name']}  ({schema.get('type', '?')})")
    if len(custom) > 15:
        print(f"  ... and {len(custom) - 15} more")
    return custom


def list_users(client: AtlassianClient, max_results: int = 10) -> list[dict]:
    """GET /rest/api/3/users/search"""
    r = client.get("/rest/api/3/users/search", params={"maxResults": max_results})
    r.raise_for_status()
    users = r.json()
    print(f"\n[Users] {len(users)} returned:")
    for u in users:
        print(f"  {u.get('accountId','')[:24]}  {u.get('displayName','n/a')}")
    return users


def get_myself(client: AtlassianClient) -> dict:
    """GET /rest/api/3/myself"""
    r = client.get("/rest/api/3/myself")
    r.raise_for_status()
    me = r.json()
    print(f"\n[Myself] {me.get('displayName')} <{me.get('emailAddress','')}>  ({me.get('accountId','')})")
    return me


# ---------------------------------------------------------------------------
# Jira Service Management (JSM)
# ---------------------------------------------------------------------------

def list_service_desks(client: AtlassianClient) -> list[dict]:
    """GET /rest/servicedeskapi/servicedesk"""
    r = client.get("/rest/servicedeskapi/servicedesk")
    r.raise_for_status()
    desks = r.json().get("values", [])
    print(f"\n[Service Desks] {len(desks)} found:")
    for d in desks:
        print(f"  ID:{d['id']}  Key:{d['projectKey']:12s}  {d['projectName']}")
    return desks


def list_request_types(client: AtlassianClient, service_desk_id: str) -> list[dict]:
    """GET /rest/servicedeskapi/servicedesk/{id}/requesttype"""
    r = client.get(f"/rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype")
    r.raise_for_status()
    types = r.json().get("values", [])
    print(f"\n[Request Types — SD {service_desk_id}] {len(types)} found:")
    for t in types:
        print(f"  ID:{t['id']:5s}  {t['name']}")
    return types


def list_jsm_queues(client: AtlassianClient, service_desk_id: str) -> list[dict]:
    """GET /rest/servicedeskapi/servicedesk/{id}/queue"""
    r = client.get(f"/rest/servicedeskapi/servicedesk/{service_desk_id}/queue")
    r.raise_for_status()
    queues = r.json().get("values", [])
    print(f"\n[Queues — SD {service_desk_id}] {len(queues)} found:")
    for q in queues:
        print(f"  ID:{q['id']:5s}  {q['name']:35s}  ({q.get('issueCount','?')} issues)")
    return queues


def create_customer_request(client: AtlassianClient, service_desk_id: str,
                             request_type_id: str, summary: str,
                             description: str = "") -> dict:
    """POST /rest/servicedeskapi/request"""
    body = {
        "serviceDeskId": service_desk_id,
        "requestTypeId": request_type_id,
        "requestFieldValues": {"summary": summary, "description": description},
    }
    r = client.post("/rest/servicedeskapi/request", body)
    r.raise_for_status()
    req = r.json()
    print(f"\n[JSM Request Created] {req['issueKey']}: {summary}")
    return req


# ---------------------------------------------------------------------------
# Jira Assets (formerly Insight)
# ---------------------------------------------------------------------------

def list_asset_schemas(client: AtlassianClient) -> list[dict]:
    """GET /rest/assets/1.0/objectschema/list"""
    r = client.get("/rest/assets/1.0/objectschema/list")
    if r.status_code == 404:
        print("\n[Assets] Not available — requires Jira Premium / Assets add-on")
        return []
    r.raise_for_status()
    schemas = r.json().get("objectschemas", [])
    print(f"\n[Asset Schemas] {len(schemas)} found:")
    for s in schemas:
        print(f"  ID:{s['id']}  {s['name']}  ({s.get('objectCount','?')} objects)")
    return schemas


def list_asset_object_types(client: AtlassianClient, schema_id: str) -> list[dict]:
    """GET /rest/assets/1.0/objectschema/{id}/objecttypes/flat"""
    r = client.get(f"/rest/assets/1.0/objectschema/{schema_id}/objecttypes/flat")
    r.raise_for_status()
    types = r.json()
    print(f"\n[Object Types — Schema {schema_id}] {len(types)} found:")
    for t in types:
        print(f"  ID:{t['id']:5s}  {t['name']}")
    return types


def search_assets(client: AtlassianClient, aql: str, max_results: int = 10) -> list[dict]:
    """POST /rest/assets/1.0/object/navlist/aql  — AQL query
    Example AQL: objectType = "Computer" AND status = Active
    """
    body = {"qlQuery": aql, "maxResults": max_results, "includeAttributes": True}
    r = client.post("/rest/assets/1.0/object/navlist/aql", body)
    r.raise_for_status()
    objects = r.json().get("objectEntries", [])
    print(f"\n[Assets] AQL: '{aql}' → {len(objects)} results:")
    for obj in objects:
        print(f"  ID:{obj['id']}  {obj.get('label','')}")
    return objects


# ---------------------------------------------------------------------------
# Jira Automation  (rule management — requires admin scope)
# ---------------------------------------------------------------------------

def list_automation_rules(client: AtlassianClient, project_key: str) -> list[dict]:
    """GET /rest/cb-automation/latest/project/{key}/rule/export
    Note: Jira Cloud automation rules can be exported but not created via REST API.
    Rule creation/editing must be done through the Jira UI or via import.
    """
    r = client.get(f"/rest/cb-automation/latest/project/{project_key}/rule/export")
    if r.status_code in (403, 404):
        print(f"\n[Automation] HTTP {r.status_code} — admin scope required or no rules configured")
        return []
    r.raise_for_status()
    rules = r.json() if isinstance(r.json(), list) else r.json().get("data", [])
    print(f"\n[Automation Rules — {project_key}] {len(rules)} found:")
    for rule in rules:
        status = "✓" if rule.get("enabled") else "○"
        print(f"  {status}  {rule.get('id','?'):8s}  {rule.get('name','?')}")
    return rules


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Jira Cloud API examples")
    parser.add_argument("--project", required=True, help="Project key, e.g. MYPROJECT")
    parser.add_argument("--env-file", default=None, metavar="FILE",
                        help="Path to .env file (default: atlassian/.env)")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (creates then deletes a test issue)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = AtlassianClient.from_env()
    project = args.project.upper()

    print(f"\n{'='*60}")
    print(f"Jira Cloud Examples  —  {client.base}")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    get_myself(client)
    list_projects(client)
    get_project(client, project)
    list_issue_types(client, project)
    search_issues(client, f"project = {project} ORDER BY created DESC", max_results=5)
    list_custom_fields(client)
    list_service_desks(client)
    list_asset_schemas(client)
    list_automation_rules(client, project)

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")
        issue = create_issue(client, project,
                             "[EXAMPLE] API test — safe to delete",
                             description="Created by atlassian/jira/examples.py")
        key = issue["key"]
        get_issue(client, key)
        add_comment(client, key, "Example comment from atlassian/jira/examples.py.")
        update_issue(client, key, summary="[EXAMPLE] API test — updated")
        get_transitions(client, key)
        delete_issue(client, key)


if __name__ == "__main__":
    main()
