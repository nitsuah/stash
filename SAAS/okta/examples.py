"""
Okta Management API Examples
Covers: users, groups, apps, factors (MFA), logs, schemas, SCIM-style provisioning

Auth:  OKTA_DOMAIN     (e.g. your-org.okta.com)
       OKTA_API_TOKEN  (Admin Console → Security → API → Tokens)
Docs:  https://developer.okta.com/docs/reference/core-okta-api/

Usage:
    # Read-only demo:
    python SAAS/okta/examples.py

    # Include write operations (creates then deactivates a test user):
    python SAAS/okta/examples.py --demo-write
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


class OktaClient:
    def __init__(self, domain: str, api_token: str):
        # domain: your-org.okta.com (no https://)
        self.base = f"https://{domain.rstrip('/')}/api/v1"
        self.headers = {
            "Authorization": f"SSWS {api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return requests.get(f"{self.base}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict) -> requests.Response:
        return requests.post(f"{self.base}{path}", headers=self.headers, json=body)

    def put(self, path: str, body: dict) -> requests.Response:
        return requests.put(f"{self.base}{path}", headers=self.headers, json=body)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(f"{self.base}{path}", headers=self.headers)

    def post_no_body(self, path: str) -> requests.Response:
        return requests.post(f"{self.base}{path}", headers=self.headers)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "OktaClient":
        load_env(env_file)
        return cls(
            domain=_require("OKTA_DOMAIN"),
            api_token=_require("OKTA_API_TOKEN"),
        )


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def list_users(client: OktaClient, limit: int = 20,
               status: str | None = None) -> list[dict]:
    """GET /users — list users, optionally filtered by status
    status: ACTIVE | INACTIVE | DEPROVISIONED | STAGED | PROVISIONED | RECOVERY | LOCKED_OUT
    """
    params: dict = {"limit": limit}
    if status:
        params["filter"] = f'status eq "{status}"'
    r = client.get("/users", params=params)
    r.raise_for_status()
    users = r.json()
    print(f"\n[Users{f' ({status})' if status else ''}] {len(users)} returned:")
    for u in users:
        p = u.get("profile", {})
        print(f"  {u['id']}  [{u['status']:12s}]  {p.get('login','?'):35s}  {p.get('displayName','?')}")
    return users


def get_user(client: OktaClient, user_id: str) -> dict:
    """GET /users/{userId} — userId can be ID, login, or login shortname"""
    r = client.get(f"/users/{user_id}")
    r.raise_for_status()
    u = r.json()
    p = u.get("profile", {})
    print(f"\n[User] {u['id']}  {p.get('login')}")
    print(f"  Name: {p.get('firstName')} {p.get('lastName')}  Status: {u['status']}")
    print(f"  Email: {p.get('email')}  Dept: {p.get('department','—')}")
    return u


def search_users(client: OktaClient, query: str, limit: int = 20) -> list[dict]:
    """GET /users?search= — search by profile attributes"""
    r = client.get("/users", params={"search": query, "limit": limit})
    r.raise_for_status()
    users = r.json()
    print(f"\n[User Search] '{query}'  {len(users)} results:")
    for u in users:
        p = u.get("profile", {})
        print(f"  {u['id']}  {p.get('login','?'):35s}  {p.get('displayName','?')}")
    return users


def create_user(client: OktaClient, first: str, last: str,
                email: str, login: str | None = None,
                activate: bool = False) -> dict:
    """POST /users — create a new user (staged by default)"""
    payload = {
        "profile": {
            "firstName": first,
            "lastName": last,
            "email": email,
            "login": login or email,
        }
    }
    r = client.post(f"/users?activate={str(activate).lower()}", payload)
    r.raise_for_status()
    u = r.json()
    print(f"\n[Created User] {u['id']}  {u['profile']['login']}  status={u['status']}")
    return u


def update_user(client: OktaClient, user_id: str, profile_updates: dict) -> dict:
    """POST /users/{userId} — partial profile update"""
    r = client.post(f"/users/{user_id}", {"profile": profile_updates})
    r.raise_for_status()
    u = r.json()
    print(f"\n[Updated User] {user_id}  updated fields: {list(profile_updates.keys())}")
    return u


def deactivate_user(client: OktaClient, user_id: str) -> None:
    """POST /users/{userId}/lifecycle/deactivate"""
    r = client.post_no_body(f"/users/{user_id}/lifecycle/deactivate")
    r.raise_for_status()
    print(f"\n[Deactivated User] {user_id}")


def activate_user(client: OktaClient, user_id: str,
                  send_email: bool = True) -> dict:
    """POST /users/{userId}/lifecycle/activate"""
    r = client.post_no_body(
        f"/users/{user_id}/lifecycle/activate?sendEmail={str(send_email).lower()}"
    )
    r.raise_for_status()
    data = r.json()
    print(f"\n[Activated User] {user_id}  send_email={send_email}")
    return data


def suspend_user(client: OktaClient, user_id: str) -> None:
    """POST /users/{userId}/lifecycle/suspend"""
    r = client.post_no_body(f"/users/{user_id}/lifecycle/suspend")
    r.raise_for_status()
    print(f"\n[Suspended User] {user_id}")


def reset_password(client: OktaClient, user_id: str,
                   send_email: bool = True) -> dict:
    """POST /users/{userId}/lifecycle/resetPassword"""
    r = client.post_no_body(
        f"/users/{user_id}/lifecycle/resetPassword?sendEmail={str(send_email).lower()}"
    )
    r.raise_for_status()
    data = r.json()
    print(f"\n[Password Reset] {user_id}  send_email={send_email}")
    return data


def delete_user(client: OktaClient, user_id: str) -> None:
    """DELETE /users/{userId} — user must be DEACTIVATED first"""
    r = client.delete(f"/users/{user_id}")
    r.raise_for_status()
    print(f"\n[Deleted User] {user_id}")


def list_user_groups(client: OktaClient, user_id: str) -> list[dict]:
    """GET /users/{userId}/groups"""
    r = client.get(f"/users/{user_id}/groups")
    r.raise_for_status()
    groups = r.json()
    print(f"\n[User Groups] {user_id}  {len(groups)} groups:")
    for g in groups:
        print(f"  {g['id']}  {g['profile']['name']}")
    return groups


def list_user_apps(client: OktaClient, user_id: str) -> list[dict]:
    """GET /users/{userId}/appLinks — apps assigned to a user"""
    r = client.get(f"/users/{user_id}/appLinks")
    r.raise_for_status()
    apps = r.json()
    print(f"\n[User Apps] {user_id}  {len(apps)} assigned:")
    for a in apps:
        print(f"  {a.get('appName','?'):25s}  {a.get('label','?')}")
    return apps


# ---------------------------------------------------------------------------
# Groups
# ---------------------------------------------------------------------------

def list_groups(client: OktaClient, limit: int = 20,
                query: str | None = None) -> list[dict]:
    """GET /groups"""
    params: dict = {"limit": limit}
    if query:
        params["q"] = query
    r = client.get("/groups", params=params)
    r.raise_for_status()
    groups = r.json()
    print(f"\n[Groups] {len(groups)} returned:")
    for g in groups:
        p = g.get("profile", {})
        count = g.get("objectClass", [])
        print(f"  {g['id']}  {p.get('name','?'):40s}  {p.get('description','')[:40]}")
    return groups


def get_group(client: OktaClient, group_id: str) -> dict:
    """GET /groups/{groupId}"""
    r = client.get(f"/groups/{group_id}")
    r.raise_for_status()
    g = r.json()
    print(f"\n[Group] {g['id']}  {g['profile']['name']}")
    return g


def list_group_members(client: OktaClient, group_id: str,
                       limit: int = 20) -> list[dict]:
    """GET /groups/{groupId}/users"""
    r = client.get(f"/groups/{group_id}/users", params={"limit": limit})
    r.raise_for_status()
    members = r.json()
    print(f"\n[Group Members] {group_id}  {len(members)} members:")
    for u in members:
        p = u.get("profile", {})
        print(f"  {u['id']}  {p.get('login','?'):35s}  {p.get('displayName','?')}")
    return members


def create_group(client: OktaClient, name: str,
                 description: str = "") -> dict:
    """POST /groups"""
    r = client.post("/groups", {"profile": {"name": name, "description": description}})
    r.raise_for_status()
    g = r.json()
    print(f"\n[Created Group] {g['id']}  {name}")
    return g


def add_user_to_group(client: OktaClient, group_id: str,
                      user_id: str) -> None:
    """PUT /groups/{groupId}/users/{userId}"""
    r = client.put(f"/groups/{group_id}/users/{user_id}", {})
    r.raise_for_status()
    print(f"\n[Added to Group] user={user_id} → group={group_id}")


def remove_user_from_group(client: OktaClient, group_id: str,
                           user_id: str) -> None:
    """DELETE /groups/{groupId}/users/{userId}"""
    r = client.delete(f"/groups/{group_id}/users/{user_id}")
    r.raise_for_status()
    print(f"\n[Removed from Group] user={user_id} ← group={group_id}")


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

def list_apps(client: OktaClient, limit: int = 20,
              active_only: bool = True) -> list[dict]:
    """GET /apps"""
    params: dict = {"limit": limit}
    if active_only:
        params["filter"] = 'status eq "ACTIVE"'
    r = client.get("/apps", params=params)
    r.raise_for_status()
    apps = r.json()
    print(f"\n[Apps] {len(apps)} returned:")
    for a in apps:
        print(f"  {a['id']}  [{a['status']:8s}]  [{a.get('name','?'):25s}]  {a['label']}")
    return apps


def get_app(client: OktaClient, app_id: str) -> dict:
    """GET /apps/{appId}"""
    r = client.get(f"/apps/{app_id}")
    r.raise_for_status()
    a = r.json()
    print(f"\n[App] {a['id']}  {a['label']}  ({a.get('name')})")
    print(f"  Status: {a['status']}  Sign-on: {a.get('signOnMode','?')}")
    return a


def list_app_users(client: OktaClient, app_id: str,
                   limit: int = 20) -> list[dict]:
    """GET /apps/{appId}/users"""
    r = client.get(f"/apps/{app_id}/users", params={"limit": limit})
    r.raise_for_status()
    users = r.json()
    print(f"\n[App Users] {app_id}  {len(users)} assigned:")
    for u in users:
        print(f"  {u['id']}  {u.get('credentials',{}).get('userName','?'):35s}  scope={u.get('scope','?')}")
    return users


def list_app_groups(client: OktaClient, app_id: str) -> list[dict]:
    """GET /apps/{appId}/groups"""
    r = client.get(f"/apps/{app_id}/groups")
    r.raise_for_status()
    groups = r.json()
    print(f"\n[App Groups] {app_id}  {len(groups)} assigned groups:")
    for g in groups:
        print(f"  {g['id']}  priority={g.get('priority','?')}")
    return groups


# ---------------------------------------------------------------------------
# MFA / Factors
# ---------------------------------------------------------------------------

def list_user_factors(client: OktaClient, user_id: str) -> list[dict]:
    """GET /users/{userId}/factors — enrolled MFA factors"""
    r = client.get(f"/users/{user_id}/factors")
    r.raise_for_status()
    factors = r.json()
    print(f"\n[MFA Factors] {user_id}  {len(factors)} enrolled:")
    for f in factors:
        print(f"  {f['id']}  [{f['status']:8s}]  {f['factorType']:20s}  {f.get('provider','?')}")
    return factors


def reset_user_factors(client: OktaClient, user_id: str) -> None:
    """DELETE /users/{userId}/factors — unenroll all MFA factors"""
    r = client.delete(f"/users/{user_id}/factors")
    r.raise_for_status()
    print(f"\n[Reset MFA] all factors cleared for {user_id}")


# ---------------------------------------------------------------------------
# System Log
# ---------------------------------------------------------------------------

def list_logs(client: OktaClient, since_minutes: int = 60,
              event_type: str | None = None,
              limit: int = 20) -> list[dict]:
    """GET /logs — system event log
    Common event types: user.session.start, user.authentication.sso,
    user.account.update_password, group.user_membership.add
    """
    from datetime import datetime, timezone, timedelta
    since = (datetime.now(timezone.utc) - timedelta(minutes=since_minutes)).isoformat()
    params: dict = {"since": since, "limit": limit, "sortOrder": "DESCENDING"}
    if event_type:
        params["filter"] = f'eventType eq "{event_type}"'
    r = client.get("/logs", params=params)
    r.raise_for_status()
    events = r.json()
    print(f"\n[System Logs] last {since_minutes}m  {len(events)} events:")
    for e in events:
        actor = e.get("actor", {}).get("displayName", "?")
        print(f"  {e.get('published','?')[:19]}  {e.get('eventType','?'):45s}  {actor}")
    return events


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Okta Management API examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  OKTA_DOMAIN     your-org.okta.com
  OKTA_API_TOKEN  Admin Console → Security → API → Tokens

Examples:
  python SAAS/okta/examples.py
  python SAAS/okta/examples.py --demo-write
  python SAAS/okta/examples.py --search 'profile.department eq "Engineering"'
        """,
    )
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--search", default=None, metavar="QUERY",
                        help="Okta search query, e.g. 'profile.department eq \"Eng\"'")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write ops (creates staged user, updates, then deletes)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = OktaClient.from_env()

    print(f"\n{'='*60}")
    print("Okta Examples")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    list_users(client, status="ACTIVE")
    list_groups(client)
    list_apps(client)
    list_logs(client, since_minutes=60)

    if args.search:
        search_users(client, args.search)

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        user = create_user(
            client,
            first="Example", last="User",
            email="example.testuser@example.com",
            activate=False,
        )
        uid = user["id"]

        update_user(client, uid, {"department": "Test", "title": "API Example"})
        time.sleep(1)

        # must deactivate before delete (even staged users need this on some orgs)
        try:
            deactivate_user(client, uid)
            time.sleep(1)
        except Exception:
            pass
        delete_user(client, uid)


if __name__ == "__main__":
    main()
