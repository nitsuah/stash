"""
Shared base clients for Atlassian Cloud API examples.

Handles credential loading from environment variables or a .env file.
All service example scripts import from here.
"""

import base64
import os
import sys
from typing import Any

import requests


# ---------------------------------------------------------------------------
# Env loader
# ---------------------------------------------------------------------------

def load_env(path: str | None = None) -> None:
    """Load a .env file into os.environ (no-op if file not found)."""
    if path is None:
        # Look next to this file first, then the caller's directory
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(here, ".env"),
            os.path.join(os.getcwd(), ".env"),
        ]
        path = next((p for p in candidates if os.path.exists(p)), None)
    if not path or not os.path.exists(path):
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


def require(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        print(f"ERROR: env var '{name}' is not set.", file=sys.stderr)
        print("Copy atlassian/.env.example → atlassian/.env and fill in values.", file=sys.stderr)
        sys.exit(1)
    return val


# ---------------------------------------------------------------------------
# Atlassian Cloud client  (Jira + Confluence — same credentials)
# ---------------------------------------------------------------------------

class AtlassianClient:
    """HTTP client for Jira and Confluence Cloud (Basic auth: email + API token)."""

    def __init__(self, host: str, email: str, token: str):
        self.base = host.rstrip("/")
        creds = base64.b64encode(f"{email}:{token}".encode()).decode()
        self.headers: dict[str, str] = {
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

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "AtlassianClient":
        load_env(env_file)
        return cls(
            host=require("JIRA_HOST"),
            email=require("JIRA_EMAIL"),
            token=require("JIRA_TOKEN"),
        )


# ---------------------------------------------------------------------------
# Bitbucket Cloud client  (Basic auth: username + app password)
# ---------------------------------------------------------------------------

class BitbucketClient:
    """HTTP client for Bitbucket Cloud (Basic auth: username + app password)."""

    BASE = "https://api.bitbucket.org"

    def __init__(self, workspace: str, username: str, app_password: str):
        self.workspace = workspace
        creds = base64.b64encode(f"{username}:{app_password}".encode()).decode()
        self.headers: dict[str, str] = {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return requests.get(f"{self.BASE}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict) -> requests.Response:
        return requests.post(f"{self.BASE}{path}", headers=self.headers, json=body)

    def put(self, path: str, body: dict) -> requests.Response:
        return requests.put(f"{self.BASE}{path}", headers=self.headers, json=body)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(f"{self.BASE}{path}", headers=self.headers)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "BitbucketClient":
        load_env(env_file)
        return cls(
            workspace=require("BITBUCKET_WORKSPACE"),
            username=require("BITBUCKET_USERNAME"),
            app_password=require("BITBUCKET_APP_PASSWORD"),
        )


# ---------------------------------------------------------------------------
# Statuspage client  (API key via Authorization header)
# ---------------------------------------------------------------------------

class StatuspageClient:
    """HTTP client for Atlassian Statuspage (OAuth API key)."""

    BASE = "https://api.statuspage.io"

    def __init__(self, api_key: str, page_id: str):
        self.page_id = page_id
        self.headers: dict[str, str] = {
            "Authorization": f"OAuth {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return requests.get(f"{self.BASE}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict) -> requests.Response:
        return requests.post(f"{self.BASE}{path}", headers=self.headers, json=body)

    def patch(self, path: str, body: dict) -> requests.Response:
        return requests.patch(f"{self.BASE}{path}", headers=self.headers, json=body)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(f"{self.BASE}{path}", headers=self.headers)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "StatuspageClient":
        load_env(env_file)
        return cls(
            api_key=require("STATUSPAGE_API_KEY"),
            page_id=require("STATUSPAGE_PAGE_ID"),
        )
