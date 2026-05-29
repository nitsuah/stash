"""
Bitbucket Cloud API Examples
Covers: repositories, branches, pull requests, pipelines, issues, webhooks

Auth:  BITBUCKET_WORKSPACE, BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD
       (App password needs: Repositories read, Pull requests read, Pipelines read)
Docs:  https://developer.atlassian.com/cloud/bitbucket/rest/

Usage:
    # Read-only demo (lists repos in your workspace):
    python atlassian/bitbucket/examples.py

    # Target a specific repo:
    python atlassian/bitbucket/examples.py --repo my-repo-slug

    # Include write operations (creates then deletes a test issue):
    python atlassian/bitbucket/examples.py --repo my-repo-slug --demo-write
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import BitbucketClient, load_env


# ---------------------------------------------------------------------------
# Workspace / Repositories
# ---------------------------------------------------------------------------

def list_repos(client: BitbucketClient, max_results: int = 10) -> list[dict]:
    """GET /2.0/repositories/{workspace}"""
    r = client.get(f"/2.0/repositories/{client.workspace}",
                   params={"pagelen": max_results, "sort": "-updated_on"})
    r.raise_for_status()
    repos = r.json().get("values", [])
    print(f"\n[Repos in {client.workspace}] {len(repos)} returned:")
    for repo in repos:
        print(f"  {repo['slug']:30s}  {repo.get('scm','?')}  "
              f"{'private' if repo.get('is_private') else 'public'}")
    return repos


def get_repo(client: BitbucketClient, repo_slug: str) -> dict:
    """GET /2.0/repositories/{workspace}/{repoSlug}"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}")
    r.raise_for_status()
    repo = r.json()
    print(f"\n[Repo] {repo['full_name']}")
    print(f"  SCM: {repo.get('scm')}  Private: {repo.get('is_private')}"
          f"  Language: {repo.get('language','n/a')}")
    print(f"  Updated: {repo.get('updated_on','?')[:10]}")
    return repo


def create_repo(client: BitbucketClient, repo_slug: str,
                private: bool = True, scm: str = "git") -> dict:
    """POST /2.0/repositories/{workspace}/{repoSlug}"""
    body = {
        "scm": scm,
        "is_private": private,
        "project": {"key": "DEFAULT"},
    }
    r = client.post(f"/2.0/repositories/{client.workspace}/{repo_slug}", body)
    r.raise_for_status()
    repo = r.json()
    print(f"\n[Created Repo] {repo['full_name']}")
    return repo


def delete_repo(client: BitbucketClient, repo_slug: str) -> bool:
    """DELETE /2.0/repositories/{workspace}/{repoSlug}"""
    r = client.delete(f"/2.0/repositories/{client.workspace}/{repo_slug}")
    ok = r.status_code == 204
    print(f"\n[{'Deleted' if ok else 'Delete failed'}] Repo {repo_slug}")
    return ok


# ---------------------------------------------------------------------------
# Branches & Commits
# ---------------------------------------------------------------------------

def list_branches(client: BitbucketClient, repo_slug: str,
                  max_results: int = 10) -> list[dict]:
    """GET /2.0/repositories/{workspace}/{repoSlug}/refs/branches"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}/refs/branches",
                   params={"pagelen": max_results})
    r.raise_for_status()
    branches = r.json().get("values", [])
    print(f"\n[Branches — {repo_slug}] {len(branches)} returned:")
    for b in branches:
        head = b.get("target", {}).get("hash", "?")[:8]
        print(f"  {b['name']:40s}  {head}")
    return branches


def list_commits(client: BitbucketClient, repo_slug: str,
                 branch: str = "main", max_results: int = 10) -> list[dict]:
    """GET /2.0/repositories/{workspace}/{repoSlug}/commits/{branch}"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}/commits/{branch}",
                   params={"pagelen": max_results})
    r.raise_for_status()
    commits = r.json().get("values", [])
    print(f"\n[Commits on {branch} — {repo_slug}] {len(commits)} returned:")
    for c in commits:
        author = c.get("author", {}).get("user", {}).get("display_name", "?")
        msg = c.get("message", "").split("\n")[0][:50]
        print(f"  {c['hash'][:8]}  {author:20s}  {msg}")
    return commits


# ---------------------------------------------------------------------------
# Pull Requests
# ---------------------------------------------------------------------------

def list_pull_requests(client: BitbucketClient, repo_slug: str,
                       state: str = "OPEN", max_results: int = 10) -> list[dict]:
    """GET /2.0/repositories/{workspace}/{repoSlug}/pullrequests"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}/pullrequests",
                   params={"state": state, "pagelen": max_results})
    r.raise_for_status()
    prs = r.json().get("values", [])
    print(f"\n[Pull Requests ({state}) — {repo_slug}] {len(prs)} returned:")
    for pr in prs:
        author = pr.get("author", {}).get("display_name", "?")
        src = pr.get("source", {}).get("branch", {}).get("name", "?")
        dst = pr.get("destination", {}).get("branch", {}).get("name", "?")
        print(f"  #{pr['id']:5d}  [{src} → {dst}]  {pr['title'][:40]}  by {author}")
    return prs


def get_pull_request(client: BitbucketClient, repo_slug: str, pr_id: int) -> dict:
    """GET /2.0/repositories/{workspace}/{repoSlug}/pullrequests/{id}"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}/pullrequests/{pr_id}")
    r.raise_for_status()
    pr = r.json()
    print(f"\n[PR #{pr['id']}] {pr['title']}")
    print(f"  State: {pr['state']}  Author: {pr.get('author',{}).get('display_name','?')}")
    print(f"  {pr.get('source',{}).get('branch',{}).get('name','?')} → "
          f"{pr.get('destination',{}).get('branch',{}).get('name','?')}")
    return pr


