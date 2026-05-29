"""
Atlassian Statuspage API Examples
Covers: pages, components, incidents, incident updates, subscribers

Auth:  STATUSPAGE_API_KEY, STATUSPAGE_PAGE_ID  (env vars or atlassian/.env)
Docs:  https://developer.statuspage.io/

Usage:
    # Read-only demo:
    python atlassian/statuspage/examples.py

    # Include write operations (creates then resolves a test incident):
    python atlassian/statuspage/examples.py --demo-write
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import StatuspageClient, load_env


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def list_pages(client: StatuspageClient) -> list[dict]:
    """GET /v1/pages  — lists all pages accessible with this API key"""
    r = client.get("/v1/pages")
    r.raise_for_status()
    pages = r.json()
    print(f"\n[Pages] {len(pages)} found:")
    for p in pages:
        print(f"  {p['id']}  {p['name']}  ({p.get('subdomain','')})")
    return pages


def get_page(client: StatuspageClient) -> dict:
    """GET /v1/pages/{page_id}"""
    r = client.get(f"/v1/pages/{client.page_id}")
    r.raise_for_status()
    p = r.json()
    print(f"\n[Page] {p['id']}: {p['name']}")
    print(f"  URL: {p.get('page_description','?')}")
    print(f"  Time zone: {p.get('time_zone','?')}")
    return p


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------

def list_components(client: StatuspageClient) -> list[dict]:
    """GET /v1/pages/{page_id}/components"""
    r = client.get(f"/v1/pages/{client.page_id}/components")
    r.raise_for_status()
    components = r.json()
    print(f"\n[Components] {len(components)} found:")
    for c in components:
        group = " (group)" if c.get("group") else ""
        print(f"  {c['id']}  [{c.get('status','?'):20s}]  {c['name']}{group}")
    return components


def update_component_status(client: StatuspageClient, component_id: str,
                             status: str) -> dict:
    """PATCH /v1/pages/{page_id}/components/{component_id}
    Valid status values: operational, degraded_performance, partial_outage,
                         major_outage, under_maintenance
    """
    body = {"component": {"status": status}}
    r = client.patch(f"/v1/pages/{client.page_id}/components/{component_id}", body)
    r.raise_for_status()
    c = r.json()
    print(f"\n[Component Updated] {c['name']} → {c['status']}")
    return c


def create_component(client: StatuspageClient, name: str,
                     description: str = "") -> dict:
    """POST /v1/pages/{page_id}/components"""
    body = {
        "component": {
            "name": name,
            "description": description,
            "status": "operational",
        }
    }
    r = client.post(f"/v1/pages/{client.page_id}/components", body)
    r.raise_for_status()
    c = r.json()
    print(f"\n[Created Component] {c['id']}: {c['name']}")
    return c


def delete_component(client: StatuspageClient, component_id: str) -> bool:
    """DELETE /v1/pages/{page_id}/components/{component_id}"""
    r = client.delete(f"/v1/pages/{client.page_id}/components/{component_id}")
    ok = r.status_code == 200
    print(f"\n[{'Deleted' if ok else 'Delete failed'}] Component {component_id}")
    return ok


# ---------------------------------------------------------------------------
# Incidents
# ---------------------------------------------------------------------------

def list_incidents(client: StatuspageClient, status: str = "unresolved",
                   max_results: int = 10) -> list[dict]:
    """GET /v1/pages/{page_id}/incidents  or  /incidents/unresolved
    status: 'unresolved' | 'scheduled' | 'all'
    """
    if status == "unresolved":
        path = f"/v1/pages/{client.page_id}/incidents/unresolved"
    else:
        path = f"/v1/pages/{client.page_id}/incidents"
    r = client.get(path, params={"per_page": max_results})
    r.raise_for_status()
    incidents = r.json()
    print(f"\n[Incidents ({status})] {len(incidents)} returned:")
    for i in incidents:
        print(f"  {i['id']}  [{i.get('status','?'):15s}]  {i.get('name','?')}")
    return incidents


def get_incident(client: StatuspageClient, incident_id: str) -> dict:
    """GET /v1/pages/{page_id}/incidents/{incident_id}"""
    r = client.get(f"/v1/pages/{client.page_id}/incidents/{incident_id}")
    r.raise_for_status()
    i = r.json()
    print(f"\n[Incident] {i['id']}: {i['name']}")
    print(f"  Status: {i.get('status')}  Impact: {i.get('impact')}")
    for update in i.get("incident_updates", [])[:3]:
        print(f"  → [{update.get('status')}] {update.get('body','')[:80]}")
    return i


def create_incident(client: StatuspageClient, name: str, status: str = "investigating",
                    body: str = "", impact_override: str = "none",
                    component_ids: list[str] | None = None) -> dict:
    """POST /v1/pages/{page_id}/incidents
    status:          investigating | identified | monitoring | resolved
    impact_override: none | minor | major | critical
    """
    payload: dict = {
        "incident": {
            "name": name,
            "status": status,
            "body": body or f"Investigating the issue: {name}",
            "impact_override": impact_override,
        }
    }
    if component_ids:
        payload["incident"]["components"] = {cid: "major_outage" for cid in component_ids}
    r = client.post(f"/v1/pages/{client.page_id}/incidents", payload)
    r.raise_for_status()
    incident = r.json()
    print(f"\n[Created Incident] {incident['id']}: {incident['name']}  ({incident['status']})")
    return incident


def update_incident(client: StatuspageClient, incident_id: str,
                    status: str, body: str = "") -> dict:
    """PATCH /v1/pages/{page_id}/incidents/{incident_id}
    Adds a new incident update with the given status and message.
    """
    payload = {
        "incident": {
            "status": status,
            "body": body or f"Status updated to {status}.",
        }
    }
    r = client.patch(f"/v1/pages/{client.page_id}/incidents/{incident_id}", payload)
    r.raise_for_status()
    incident = r.json()
    print(f"\n[Updated Incident] {incident_id} → {incident['status']}")
    return incident


def delete_incident(client: StatuspageClient, incident_id: str) -> bool:
    """DELETE /v1/pages/{page_id}/incidents/{incident_id}"""
    r = client.delete(f"/v1/pages/{client.page_id}/incidents/{incident_id}")
    ok = r.status_code == 200
    print(f"\n[{'Deleted' if ok else 'Delete failed'}] Incident {incident_id}")
    return ok


# ---------------------------------------------------------------------------
# Scheduled Maintenances
# ---------------------------------------------------------------------------

def list_scheduled_maintenances(client: StatuspageClient) -> list[dict]:
    """GET /v1/pages/{page_id}/incidents/scheduled"""
    r = client.get(f"/v1/pages/{client.page_id}/incidents/scheduled")
    r.raise_for_status()
    items = r.json()
    print(f"\n[Scheduled Maintenances] {len(items)} found:")
    for m in items:
        print(f"  {m['id']}  [{m.get('status','?'):12s}]  {m.get('name','?')}")
        print(f"    {m.get('scheduled_for','?')[:16]} → {m.get('scheduled_until','?')[:16]}")
    return items


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Statuspage API examples")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (creates then deletes a test incident)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = StatuspageClient.from_env()

    print(f"\n{'='*60}")
    print(f"Statuspage Examples  —  page: {client.page_id}")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    list_pages(client)
    get_page(client)
    list_components(client)
    list_incidents(client, status="unresolved")
    list_scheduled_maintenances(client)

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")
        incident = create_incident(
            client,
            name="[EXAMPLE] API test incident — safe to delete",
            status="investigating",
            body="This is an automated test incident created by atlassian/statuspage/examples.py.",
        )
        incident_id = incident["id"]
        get_incident(client, incident_id)
        update_incident(client, incident_id, status="identified",
                        body="Root cause identified. Working on a fix.")
        update_incident(client, incident_id, status="resolved",
                        body="Issue resolved. All systems operational.")
        delete_incident(client, incident_id)


if __name__ == "__main__":
    main()
