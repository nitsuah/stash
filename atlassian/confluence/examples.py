"""
Confluence Cloud API Examples
Covers: spaces, pages, search, labels, attachments

Auth:  JIRA_HOST, JIRA_EMAIL, JIRA_TOKEN  (same credentials as Jira)
Docs:  https://developer.atlassian.com/cloud/confluence/rest/v1/

Usage:
    # Read-only demo:
    python atlassian/confluence/examples.py

    # Include write operations (creates then deletes a test page):
    python atlassian/confluence/examples.py --demo-write --space MYSPACE
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import AtlassianClient, load_env


# Confluence REST API lives under /wiki on the same host as Jira
WIKI = "/wiki/rest/api"


# ---------------------------------------------------------------------------
# Spaces
# ---------------------------------------------------------------------------

def list_spaces(client: AtlassianClient, max_results: int = 10) -> list[dict]:
    """GET /wiki/rest/api/space"""
    r = client.get(f"{WIKI}/space", params={"limit": max_results, "type": "global"})
    r.raise_for_status()
    spaces = r.json().get("results", [])
    print(f"\n[Spaces] {len(spaces)} returned (of {r.json().get('size','?')} total):")
    for s in spaces:
        print(f"  {s['key']:12s}  {s['name']}")
    return spaces


def get_space(client: AtlassianClient, space_key: str) -> dict:
    """GET /wiki/rest/api/space/{spaceKey}"""
    r = client.get(f"{WIKI}/space/{space_key}")
    r.raise_for_status()
    s = r.json()
    print(f"\n[Space] {s['key']}: {s['name']}  (type: {s.get('type','?')})")
    return s


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def list_pages_in_space(client: AtlassianClient, space_key: str,
                         max_results: int = 10) -> list[dict]:
    """GET /wiki/rest/api/space/{spaceKey}/content/page"""
    r = client.get(f"{WIKI}/space/{space_key}/content/page",
                   params={"limit": max_results, "expand": "version"})
    r.raise_for_status()
    pages = r.json().get("results", [])
    print(f"\n[Pages in {space_key}] {len(pages)} returned:")
    for p in pages:
        ver = p.get("version", {}).get("number", "?")
        print(f"  {p['id']:12s}  v{ver}  {p['title']}")
    return pages


def get_page(client: AtlassianClient, page_id: str,
             expand: str = "body.storage,version") -> dict:
    """GET /wiki/rest/api/content/{pageId}"""
    r = client.get(f"{WIKI}/content/{page_id}", params={"expand": expand})
    r.raise_for_status()
    p = r.json()
    ver = p.get("version", {}).get("number", "?")
    print(f"\n[Page] {p['id']}  v{ver}  '{p['title']}'")
    body_len = len(p.get("body", {}).get("storage", {}).get("value", ""))
    print(f"  Body length: {body_len} chars")
    return p


def create_page(client: AtlassianClient, space_key: str, title: str,
                body_html: str = "", parent_id: str | None = None) -> dict:
    """POST /wiki/rest/api/content"""
    payload: dict = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": body_html or f"<p>Page created via API: {title}</p>",
                "representation": "storage",
            }
        },
    }
    if parent_id:
        payload["ancestors"] = [{"id": parent_id}]
    r = client.post(f"{WIKI}/content", payload)
    r.raise_for_status()
    p = r.json()
    print(f"\n[Created Page] {p['id']}  '{p['title']}'  in space {space_key}")
    return p


def update_page(client: AtlassianClient, page_id: str, new_title: str,
                new_body_html: str, current_version: int) -> dict:
    """PUT /wiki/rest/api/content/{pageId}  — version number must be current+1"""
    payload = {
        "type": "page",
        "title": new_title,
        "version": {"number": current_version + 1},
        "body": {
            "storage": {
                "value": new_body_html,
                "representation": "storage",
            }
        },
    }
    r = client.put(f"{WIKI}/content/{page_id}", payload)
    r.raise_for_status()
    p = r.json()
    print(f"\n[Updated Page] {p['id']}  '{p['title']}'  → v{p['version']['number']}")
    return p


def delete_page(client: AtlassianClient, page_id: str) -> bool:
    """DELETE /wiki/rest/api/content/{pageId}"""
    r = client.delete(f"{WIKI}/content/{page_id}")
    ok = r.status_code == 204
    print(f"\n[{'Deleted' if ok else 'Delete failed'}] Page {page_id}")
    return ok


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search_content(client: AtlassianClient, cql: str, max_results: int = 10) -> list[dict]:
    """GET /wiki/rest/api/search  — CQL query
    Example CQL: space = "MYSPACE" AND type = page AND title ~ "API"
    """
    r = client.get(f"{WIKI}/search", params={"cql": cql, "limit": max_results})
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])
    print(f"\n[Search] '{cql}'")
    print(f"  {data.get('totalSize','?')} total — showing {len(results)}:")
    for item in results:
        content = item.get("content", {})
        print(f"  {content.get('id','?'):12s}  [{content.get('type','?'):6s}]  {item.get('title','?')}")
    return results


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

def get_page_labels(client: AtlassianClient, page_id: str) -> list[dict]:
    """GET /wiki/rest/api/content/{pageId}/label"""
    r = client.get(f"{WIKI}/content/{page_id}/label")
    r.raise_for_status()
    labels = r.json().get("results", [])
    names = [l["name"] for l in labels]
    print(f"\n[Labels on {page_id}] {names or '(none)'}")
    return labels


def add_label(client: AtlassianClient, page_id: str, label: str) -> dict:
    """POST /wiki/rest/api/content/{pageId}/label"""
    r = client.post(f"{WIKI}/content/{page_id}/label", [{"prefix": "global", "name": label}])
    r.raise_for_status()
    print(f"\n[Label added] '{label}' on page {page_id}")
    return r.json()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Confluence Cloud API examples")
    parser.add_argument("--space", default=None, metavar="KEY",
                        help="Space key to use for examples (e.g. MYSPACE)")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (creates then deletes a test page)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = AtlassianClient.from_env()

    print(f"\n{'='*60}")
    print(f"Confluence Cloud Examples  —  {client.base}")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    spaces = list_spaces(client)

    space_key = args.space or (spaces[0]["key"] if spaces else None)
    if space_key:
        get_space(client, space_key)
        pages = list_pages_in_space(client, space_key, max_results=5)
        search_content(client, f'space = "{space_key}" AND type = page', max_results=5)
        if pages:
            get_page(client, pages[0]["id"])
            get_page_labels(client, pages[0]["id"])

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        if not space_key:
            print("\n[Write] --space KEY required for write demo")
            return
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")
        page = create_page(
            client, space_key,
            title="[EXAMPLE] API test — safe to delete",
            body_html="<p>Created by <code>atlassian/confluence/examples.py</code>.</p>",
        )
        page_id = page["id"]
        get_page(client, page_id)
        add_label(client, page_id, "api-example")
        update_page(client, page_id,
                    new_title="[EXAMPLE] API test — updated",
                    new_body_html="<p>Updated by API example.</p>",
                    current_version=page["version"]["number"])
        delete_page(client, page_id)


if __name__ == "__main__":
    main()