def create_pull_request(client: BitbucketClient, repo_slug: str, title: str,
                         source_branch: str, dest_branch: str = "main",
                         description: str = "") -> dict:
    """POST /2.0/repositories/{workspace}/{repoSlug}/pullrequests"""
    body = {
        "title": title,
        "description": description,
        "source": {"branch": {"name": source_branch}},
        "destination": {"branch": {"name": dest_branch}},
    }
    r = client.post(f"/2.0/repositories/{client.workspace}/{repo_slug}/pullrequests", body)
    r.raise_for_status()
    pr = r.json()
    print(f"\n[Created PR] #{pr['id']}: {pr['title']}")
    return pr


# ---------------------------------------------------------------------------
# Pipelines
# ---------------------------------------------------------------------------

def list_pipelines(client: BitbucketClient, repo_slug: str,
                   max_results: int = 10) -> list[dict]:
    """GET /2.0/repositories/{workspace}/{repoSlug}/pipelines"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}/pipelines",
                   params={"pagelen": max_results, "sort": "-created_on"})
    if r.status_code == 404:
        print(f"\n[Pipelines] Not enabled on {repo_slug}")
        return []
    r.raise_for_status()
    pipelines = r.json().get("values", [])
    print(f"\n[Pipelines — {repo_slug}] {len(pipelines)} returned:")
    for p in pipelines:
        state = p.get("state", {})
        status = state.get("result", {}).get("name") or state.get("name", "?")
        branch = p.get("target", {}).get("ref_name", "?")
        print(f"  #{p['build_number']:5d}  [{status:12s}]  {branch}")
    return pipelines


def trigger_pipeline(client: BitbucketClient, repo_slug: str,
                     branch: str = "main") -> dict:
    """POST /2.0/repositories/{workspace}/{repoSlug}/pipelines"""
    body = {
        "target": {
            "ref_type": "branch",
            "type": "pipeline_ref_target",
            "ref_name": branch,
        }
    }
    r = client.post(f"/2.0/repositories/{client.workspace}/{repo_slug}/pipelines", body)
    r.raise_for_status()
    p = r.json()
    print(f"\n[Pipeline Triggered] #{p.get('build_number')} on {branch}")
    return p


# ---------------------------------------------------------------------------
# Issues  (only on repos with issues enabled)
# ---------------------------------------------------------------------------

def list_issues(client: BitbucketClient, repo_slug: str,
                max_results: int = 10) -> list[dict]:
    """GET /2.0/repositories/{workspace}/{repoSlug}/issues"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}/issues",
                   params={"pagelen": max_results})
    if r.status_code == 404:
        print(f"\n[Issues] Not enabled on {repo_slug}")
        return []
    r.raise_for_status()
    issues = r.json().get("values", [])
    print(f"\n[Issues — {repo_slug}] {len(issues)} returned:")
    for i in issues:
        print(f"  #{i['id']:5d}  [{i.get('status','?'):10s}]  {i.get('title','?')}")
    return issues


def create_issue(client: BitbucketClient, repo_slug: str, title: str,
                 content: str = "", kind: str = "bug") -> dict:
    """POST /2.0/repositories/{workspace}/{repoSlug}/issues"""
    body = {"title": title, "content": {"raw": content}, "kind": kind}
    r = client.post(f"/2.0/repositories/{client.workspace}/{repo_slug}/issues", body)
    r.raise_for_status()
    issue = r.json()
    print(f"\n[Created Issue] #{issue['id']}: {title}")
    return issue


def delete_issue(client: BitbucketClient, repo_slug: str, issue_id: int) -> bool:
    """DELETE /2.0/repositories/{workspace}/{repoSlug}/issues/{id}"""
    r = client.delete(f"/2.0/repositories/{client.workspace}/{repo_slug}/issues/{issue_id}")
    ok = r.status_code == 200
    print(f"\n[{'Deleted' if ok else 'Delete failed'}] Issue #{issue_id}")
    return ok


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------

def list_webhooks(client: BitbucketClient, repo_slug: str) -> list[dict]:
    """GET /2.0/repositories/{workspace}/{repoSlug}/hooks"""
    r = client.get(f"/2.0/repositories/{client.workspace}/{repo_slug}/hooks")
    r.raise_for_status()
    hooks = r.json().get("values", [])
    print(f"\n[Webhooks — {repo_slug}] {len(hooks)} found:")
    for h in hooks:
        events = ", ".join(h.get("events", []))
        print(f"  {h['uuid']}  active:{h.get('active')}  {h.get('url','?')[:50]}")
        print(f"    events: {events}")
    return hooks


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Bitbucket Cloud API examples")
    parser.add_argument("--repo", default=None, metavar="SLUG",
                        help="Repository slug to use for examples")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (creates then deletes a test issue)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = BitbucketClient.from_env()

    print(f"\n{'='*60}")
    print(f"Bitbucket Cloud Examples  —  workspace: {client.workspace}")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    repos = list_repos(client)

    repo_slug = args.repo or (repos[0]["slug"] if repos else None)
    if repo_slug:
        get_repo(client, repo_slug)
        list_branches(client, repo_slug)
        list_commits(client, repo_slug)
        list_pull_requests(client, repo_slug)
        list_pipelines(client, repo_slug)
        list_issues(client, repo_slug)
        list_webhooks(client, repo_slug)

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        if not repo_slug:
            print("\n[Write] --repo SLUG required for write demo")
            return
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")
        issue = create_issue(client, repo_slug,
                             title="[EXAMPLE] API test — safe to delete",
                             content="Created by atlassian/bitbucket/examples.py",
                             kind="task")
        delete_issue(client, repo_slug, issue["id"])


if __name__ == "__main__":
    main()
