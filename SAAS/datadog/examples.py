"""
Datadog API Examples
Covers: metrics, monitors, dashboards, incidents, logs, hosts, downtimes, events

Auth:  DATADOG_API_KEY  (Datadog → Organization Settings → API Keys)
       DATADOG_APP_KEY  (Datadog → Organization Settings → Application Keys)
       DATADOG_SITE     (default: datadoghq.com — use datadoghq.eu for EU)
Docs:  https://docs.datadoghq.com/api/latest/

Usage:
    # Read-only demo:
    python SAAS/datadog/examples.py

    # Include write operations (creates then deletes a test monitor):
    python SAAS/datadog/examples.py --demo-write
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


class DatadogClient:
    def __init__(self, api_key: str, app_key: str, site: str = "datadoghq.com"):
        self.base = f"https://api.{site}/api/v1"
        self.base_v2 = f"https://api.{site}/api/v2"
        self.headers = {
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key,
            "Content-Type": "application/json",
        }

    def get(self, path: str, params: dict | None = None,
            v2: bool = False) -> requests.Response:
        base = self.base_v2 if v2 else self.base
        return requests.get(f"{base}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict, v2: bool = False) -> requests.Response:
        base = self.base_v2 if v2 else self.base
        return requests.post(f"{base}{path}", headers=self.headers, json=body)

    def put(self, path: str, body: dict) -> requests.Response:
        return requests.put(f"{self.base}{path}", headers=self.headers, json=body)

    def delete(self, path: str, v2: bool = False) -> requests.Response:
        base = self.base_v2 if v2 else self.base
        return requests.delete(f"{base}{path}", headers=self.headers)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "DatadogClient":
        load_env(env_file)
        return cls(
            api_key=_require("DATADOG_API_KEY"),
            app_key=_require("DATADOG_APP_KEY"),
            site=os.environ.get("DATADOG_SITE", "datadoghq.com"),
        )


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def query_metrics(client: DatadogClient, query: str,
                  lookback_seconds: int = 3600) -> dict:
    """GET /query — time-series metric query (DogStatsD query syntax)
    Example query: 'avg:system.cpu.user{*}'
    """
    now = int(time.time())
    r = client.get("/query", params={"query": query, "from": now - lookback_seconds, "to": now})
    r.raise_for_status()
    data = r.json()
    series = data.get("series", [])
    print(f"\n[Metrics Query] '{query}'  {len(series)} series:")
    for s in series:
        pts = s.get("pointlist", [])
        last = pts[-1][1] if pts else None
        print(f"  {s.get('metric','?')}  scope={s.get('scope','?')}  "
              f"last={last:.4f}" if last is not None else f"  {s.get('metric','?')}  (no data)")
    return data


def list_active_metrics(client: DatadogClient, lookback_seconds: int = 3600) -> list[str]:
    """GET /metrics — list metrics seen in the last N seconds"""
    from_ts = int(time.time()) - lookback_seconds
    r = client.get("/metrics", params={"from": from_ts})
    r.raise_for_status()
    metrics = r.json().get("metrics", [])
    print(f"\n[Active Metrics] {len(metrics)} seen in last {lookback_seconds}s:")
    for m in metrics[:20]:
        print(f"  {m}")
    if len(metrics) > 20:
        print(f"  ... and {len(metrics) - 20} more")
    return metrics


def submit_metric(client: DatadogClient, metric: str, value: float,
                  tags: list[str] | None = None, metric_type: str = "gauge") -> dict:
    """POST /series — submit a custom metric point
    metric_type: gauge | count | rate
    """
    payload = {
        "series": [{
            "metric": metric,
            "points": [[int(time.time()), value]],
            "type": metric_type,
            "tags": tags or [],
        }]
    }
    r = client.post("/series", payload)
    r.raise_for_status()
    print(f"\n[Metric submitted] {metric}={value}  type={metric_type}  tags={tags or []}")
    return r.json()


# ---------------------------------------------------------------------------
# Monitors
# ---------------------------------------------------------------------------

def list_monitors(client: DatadogClient, max_results: int = 20) -> list[dict]:
    """GET /monitor"""
    r = client.get("/monitor", params={"page_size": max_results})
    r.raise_for_status()
    monitors = r.json()
    print(f"\n[Monitors] {len(monitors)} returned:")
    for m in monitors:
        status = m.get("overall_state", "?")
        print(f"  {m['id']:10d}  [{status:8s}]  [{m['type']:25s}]  {m['name'][:50]}")
    return monitors


def get_monitor(client: DatadogClient, monitor_id: int) -> dict:
    """GET /monitor/{monitor_id}"""
    r = client.get(f"/monitor/{monitor_id}")
    r.raise_for_status()
    m = r.json()
    print(f"\n[Monitor] {m['id']}: {m['name']}")
    print(f"  Type: {m['type']}  State: {m.get('overall_state','?')}")
    print(f"  Query: {m.get('query','?')[:80]}")
    return m


def create_monitor(client: DatadogClient, name: str, query: str,
                   message: str = "", monitor_type: str = "metric alert",
                   tags: list[str] | None = None) -> dict:
    """POST /monitor"""
    payload = {
        "name": name,
        "type": monitor_type,
        "query": query,
        "message": message,
        "tags": tags or [],
        "options": {"notify_no_data": False, "renotify_interval": 0},
    }
    r = client.post("/monitor", payload)
    r.raise_for_status()
    m = r.json()
    print(f"\n[Created Monitor] {m['id']}: {m['name']}")
    return m


def mute_monitor(client: DatadogClient, monitor_id: int,
                 end_ts: int | None = None) -> dict:
    """POST /monitor/{monitor_id}/mute"""
    body: dict = {}
    if end_ts:
        body["end"] = end_ts
    r = client.post(f"/monitor/{monitor_id}/mute", body)
    r.raise_for_status()
    print(f"\n[Muted Monitor] {monitor_id}")
    return r.json()


def delete_monitor(client: DatadogClient, monitor_id: int) -> None:
    """DELETE /monitor/{monitor_id}"""
    r = client.delete(f"/monitor/{monitor_id}")
    r.raise_for_status()
    print(f"\n[Deleted Monitor] {monitor_id}")


# ---------------------------------------------------------------------------
# Dashboards
# ---------------------------------------------------------------------------

def list_dashboards(client: DatadogClient) -> list[dict]:
    """GET /dashboard"""
    r = client.get("/dashboard")
    r.raise_for_status()
    dashboards = r.json().get("dashboards", [])
    print(f"\n[Dashboards] {len(dashboards)} returned:")
    for d in dashboards:
        print(f"  {d['id']:20s}  [{d.get('layout_type','?'):12s}]  {d['title'][:50]}")
    return dashboards


def get_dashboard(client: DatadogClient, dashboard_id: str) -> dict:
    """GET /dashboard/{dashboard_id}"""
    r = client.get(f"/dashboard/{dashboard_id}")
    r.raise_for_status()
    d = r.json()
    print(f"\n[Dashboard] {d['id']}: {d['title']}")
    print(f"  Layout: {d.get('layout_type')}  Widgets: {len(d.get('widgets', []))}")
    return d


# ---------------------------------------------------------------------------
# Hosts
# ---------------------------------------------------------------------------

def list_hosts(client: DatadogClient, max_results: int = 20) -> list[dict]:
    """GET /hosts"""
    r = client.get("/hosts", params={"count": max_results, "sort_field": "last_reported_time",
                                      "sort_dir": "desc"})
    r.raise_for_status()
    host_list = r.json().get("host_list", [])
    print(f"\n[Hosts] {len(host_list)} returned:")
    for h in host_list:
        apps = ", ".join(h.get("apps", [])[:4])
        print(f"  {h['host_name']:40s}  {apps}")
    return host_list


def get_host_totals(client: DatadogClient) -> dict:
    """GET /hosts/totals"""
    r = client.get("/hosts/totals")
    r.raise_for_status()
    totals = r.json()
    print(f"\n[Host Totals] total={totals.get('total_active')}  "
          f"up={totals.get('total_up')}")
    return totals


# ---------------------------------------------------------------------------
# Downtimes
# ---------------------------------------------------------------------------

def list_downtimes(client: DatadogClient, current_only: bool = True) -> list[dict]:
    """GET /downtime"""
    r = client.get("/downtime", params={"current_only": current_only})
    r.raise_for_status()
    downtimes = r.json()
    print(f"\n[Downtimes] {len(downtimes)} returned:")
    for dt in downtimes:
        scope = dt.get("scope", ["?"])
        print(f"  {dt['id']:10d}  {dt.get('message','')[:40]}  scope={scope}")
    return downtimes


def create_downtime(client: DatadogClient, scope: str, message: str = "",
                    duration_seconds: int = 3600) -> dict:
    """POST /downtime — schedule a maintenance window
    scope: e.g. 'host:my-host' or '*' for all
    """
    now = int(time.time())
    payload = {
        "scope": [scope],
        "message": message,
        "start": now,
        "end": now + duration_seconds,
    }
    r = client.post("/downtime", payload)
    r.raise_for_status()
    dt = r.json()
    print(f"\n[Created Downtime] {dt['id']}  scope={scope}  duration={duration_seconds}s")
    return dt


def cancel_downtime(client: DatadogClient, downtime_id: int) -> None:
    """DELETE /downtime/{downtime_id}"""
    r = client.delete(f"/downtime/{downtime_id}")
    r.raise_for_status()
    print(f"\n[Cancelled Downtime] {downtime_id}")


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def list_events(client: DatadogClient, lookback_seconds: int = 3600,
                priority: str = "all") -> list[dict]:
    """GET /events"""
    now = int(time.time())
    r = client.get("/events", params={
        "start": now - lookback_seconds, "end": now, "priority": priority
    })
    r.raise_for_status()
    events = r.json().get("events", [])
    print(f"\n[Events] {len(events)} in last {lookback_seconds}s:")
    for e in events[:10]:
        print(f"  {e.get('date_happened','?')}  [{e.get('alert_type','?'):8s}]  "
              f"{e.get('title','?')[:60]}")
    return events


def post_event(client: DatadogClient, title: str, text: str,
               tags: list[str] | None = None,
               alert_type: str = "info") -> dict:
    """POST /events
    alert_type: error | warning | info | success
    """
    payload = {
        "title": title,
        "text": text,
        "alert_type": alert_type,
        "tags": tags or [],
    }
    r = client.post("/events", payload)
    r.raise_for_status()
    ev = r.json().get("event", {})
    print(f"\n[Event posted] id={ev.get('id')}  {title}")
    return ev


# ---------------------------------------------------------------------------
# Logs (v2)
# ---------------------------------------------------------------------------

def search_logs(client: DatadogClient, query: str = "*",
                lookback_seconds: int = 900, max_results: int = 10) -> list[dict]:
    """POST /logs/events/search (v2)"""
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    since = now - timedelta(seconds=lookback_seconds)
    payload = {
        "filter": {
            "query": query,
            "from": since.isoformat(),
            "to": now.isoformat(),
        },
        "page": {"limit": max_results},
        "sort": "-timestamp",
    }
    r = client.post("/logs/events/search", payload, v2=True)
    r.raise_for_status()
    logs = r.json().get("data", [])
    print(f"\n[Logs] query='{query}'  {len(logs)} results:")
    for log in logs:
        attrs = log.get("attributes", {})
        svc = attrs.get("service", "?")
        msg = str(attrs.get("message", ""))[:70]
        print(f"  [{svc}]  {msg}")
    return logs


# ---------------------------------------------------------------------------
# Incidents (v2)
# ---------------------------------------------------------------------------

def list_incidents(client: DatadogClient, max_results: int = 10) -> list[dict]:
    """GET /incidents (v2) — requires Incident Management"""
    r = client.get("/incidents", params={"page[size]": max_results}, v2=True)
    r.raise_for_status()
    incidents = r.json().get("data", [])
    print(f"\n[Incidents] {len(incidents)} returned:")
    for inc in incidents:
        attrs = inc.get("attributes", {})
        print(f"  {inc['id']}  [{attrs.get('status','?'):12s}]  "
              f"[sev:{attrs.get('severity','?')}]  {attrs.get('title','?')[:50]}")
    return incidents


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Datadog API examples")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (creates monitor + event, then deletes)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = DatadogClient.from_env()

    print(f"\n{'='*60}")
    print("Datadog Examples")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    get_host_totals(client)
    list_hosts(client)
    list_monitors(client)
    list_dashboards(client)
    list_downtimes(client)
    list_events(client)
    list_active_metrics(client)
    query_metrics(client, "avg:system.cpu.user{*}")
    search_logs(client, query="status:error")
    list_incidents(client)

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        # Custom metric
        submit_metric(client, "examples.test.gauge", 1.0,
                      tags=["env:test", "source:examples_py"])

        # Event
        post_event(client,
                   title="[EXAMPLE] API test from examples.py",
                   text="Posted by SAAS/datadog/examples.py — safe to ignore.",
                   tags=["env:test"],
                   alert_type="info")

        # Monitor lifecycle
        monitor = create_monitor(
            client,
            name="[EXAMPLE] Test monitor — safe to delete",
            query="avg(last_5m):avg:system.cpu.user{env:test} > 99",
            message="Test monitor from examples.py @slack-test",
            tags=["env:test"],
        )
        monitor_id = monitor["id"]
        time.sleep(1)
        mute_monitor(client, monitor_id,
                     end_ts=int(time.time()) + 3600)
        time.sleep(1)
        delete_monitor(client, monitor_id)


if __name__ == "__main__":
    main()
