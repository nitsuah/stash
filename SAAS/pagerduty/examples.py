"""
PagerDuty API Examples
Covers: incidents, services, escalation policies, schedules, on-call, events

Auth:  PAGERDUTY_API_KEY      (REST API — account/team API key)
       PAGERDUTY_ROUTING_KEY  (Events API v2 — service integration key)
Docs:  https://developer.pagerduty.com/api-reference/

Usage:
    # Read-only demo:
    python SAAS/pagerduty/examples.py

    # Include write operations (creates then resolves a test incident):
    python SAAS/pagerduty/examples.py --demo-write
"""

import argparse
import os
import sys
import time

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


REST_BASE = "https://api.pagerduty.com"
EVENTS_BASE = "https://events.pagerduty.com"


class PagerDutyClient:
    def __init__(self, api_key: str):
        self.headers = {
            "Authorization": f"Token token={api_key}",
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Content-Type": "application/json",
        }

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return requests.get(f"{REST_BASE}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict) -> requests.Response:
        return requests.post(f"{REST_BASE}{path}", headers=self.headers, json=body)

    def put(self, path: str, body: dict) -> requests.Response:
        return requests.put(f"{REST_BASE}{path}", headers=self.headers, json=body)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(f"{REST_BASE}{path}", headers=self.headers)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "PagerDutyClient":
        load_env(env_file)
        return cls(api_key=_require("PAGERDUTY_API_KEY"))


# ---------------------------------------------------------------------------
# Incidents
# ---------------------------------------------------------------------------

def list_incidents(client: PagerDutyClient, status: str = "triggered,acknowledged",
                   max_results: int = 10) -> list[dict]:
    """GET /incidents"""
    r = client.get("/incidents", params={"statuses[]": status.split(","),
                                          "limit": max_results, "sort_by": "created_at:desc"})
    r.raise_for_status()
    incidents = r.json().get("incidents", [])
    print(f"\n[Incidents ({status})] {len(incidents)} returned:")
    for i in incidents:
        svc = i.get("service", {}).get("summary", "?")
        print(f"  {i['id']}  [{i['status']:12s}]  [{i['urgency']}]  {i['title'][:45]}  ({svc})")
    return incidents


def get_incident(client: PagerDutyClient, incident_id: str) -> dict:
    """GET /incidents/{id}"""
    r = client.get(f"/incidents/{incident_id}")
    r.raise_for_status()
    i = r.json()["incident"]
    print(f"\n[Incident] {i['id']}: {i['title']}")
    print(f"  Status: {i['status']}  Urgency: {i['urgency']}")
    print(f"  Service: {i.get('service',{}).get('summary','?')}")
    print(f"  Created: {i.get('created_at','?')[:19]}")
    return i


def create_incident(client: PagerDutyClient, title: str, service_id: str,
                    urgency: str = "high", body: str = "",
                    escalation_policy_id: str | None = None) -> dict:
    """POST /incidents"""
    payload: dict = {
        "incident": {
            "type": "incident",
            "title": title,
            "service": {"id": service_id, "type": "service_reference"},
            "urgency": urgency,
        }
    }
    if body:
        payload["incident"]["body"] = {"type": "incident_body", "details": body}
    if escalation_policy_id:
        payload["incident"]["escalation_policy"] = {
            "id": escalation_policy_id, "type": "escalation_policy_reference"
        }
    r = client.post("/incidents", payload)
    r.raise_for_status()
    i = r.json()["incident"]
    print(f"\n[Created Incident] {i['id']}: {i['title']}  ({i['status']})")
    return i


def update_incident_status(client: PagerDutyClient, incident_id: str,
                            status: str, resolution: str = "") -> dict:
    """PUT /incidents/{id}  — status: acknowledged | resolved"""
    payload: dict = {
        "incident": {"type": "incident", "status": status}
    }
    if resolution:
        payload["incident"]["resolution"] = resolution
    r = client.put(f"/incidents/{incident_id}", payload)
    r.raise_for_status()
    i = r.json()["incident"]
    print(f"\n[Updated Incident] {incident_id} → {i['status']}")
    return i


def add_note(client: PagerDutyClient, incident_id: str, content: str) -> dict:
    """POST /incidents/{id}/notes"""
    r = client.post(f"/incidents/{incident_id}/notes", {"note": {"content": content}})
    r.raise_for_status()
    note = r.json()["note"]
    print(f"\n[Note added] {incident_id}: {content[:60]}")
    return note


# ---------------------------------------------------------------------------
# Events API v2  (alert ingestion — separate endpoint + routing key auth)
# ---------------------------------------------------------------------------

def send_event(routing_key: str, summary: str, source: str,
               severity: str = "error", action: str = "trigger",
               dedup_key: str | None = None, custom_details: dict | None = None) -> dict:
    """POST https://events.pagerduty.com/v2/enqueue
    severity: info | warning | error | critical
    action:   trigger | acknowledge | resolve
    Returns response JSON with dedup_key for follow-up ack/resolve calls.
    """
    payload: dict = {
        "routing_key": routing_key,
        "event_action": action,
        "payload": {
            "summary": summary,
            "source": source,
            "severity": severity,
        },
    }
    if dedup_key:
        payload["dedup_key"] = dedup_key
    if custom_details:
        payload["payload"]["custom_details"] = custom_details
    r = requests.post(f"{EVENTS_BASE}/v2/enqueue",
                      headers={"Content-Type": "application/json"},
                      json=payload)
    r.raise_for_status()
    data = r.json()
    print(f"\n[Event sent] action={action}  status={data.get('status')}  "
          f"dedup_key={data.get('dedup_key','?')}")
    return data


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

def list_services(client: PagerDutyClient, max_results: int = 10) -> list[dict]:
    """GET /services"""
    r = client.get("/services", params={"limit": max_results, "sort_by": "name"})
    r.raise_for_status()
    services = r.json().get("services", [])
    print(f"\n[Services] {len(services)} returned:")
    for s in services:
        print(f"  {s['id']}  [{s.get('status','?'):12s}]  {s['name']}")
    return services


def get_service(client: PagerDutyClient, service_id: str) -> dict:
    """GET /services/{id}"""
    r = client.get(f"/services/{service_id}")
    r.raise_for_status()
    s = r.json()["service"]
    print(f"\n[Service] {s['id']}: {s['name']}  (status: {s.get('status')})")
    return s


# ---------------------------------------------------------------------------
# Escalation Policies & On-Call
# ---------------------------------------------------------------------------

def list_escalation_policies(client: PagerDutyClient, max_results: int = 10) -> list[dict]:
    """GET /escalation_policies"""
    r = client.get("/escalation_policies", params={"limit": max_results})
    r.raise_for_status()
    policies = r.json().get("escalation_policies", [])
    print(f"\n[Escalation Policies] {len(policies)} returned:")
    for p in policies:
        rules = len(p.get("escalation_rules", []))
        print(f"  {p['id']}  {p['name']}  ({rules} rules)")
    return policies


def list_oncall(client: PagerDutyClient, escalation_policy_ids: list[str] | None = None,
                max_results: int = 10) -> list[dict]:
    """GET /oncalls"""
    params: dict = {"limit": max_results}
    if escalation_policy_ids:
        params["escalation_policy_ids[]"] = escalation_policy_ids
    r = client.get("/oncalls", params=params)
    r.raise_for_status()
    oncalls = r.json().get("oncalls", [])
    print(f"\n[On-Call] {len(oncalls)} entries:")
    for oc in oncalls:
        user = oc.get("user", {}).get("summary", "?")
        sched = oc.get("schedule", {}).get("summary", "no schedule") if oc.get("schedule") else "no schedule"
        print(f"  L{oc.get('escalation_level','?')}  {user:30s}  {sched}")
    return oncalls


# ---------------------------------------------------------------------------
# Schedules
# ---------------------------------------------------------------------------

def list_schedules(client: PagerDutyClient, max_results: int = 10) -> list[dict]:
    """GET /schedules"""
    r = client.get("/schedules", params={"limit": max_results})
    r.raise_for_status()
    schedules = r.json().get("schedules", [])
    print(f"\n[Schedules] {len(schedules)} returned:")
    for s in schedules:
        tz = s.get("time_zone", "?")
        print(f"  {s['id']}  {s['name']}  ({tz})")
    return schedules


def get_schedule(client: PagerDutyClient, schedule_id: str,
                 since: str | None = None, until: str | None = None) -> dict:
    """GET /schedules/{id} — optionally filter rendered entries by date range
    Dates as ISO 8601 strings, e.g. '2026-06-01T00:00:00Z'
    """
    params: dict = {}
    if since:
        params["since"] = since
    if until:
        params["until"] = until
    r = client.get(f"/schedules/{schedule_id}", params=params)
    r.raise_for_status()
    s = r.json()["schedule"]
    print(f"\n[Schedule] {s['id']}: {s['name']}  ({s.get('time_zone','?')})")
    entries = s.get("final_schedule", {}).get("rendered_schedule_entries", [])
    print(f"  {len(entries)} rendered entries:")
    for e in entries[:5]:
        user = e.get("user", {}).get("summary", "?")
        print(f"    {e.get('start','?')[:16]} → {e.get('end','?')[:16]}  {user}")
    return s


# ---------------------------------------------------------------------------
# Users & Teams
# ---------------------------------------------------------------------------

def list_users(client: PagerDutyClient, max_results: int = 10) -> list[dict]:
    """GET /users"""
    r = client.get("/users", params={"limit": max_results})
    r.raise_for_status()
    users = r.json().get("users", [])
    print(f"\n[Users] {len(users)} returned:")
    for u in users:
        print(f"  {u['id']}  {u.get('name','?'):30s}  {u.get('email','?')}")
    return users


def list_teams(client: PagerDutyClient, max_results: int = 10) -> list[dict]:
    """GET /teams"""
    r = client.get("/teams", params={"limit": max_results})
    r.raise_for_status()
    teams = r.json().get("teams", [])
    print(f"\n[Teams] {len(teams)} returned:")
    for t in teams:
        print(f"  {t['id']}  {t['name']}")
    return teams


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="PagerDuty API examples")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--service-id", default=None,
                        help="Service ID for write demo (overrides PAGERDUTY_SERVICE_ID env var)")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (creates then resolves a test incident)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = PagerDutyClient.from_env()

    print(f"\n{'='*60}")
    print("PagerDuty Examples")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    list_services(client)
    list_escalation_policies(client)
    list_schedules(client)
    list_oncall(client)
    list_users(client)
    list_teams(client)
    list_incidents(client)

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        service_id = args.service_id or os.environ.get("PAGERDUTY_SERVICE_ID", "")
        routing_key = os.environ.get("PAGERDUTY_ROUTING_KEY", "")

        if service_id:
            incident = create_incident(
                client,
                title="[EXAMPLE] API test — safe to resolve",
                service_id=service_id,
                urgency="low",
                body="Created by SAAS/pagerduty/examples.py",
            )
            incident_id = incident["id"]
            get_incident(client, incident_id)
            add_note(client, incident_id, "Automated test note from examples.py")
            time.sleep(2)
            update_incident_status(client, incident_id, "acknowledged")
            time.sleep(2)
            update_incident_status(client, incident_id, "resolved",
                                   resolution="Resolved by API example cleanup.")
        else:
            print("\n[Write] Set PAGERDUTY_SERVICE_ID or pass --service-id to test incident creation")

        if routing_key:
            # Events API v2 demo: trigger → resolve via dedup_key
            dedup_key = "example-test-event-001"
            send_event(routing_key, summary="[EXAMPLE] Test alert from examples.py",
                       source="examples.py", severity="warning",
                       dedup_key=dedup_key,
                       custom_details={"environment": "test", "script": "SAAS/pagerduty/examples.py"})
            time.sleep(2)
            send_event(routing_key, summary="[EXAMPLE] Test alert resolved",
                       source="examples.py", severity="info",
                       action="resolve", dedup_key=dedup_key)
        else:
            print("\n[Write] Set PAGERDUTY_ROUTING_KEY to test Events API v2")


if __name__ == "__main__":
    main()
