"""
GitHub REST API Examples
Covers: repos, issues, PRs, actions, releases, users, orgs, webhooks, Copilot

Auth:  GITHUB_TOKEN  (Personal Access Token or GitHub App token)
Docs:  https://docs.github.com/en/rest

Usage:
    # Read-only demo:
    python SAAS/github/examples.py

    # Include write operations (creates then closes a test issue):
    python SAAS/github/examples.py --demo-write --repo owner/repo
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


BASE = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        return requests.get(f"{BASE}{path}", headers=self.headers, params=params)

    def post(self, path: str, body: dict) -> requests.Response:
        return requests.post(f"{BASE}{path}", headers=self.headers, json=body)

    def patch(self, path: str, body: dict) -> requests.Response:
        return requests.patch(f"{BASE}{path}", headers=self.headers, json=body)

    def delete(self, path: str) -> requests.Response:
        return requests.delete(f"{BASE}{path}", headers=self.headers)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "GitHubClient":
        load_env(env_file)
        return cls(token=_require("GITHUB_TOKEN"))


# ---------------------------------------------------------------------------
# Authenticated user
# ---------------------------------------------------------------------------

def get_authenticated_user(client: GitHubClient) -> dict:
    """GET /user"""
    r = client.get("/user")
    r.raise_for_status()
    u = r.json()
    print(f"\n[Authenticated User] @{u['login']}  ({u.get('name','?')})")
    print(f"  Public repos: {u.get('public_repos')}  Followers: {u.get('followers')}")
    return u


# ---------------------------------------------------------------------------
# Repositories
# ---------------------------------------------------------------------------

def list_repos(client: GitHubClient, owner: str | None = None,
               max_results: int = 10) -> list[dict]:
    """GET /user/repos or /users/{owner}/repos"""
    path = f"/users/{owner}/repos" if owner else "/user/repos"
    r = client.get(path, params={"per_page": max_results, "sort": "updated"})
    r.raise_for_status()
    repos = r.json()
    print(f"\n[Repos] {len(repos)} returned:")
    for repo in repos:
        lang = repo.get("language") or "—"
        stars = repo.get("stargazers_count", 0)
        print(f"  {repo['full_name']:45s}  [{lang:12s}]  ★{stars}")
    return repos


def get_repo(client: GitHubClient, repo: str) -> dict:
    """GET /repos/{owner}/{repo}"""
    r = client.get(f"/repos/{repo}")
    r.raise_for_status()
    d = r.json()
    print(f"\n[Repo] {d['full_name']}")
    print(f"  {d.get('description') or '(no description)'}")
    print(f"  Stars: {d['stargazers_count']}  Forks: {d['forks_count']}  "
          f"Open issues: {d['open_issues_count']}")
    print(f"  Default branch: {d['default_branch']}  Language: {d.get('language')}")
    return d


def list_branches(client: GitHubClient, repo: str,
                  max_results: int = 20) -> list[dict]:
    """GET /repos/{owner}/{repo}/branches"""
    r = client.get(f"/repos/{repo}/branches", params={"per_page": max_results})
    r.raise_for_status()
    branches = r.json()
    print(f"\n[Branches] {repo}  ({len(branches)} returned):")
    for b in branches:
        protected = " [protected]" if b.get("protected") else ""
        print(f"  {b['name']}{protected}")
    return branches


def list_commits(client: GitHubClient, repo: str, branch: str | None = None,
                 max_results: int = 10) -> list[dict]:
    """GET /repos/{owner}/{repo}/commits"""
    params: dict = {"per_page": max_results}
    if branch:
        params["sha"] = branch
    r = client.get(f"/repos/{repo}/commits", params=params)
    r.raise_for_status()
    commits = r.json()
    print(f"\n[Commits] {repo}  ({len(commits)} returned):")
    for c in commits:
        sha = c["sha"][:7]
        author = c["commit"]["author"]["name"]
        msg = c["commit"]["message"].split("\n")[0][:60]
        print(f"  {sha}  {author:20s}  {msg}")
    return commits


def list_releases(client: GitHubClient, repo: str,
                  max_results: int = 5) -> list[dict]:
    """GET /repos/{owner}/{repo}/releases"""
    r = client.get(f"/repos/{repo}/releases", params={"per_page": max_results})
    r.raise_for_status()
    releases = r.json()
    print(f"\n[Releases] {repo}  ({len(releases)} returned):")
    for rel in releases:
        pre = " [pre-release]" if rel.get("prerelease") else ""
        print(f"  {rel['tag_name']:15s}  {rel.get('name','')[:40]}{pre}")
    return releases


def list_contributors(client: GitHubClient, repo: str,
                      max_results: int = 10) -> list[dict]:
    """GET /repos/{owner}/{repo}/contributors"""
    r = client.get(f"/repos/{repo}/contributors", params={"per_page": max_results})
    r.raise_for_status()
    contribs = r.json()
    print(f"\n[Contributors] {repo}:")
    for c in contribs:
        print(f"  @{c['login']:30s}  {c['contributions']} commits")
    return contribs


# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------

def list_issues(client: GitHubClient, repo: str, state: str = "open",
                max_results: int = 10) -> list[dict]:
    """GET /repos/{owner}/{repo}/issues"""
    r = client.get(f"/repos/{repo}/issues",
                   params={"state": state, "per_page": max_results, "sort": "updated"})
    r.raise_for_status()
    issues = [i for i in r.json() if "pull_request" not in i]  # exclude PRs
    print(f"\n[Issues ({state})] {repo}  {len(issues)} returned:")
    for i in issues:
        labels = ", ".join(l["name"] for l in i.get("labels", []))
        print(f"  #{i['number']:5d}  {i['title'][:55]}  [{labels}]")
    return issues


def get_issue(client: GitHubClient, repo: str, number: int) -> dict:
    """GET /repos/{owner}/{repo}/issues/{number}"""
    r = client.get(f"/repos/{repo}/issues/{number}")
    r.raise_for_status()
    i = r.json()
    print(f"\n[Issue #{i['number']}] {i['title']}")
    print(f"  State: {i['state']}  Author: @{i['user']['login']}")
    print(f"  Created: {i['created_at'][:10]}  Comments: {i['comments']}")
    return i


def create_issue(client: GitHubClient, repo: str, title: str,
                 body: str = "", labels: list[str] | None = None) -> dict:
    """POST /repos/{owner}/{repo}/issues"""
    payload: dict = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    r = client.post(f"/repos/{repo}/issues", payload)
    r.raise_for_status()
    i = r.json()
    print(f"\n[Created Issue] #{i['number']} {i['title']}")
    return i


def update_issue(client: GitHubClient, repo: str, number: int,
                 state: str | None = None, title: str | None = None,
                 body: str | None = None) -> dict:
    """PATCH /repos/{owner}/{repo}/issues/{number}"""
    payload: dict = {}
    if state:
        payload["state"] = state
    if title:
        payload["title"] = title
    if body:
        payload["body"] = body
    r = client.patch(f"/repos/{repo}/issues/{number}", payload)
    r.raise_for_status()
    i = r.json()
    print(f"\n[Updated Issue] #{i['number']} → {i['state']}")
    return i


def add_issue_comment(client: GitHubClient, repo: str, number: int,
                      body: str) -> dict:
    """POST /repos/{owner}/{repo}/issues/{number}/comments"""
    r = client.post(f"/repos/{repo}/issues/{number}/comments", {"body": body})
    r.raise_for_status()
    c = r.json()
    print(f"\n[Comment added] issue #{number}: {body[:60]}")
    return c


# ---------------------------------------------------------------------------
# Pull Requests
# ---------------------------------------------------------------------------

def list_pull_requests(client: GitHubClient, repo: str, state: str = "open",
                       max_results: int = 10) -> list[dict]:
    """GET /repos/{owner}/{repo}/pulls"""
    r = client.get(f"/repos/{repo}/pulls",
                   params={"state": state, "per_page": max_results, "sort": "updated"})
    r.raise_for_status()
    prs = r.json()
    print(f"\n[Pull Requests ({state})] {repo}  {len(prs)} returned:")
    for pr in prs:
        draft = " [draft]" if pr.get("draft") else ""
        print(f"  #{pr['number']:5d}  {pr['title'][:55]}{draft}  ← {pr['head']['ref']}")
    return prs


def get_pull_request(client: GitHubClient, repo: str, number: int) -> dict:
    """GET /repos/{owner}/{repo}/pulls/{number}"""
    r = client.get(f"/repos/{repo}/pulls/{number}")
    r.raise_for_status()
    pr = r.json()
    print(f"\n[PR #{pr['number']}] {pr['title']}")
    print(f"  State: {pr['state']}  Mergeable: {pr.get('mergeable')}")
    print(f"  {pr['head']['ref']} → {pr['base']['ref']}  +{pr.get('additions')} -{pr.get('deletions')}")
    return pr


def list_pr_reviews(client: GitHubClient, repo: str, number: int) -> list[dict]:
    """GET /repos/{owner}/{repo}/pulls/{number}/reviews"""
    r = client.get(f"/repos/{repo}/pulls/{number}/reviews")
    r.raise_for_status()
    reviews = r.json()
    print(f"\n[PR Reviews] #{number}  {len(reviews)} reviews:")
    for rev in reviews:
        print(f"  @{rev['user']['login']:25s}  {rev['state']}")
    return reviews


# ---------------------------------------------------------------------------
# Actions (CI/CD)
# ---------------------------------------------------------------------------

def list_workflows(client: GitHubClient, repo: str) -> list[dict]:
    """GET /repos/{owner}/{repo}/actions/workflows"""
    r = client.get(f"/repos/{repo}/actions/workflows")
    r.raise_for_status()
    workflows = r.json().get("workflows", [])
    print(f"\n[Workflows] {repo}  {len(workflows)} workflows:")
    for wf in workflows:
        print(f"  {wf['id']:10d}  [{wf['state']:8s}]  {wf['name']}")
    return workflows


def list_workflow_runs(client: GitHubClient, repo: str,
                       workflow_id: int | str | None = None,
                       max_results: int = 10) -> list[dict]:
    """GET /repos/{owner}/{repo}/actions/runs or /actions/workflows/{id}/runs"""
    if workflow_id:
        path = f"/repos/{repo}/actions/workflows/{workflow_id}/runs"
    else:
        path = f"/repos/{repo}/actions/runs"
    r = client.get(path, params={"per_page": max_results})
    r.raise_for_status()
    runs = r.json().get("workflow_runs", [])
    print(f"\n[Workflow Runs] {len(runs)} returned:")
    for run in runs:
        print(f"  #{run['run_number']:5d}  [{run['status']:10s}]  [{run.get('conclusion') or '—':10s}]  "
              f"{run['name'][:40]}  {run['head_branch']}")
    return runs


def get_workflow_run(client: GitHubClient, repo: str, run_id: int) -> dict:
    """GET /repos/{owner}/{repo}/actions/runs/{run_id}"""
    r = client.get(f"/repos/{repo}/actions/runs/{run_id}")
    r.raise_for_status()
    run = r.json()
    print(f"\n[Workflow Run] #{run['run_number']}  {run['name']}")
    print(f"  Status: {run['status']}  Conclusion: {run.get('conclusion')}")
    print(f"  Branch: {run['head_branch']}  SHA: {run['head_sha'][:7]}")
    print(f"  Started: {run.get('run_started_at','?')[:19]}")
    return run


def trigger_workflow(client: GitHubClient, repo: str, workflow_id: int | str,
                     ref: str = "main", inputs: dict | None = None) -> None:
    """POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"""
    payload: dict = {"ref": ref}
    if inputs:
        payload["inputs"] = inputs
    r = client.post(f"/repos/{repo}/actions/workflows/{workflow_id}/dispatches", payload)
    r.raise_for_status()
    print(f"\n[Workflow triggered] {workflow_id} on {ref}")


# ---------------------------------------------------------------------------
# Org & Teams
# ---------------------------------------------------------------------------

def get_org(client: GitHubClient, org: str) -> dict:
    """GET /orgs/{org}"""
    r = client.get(f"/orgs/{org}")
    r.raise_for_status()
    o = r.json()
    print(f"\n[Org] {o['login']}  ({o.get('name','?')})")
    print(f"  Public repos: {o.get('public_repos')}  Members: {o.get('members_count','?')}")
    return o


def list_org_members(client: GitHubClient, org: str,
                     max_results: int = 20) -> list[dict]:
    """GET /orgs/{org}/members"""
    r = client.get(f"/orgs/{org}/members", params={"per_page": max_results})
    r.raise_for_status()
    members = r.json()
    print(f"\n[Org Members] {org}  {len(members)} returned:")
    for m in members:
        print(f"  @{m['login']}")
    return members


def list_org_teams(client: GitHubClient, org: str,
                   max_results: int = 20) -> list[dict]:
    """GET /orgs/{org}/teams"""
    r = client.get(f"/orgs/{org}/teams", params={"per_page": max_results})
    r.raise_for_status()
    teams = r.json()
    print(f"\n[Teams] {org}  {len(teams)} returned:")
    for t in teams:
        print(f"  {t['slug']:30s}  {t.get('members_count','?')} members")
    return teams


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------

def list_repo_webhooks(client: GitHubClient, repo: str) -> list[dict]:
    """GET /repos/{owner}/{repo}/hooks"""
    r = client.get(f"/repos/{repo}/hooks")
    r.raise_for_status()
    hooks = r.json()
    print(f"\n[Webhooks] {repo}  {len(hooks)} hooks:")
    for h in hooks:
        events = ", ".join(h.get("events", []))
        print(f"  {h['id']}  [{h['config'].get('url','?')[:50]}]  events: {events}")
    return hooks


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="GitHub API examples")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--repo", default=None, metavar="OWNER/REPO",
                        help="Target repo (overrides GITHUB_REPO env var)")
    parser.add_argument("--org", default=None, metavar="ORG",
                        help="Target org (overrides GITHUB_ORG env var)")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (creates then closes a test issue)")
    args = parser.parse_args()

    load_env(args.env_file)
    client = GitHubClient.from_env()

    print(f"\n{'='*60}")
    print("GitHub Examples")
    print(f"{'='*60}")

    # ── Read-only ────────────────────────────────────────────────────────────
    user = get_authenticated_user(client)
    list_repos(client)

    repo = args.repo or os.environ.get("GITHUB_REPO", "")
    org  = args.org  or os.environ.get("GITHUB_ORG", "")

    if repo:
        get_repo(client, repo)
        list_branches(client, repo)
        list_commits(client, repo)
        list_issues(client, repo)
        list_pull_requests(client, repo)
        list_workflows(client, repo)
        list_workflow_runs(client, repo)
        list_releases(client, repo)
        list_contributors(client, repo)
        list_repo_webhooks(client, repo)
    else:
        print("\n[Read] Set GITHUB_REPO or pass --repo owner/repo for repo-level examples")

    if org:
        get_org(client, org)
        list_org_members(client, org)
        list_org_teams(client, org)
    else:
        print("\n[Read] Set GITHUB_ORG or pass --org for org-level examples")

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        if not repo:
            print("\n[Write] Set GITHUB_REPO or pass --repo to test issue creation")
        else:
            issue = create_issue(
                client, repo,
                title="[EXAMPLE] API test — safe to close",
                body="Created by `SAAS/github/examples.py`. Close immediately.",
                labels=["documentation"],
            )
            number = issue["number"]
            add_issue_comment(client, repo, number,
                              "Automated test comment from examples.py")
            time.sleep(1)
            update_issue(client, repo, number, state="closed")


if __name__ == "__main__":
    main()
