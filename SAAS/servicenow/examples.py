"""
ServiceNow REST API Examples
Covers: incidents, change requests, CMDB, users, catalog, knowledge base

Auth:  SERVICENOW_INSTANCE  (e.g. dev12345.service-now.com)
       SERVICENOW_USER      (username)
       SERVICENOW_PASSWORD  (password or OAuth token)
Docs:  https://developer.servicenow.com/dev.do#!/reference/api/latest/rest/

Usage:
    # Read-only demo:
    python SAAS/servicenow/examples.py

    # Include write operations (creates then resolves a test incident):
    python SAAS/servicenow/examples.py --demo-write
"""

import argparse
import os
import sys
import time
from base64 import b64encode

import requests

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SAAS_DIR   = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, os.path.dirname(_SAAS_DIR))


# ---------------------------------------------------------------------------
# Env + client
# ---------------------------------------------------------------------------

def _load_env(path: str) -> None:
    if not os.path.exists(path):
        return
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
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def _require(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        print(f"ERROR: env var '{name}' is not set.", file=sys.stderr)
        sys.exit(1)
    return val


def load_env(env_file: str | None = None) -> None:
    for p in [env_file,
              os.path.join(_SCRIPT_DIR, ".env"),
              os.path.join(_SAAS_DIR, ".env")]:
        if p and os.path.exists(p):
            _load_env(p)
            return


class ServiceNowClient:
    def __init__(self, instance: str, user: str, password: str):
        self.base = f"https://{instance.rstrip('/')}/api/now"
        creds = b64encode(f"{user}:{password}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {creds}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return requests.get(f"{self.base}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict) -> requests.Response:
        return requests.post(f"{self.base}{path}", headers=self.headers, json=body)

    def patch(self, path: str, body: dict) -> requests.Response:
        return requests.patch(f"{self.base}{path}", headers=self.headers, json=body)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(f"{self.base}{path}", headers=self.headers)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "ServiceNowClient":
        load_env(env_file)
        return cls(
            instance=_require("SERVICENOW_INSTANCE"),
            user=_require("SERVICENOW_USER"),
            password=_require("SERVICENOW_PASSWORD"),
        )


def _table(path: str) -> str:
    return f"/table/{path}"


# ---------------------------------------------------------------------------
# Incidents
# ---------------------------------------------------------------------------

def list_incidents(client: ServiceNowClient, limit: int = 10,
                   state: str | None = None) -> list[dict]:
    """GET /table/incident
    state: 1=New 2=In Progress 3=On Hold 6=Resolved 7=Closed
    """
    params: dict = {
        "sysparm_limit": limit,
        "sysparm_fields": "sys_id,number,short_description,state,priority,assigned_to,opened_at",
        "sysparm_query": "ORDERBYDESCopened_at",
    }
    if state:
        params["sysparm_query"] += f"^state={state}"
    r = client.get(_table("incident"), params=params)
    r.raise_for_status()
    records = r.json().get("result", [])
    print(f"\n[Incidents] {len(records)} returned:")
    for i in records:
        assignee = i.get("assigned_to", {})
        assignee_name = assignee.get("display_value", "—") if isinstance(assignee, dict) else "—"
        print(f"  {i['number']}  [P{i.get('priority',{}).get('value','?')}]  "
              f"{i['short_description'][:50]}  → {assignee_name}")
    return records


def get_incident(client: ServiceNowClient, sys_id: str) -> dict:
    """GET /table/incident/{sys_id}"""
    r = client.get(_table(f"incident/{sys_id}"))
    r.raise_for_status()
    i = r.json()["result"]
    print(f"\n[Incident] {i['number']}  {i['short_description']}")
    print(f"  State: {i.get('state',{}).get('display_value','?')}  "
          f"Priority: {i.get('priority',{}).get('display_value','?')}")
    return i


def create_incident(client: ServiceNowClient, short_description: str,
                    description: str = "", priority: int = 3,
                    category: str = "software") -> dict:
    """POST /table/incident
    priority: 1=Critical 2=High 3=Moderate 4=Low
    """
    payload = {
        "short_description": short_description,
        "description": description,
        "priority": str(priority),
        "category": category,
    }
    r = client.post(_table("incident"), payload)
    r.raise_for_status()
    i = r.json()["result"]
    print(f"\n[Created Incident] {i['number']}  {i['short_description']}")
    return i


def update_incident(client: ServiceNowClient, sys_id: str,
                    updates: dict) -> dict:
    """PATCH /table/incident/{sys_id}"""
    r = client.patch(_table(f"incident/{sys_id}"), updates)
    r.raise_for_status()
    i = r.json()["result"]
    print(f"\n[Updated Incident] {i['number']}  fields={list(updates.keys())}")
    return i


def resolve_incident(client: ServiceNowClient, sys_id: str,
                     resolution_notes: str) -> dict:
    """Resolve an incident (state=6, close_code required)"""
    return update_incident(client, sys_id, {
        "state": "6",
        "close_code": "Solved (Permanently)",
        "close_notes": resolution_notes,
    })


# ---------------------------------------------------------------------------
# Change Requests
# ---------------------------------------------------------------------------

def list_changes(client: ServiceNowClient, limit: int = 10,
                 change_type: str | None = None) -> list[dict]:
    """GET /table/change_request
    change_type: standard | normal | emergency
    """
    params: dict = {
        "sysparm_limit": limit,
        "sysparm_fields": "sys_id,number,short_description,state,type,start_date,end_date",
        "sysparm_query": "ORDERBYDESCsys_created_on",
    }
    if change_type:
        params["sysparm_query"] += f"^type={change_type}"
    r = client.get(_table("change_request"), params=params)
    r.raise_for_status()
    records = r.json().get("result", [])
    print(f"\n[Change Requests] {len(records)} returned:")
    for c in records:
        print(f"  {c['number']}  [{c.get('type',{}).get('value','?'):10s}]  "
              f"{c['short_description'][:50]}")
    return records


def create_change(client: ServiceNowClient, short_description: str,
                  description: str = "", change_type: str = "normal",
                  risk: str = "moderate") -> dict:
    """POST /table/change_request"""
    payload = {
        "short_description": short_description,
        "description": description,
        "type": change_type,
        "risk": risk,
    }
    r = client.post(_table("change_request"), payload)
    r.raise_for_status()
    c = r.json()["result"]
    print(f"\n[Created Change] {c['number']}  type={change_type}")
    return c


# ---------------------------------------------------------------------------
# CMDB (Configuration Items)
# ---------------------------------------------------------------------------

def list_cis(client: ServiceNowClient, ci_class: str = "cmdb_ci_server",
             limit: int = 10) -> list[dict]:
    """GET /table/{ci_class} — query CMDB configuration items
    Common classes: cmdb_ci_server, cmdb_ci_database, cmdb_ci_application,
                    cmdb_ci_service, cmdb_ci_computer
    """
    params = {
        "sysparm_limit": limit,
        "sysparm_fields": "sys_id,name,ip_address,os,operational_status,assigned_to",
    }
    r = client.get(_table(ci_class), params=params)
    r.raise_for_status()
    records = r.json().get("result", [])
    print(f"\n[CMDB: {ci_class}] {len(records)} returned:")
    for ci in records:
        ip = ci.get("ip_address", "—")
        status = ci.get("operational_status", {})
        status_val = status.get("display_value", "?") if isinstance(status, dict) else status
        print(f"  {ci['name']:40s}  [{status_val:10s}]  {ip}")
    return records


def get_ci(client: ServiceNowClient, ci_class: str, sys_id: str) -> dict:
    """GET /table/{ci_class}/{sys_id}"""
    r = client.get(_table(f"{ci_class}/{sys_id}"))
    r.raise_for_status()
    ci = r.json()["result"]
    print(f"\n[CI] {ci.get('name')}  class={ci_class}")
    return ci


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def list_users(client: ServiceNowClient, limit: int = 20,
               active_only: bool = True) -> list[dict]:
    """GET /table/sys_user"""
    params: dict = {
        "sysparm_limit": limit,
        "sysparm_fields": "sys_id,user_name,email,name,department,active",
    }
    if active_only:
        params["sysparm_query"] = "active=true"
    r = client.get(_table("sys_user"), params=params)
    r.raise_for_status()
    users = r.json().get("result", [])
    print(f"\n[Users] {len(users)} returned:")
    for u in users:
        dept = u.get("department", {})
        dept_name = dept.get("display_value", "—") if isinstance(dept, dict) else dept
        print(f"  {u['user_name']:25s}  {u['name']:30s}  {dept_name}")
    return users


def get_user(client: ServiceNowClient, user_name: str) -> dict:
    """GET /table/sys_user?sysparm_query=user_name={user_name}"""
    r = client.get(_table("sys_user"), params={
        "sysparm_query": f"user_name={user_name}",
        "sysparm_limit": 1,
    })
    r.raise_for_status()
    results = r.json().get("result", [])
    if not results:
        raise ValueError(f"User not found: {user_name}")
    u = results[0]
    print(f"\n[User] {u['user_name']}  {u['name']}  {u.get('email','?')}")
    return u


# ---------------------------------------------------------------------------
# Service Catalog
# ---------------------------------------------------------------------------

def list_catalog_items(client: ServiceNowClient, limit: int = 10) -> list[dict]:
    """GET /table/sc_cat_item — service catalog items"""
    params = {
        "sysparm_limit": limit,
        "sysparm_fields": "sys_id,name,category,price,active",
        "sysparm_query": "active=true",
    }
    r = client.get(_table("sc_cat_item"), params=params)
    r.raise_for_status()
    items = r.json().get("result", [])
    print(f"\n[Catalog Items] {len(items)} returned:")
    for item in items:
        cat = item.get("category", {})
        cat_name = cat.get("display_value", "?") if isinstance(cat, dict) else cat
        print(f"  {item['name']:45s}  [{cat_name}]")
    return items


# ---------------------------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------------------------

def list_kb_articles(client: ServiceNowClient, limit: int = 10,
                     query: str | None = None) -> list[dict]:
    """GET /table/kb_knowledge"""
    params: dict = {
        "sysparm_limit": limit,
        "sysparm_fields": "sys_id,number,short_description,category,view_count,kb_knowledge_base",
        "sysparm_query": "workflowORDERBYDESCview_count",
    }
    if query:
        params["sysparm_query"] += f"^short_descriptionLIKE{query}"
    r = client.get(_table("kb_knowledge"), params=params)
    r.raise_for_status()
    articles = r.json().get("result", [])
    print(f"\n[KB Articles] {len(articles)} returned:")
    for a in articles:
        views = a.get("view_count", 0)
        print(f"  {a['number']}  [{views:>5} views]  {a['short_description'][:60]}")
    return articles


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ServiceNow REST API examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  SERVICENOW_INSTANCE  dev12345.service-now.com
  SERVICENOW_USER      admin
  SERVICENOW_PASSWORD  your-password

Examples:
  python SAAS/servicenow/examples.py
  python SAAS/servicenow/examples.py --demo-write
        """,
    )
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write ops (creates then resolves a test incident)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = ServiceNowClient.from_env()

    print(f"\n{'='*60}")
    print("ServiceNow Examples")
    print(f"{'='*60}")

    list_incidents(client)
    list_changes(client)
    list_cis(client)
    list_users(client)
    list_catalog_items(client)
    list_kb_articles(client)

    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        inc = create_incident(
            client,
            short_description="[EXAMPLE] API test — safe to resolve",
            description="Created by SAAS/servicenow/examples.py",
            priority=4,
        )
        sys_id = inc["sys_id"]
        time.sleep(1)
        update_incident(client, sys_id, {"description": "Updated by examples.py"})
        time.sleep(1)
        resolve_incident(client, sys_id, "Resolved by API example cleanup.")


if __name__ == "__main__":
    main()
