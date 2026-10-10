"""Visual board: per-repo promo / visual-docs status for every tracked public repo.

Reads each local clone's origin default branch (after a fetch) and two GitHub
settings, scores eleven columns, and picks one "today" gap to work on. The
artifact page (agent/scripts/visual-board-page.html) renders the JSON this writes.

Usage:
  python agent/scripts/visual_board.py [--out PATH] [--no-fetch]

Default output: agent/reports/visual/visual-board.json (not committed; the
artifact holds the published copy).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sotu  # noqa: E402  (shares the tracked-repo list and tiers)

OUT = sotu.STASH / "agent" / "reports" / "visual" / "visual-board.json"

# Column order is also the pick order within a repo: cheapest, most unblocking first.
COLUMNS = [
    ("actions_pr", "Actions PRs"),
    ("spots", "Promo manifest"),
    ("screenshots", "Screenshots"),
    ("pages", "Pages"),
    ("linked", "Features linked"),
    ("videos", "Spots published"),
    ("diagrams", "Diagrams"),
    ("brand", "Brand"),
    ("reels", "Hero reel"),
    ("journeys", "Journeys"),
    ("vertical", "Vertical"),
]


def run(*cmd: str) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def git(path: str, *args: str) -> str:
    code, out = run("git", "-C", path, *args)
    return out if code == 0 else ""


def gh(path: str, query: str) -> str | None:
    code, out = run("gh", "api", path, "-q", query)
    return out.strip() if code == 0 else None


def fix_hint(col: str, repo: dict) -> str:
    path, full = repo["path"], repo["full_name"]
    return {
        "actions_pr": f"gh api -X PUT repos/{full}/actions/permissions/workflow -f default_workflow_permissions=read -F can_approve_pull_request_reviews=true",
        "spots": f"Run /promo in {path} (first run: builds promo/spots.json from FEATURES.md)",
        "screenshots": f"Run /promo in {path} and add its screenshot CI workflow, so screenshots regenerate and get committed",
        "pages": f"Run /promo in {path} to set up the GitHub Pages site",
        "linked": f"Run /promo in {path}: link the visual features in promo/spots.json to spots or screenshots",
        "videos": f"Run /promo in {path}: render and publish the remaining spots",
        "diagrams": f"Add a Mermaid architecture diagram to {path} with a CI render step (recipe pending in vigil's visual-docs epic)",
        "brand": f"Run /promo in {path}: brand step (logo, favicon, colors)",
        "reels": f"Run /promo in {path}: combine the spots into a hero reel",
        "journeys": f"Run /journeys in {path}",
        "vertical": f"Run /promo in {path}: cut a vertical short",
    }[col]


def scan(repo: dict, fetch: bool) -> dict:
    p = repo["path"]
    if fetch:
        run("git", "-C", p, "fetch", "-q", "origin")
    ref = git(p, "symbolic-ref", "--short", "refs/remotes/origin/HEAD").strip() or "origin/main"
    files = git(p, "ls-tree", "-r", "--name-only", ref).splitlines()
    found = bool(files)

    spots_raw = git(p, "show", f"{ref}:promo/spots.json")
    s = {}
    if spots_raw:
        try:
            d = json.loads(spots_raw)
            feats, sp = d.get("features", []), d.get("spots", [])
            visual = [f for f in feats if f.get("visual") != "none"]
            s = {"features": len(feats), "visual": len(visual),
                 "linked": sum(1 for f in visual if f.get("spots") or f.get("screenshots")),
                 "spots": len(sp), "published": sum(1 for x in sp if x.get("published")),
                 "reels": len(d.get("reels") or []), "brand": bool(d.get("brand")),
                 "vertical": sum(1 for x in sp if x.get("format") in ("vertical", "portrait"))}
        except ValueError:
            s = {}

    wf = [f for f in files if f.startswith(".github/workflows/")]
    wftext = " ".join(git(p, "show", f"{ref}:{f}") for f in wf).lower()
    shots = [f for f in files if re.search(r"(screenshots?|gallery)/.*\.(png|jpe?g|webp)$", f, re.I)]
    diags = [f for f in files if re.search(r"\.(mmd|excalidraw|drawio)$|diagrams?/.*\.(svg|png)$", f, re.I)]
    shot_ci = "screenshot" in wftext
    diag_ci = bool(re.search(r"mermaid|mmdc|excalidraw|diagram", wftext))
    journeys = "journey" in wftext or any("journeys" in f for f in files)
    pages = gh(f"repos/{repo['full_name']}/pages", ".html_url")
    approve = gh(f"repos/{repo['full_name']}/actions/permissions/workflow", ".can_approve_pull_request_reviews")

    def cell(status: str, label: str) -> dict:
        return {"status": status, "label": label}

    c = {}
    c["actions_pr"] = cell("ok", "on") if approve == "true" else cell("missing", "off" if approve else "unknown")
    c["spots"] = cell("ok", f"{s['features']} features") if s else cell("missing", "none")
    if shot_ci and shots:
        c["screenshots"] = cell("ok", f"CI · {len(shots)}")
    elif shots:
        c["screenshots"] = cell("partial", f"static · {len(shots)}")
    elif shot_ci:
        c["screenshots"] = cell("partial", "CI, none committed")
    else:
        c["screenshots"] = cell("missing", "none")
    c["pages"] = cell("ok", "deployed") if pages else cell("missing", "none")
    if s and s["visual"]:
        ratio = s["linked"] / s["visual"]
        st = "ok" if ratio >= 0.8 else "partial" if s["linked"] else "missing"
        c["linked"] = cell(st, f"{s['linked']}/{s['visual']}")
    else:
        c["linked"] = cell("na", "—")
    if s and s["spots"]:
        st = "ok" if s["published"] == s["spots"] else "partial"
        c["videos"] = cell(st, f"{s['published']}/{s['spots']}")
    else:
        c["videos"] = cell("missing", "none")
    if diags and diag_ci:
        c["diagrams"] = cell("ok", f"CI · {len(diags)}")
    elif diags:
        c["diagrams"] = cell("partial", f"static · {len(diags)}")
    else:
        c["diagrams"] = cell("missing", "none")
    c["brand"] = cell("ok", "set") if s.get("brand") else cell("missing", "none")
    c["reels"] = cell("ok", str(s["reels"])) if s.get("reels") else cell("missing", "none")
    c["journeys"] = cell("ok", "nightly") if journeys else cell("missing", "none")
    c["vertical"] = cell("ok", str(s["vertical"])) if s.get("vertical") else cell("missing", "none")

    scored = [v for v in c.values() if v["status"] != "na"]
    score = round(100 * sum(1 if v["status"] == "ok" else 0.5 if v["status"] == "partial" else 0 for v in scored) / len(scored))
    nxt = next((k for k, _ in COLUMNS if c[k]["status"] in ("missing", "partial")), None)
    return {"repo": repo["repo"], "full_name": repo["full_name"], "tier": sotu.tier_of(repo["repo"]),
            "path": p, "found": found, "score": score, "cells": c,
            "next": {"column": nxt, "hint": fix_hint(nxt, repo)} if nxt else None}


def build(fetch: bool) -> dict:
    rows = [scan(r, fetch) for r in sotu.tracked_repos() if not r["private"]]
    order = {"I": 0, "II": 1, "III": 2}
    rows.sort(key=lambda r: (order.get(r["tier"], 3), -r["score"], r["repo"]))
    # Today's pick: the first gap in the highest tier, in column order, so fixes walk the board predictably.
    pick = None
    for col, _ in COLUMNS:
        for r in rows:
            if r["tier"] == "I" and r["cells"][col]["status"] in ("missing", "partial"):
                pick = {"repo": r["repo"], "column": col, "hint": fix_hint(col, r)}
                break
        if pick:
            break
    if not pick:
        pick = next(({"repo": r["repo"], **r["next"]} for r in rows if r["next"]), None)
    totals = {k: sum(1 for r in rows if r["cells"][k]["status"] == "ok") for k, _ in COLUMNS}
    return {"generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
            "columns": [{"key": k, "label": label} for k, label in COLUMNS],
            "rows": rows, "pick": pick, "totals": totals,
            "portfolio_score": round(sum(r["score"] for r in rows) / len(rows)) if rows else 0}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args()
    data = build(not a.no_fetch)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    missing = [r["repo"] for r in data["rows"] if not r["found"]]
    print(f"visual-board: {len(data['rows'])} repos, portfolio {data['portfolio_score']}%, "
          f"pick {(data['pick'] or {}).get('repo','-')}/{(data['pick'] or {}).get('column','-')} -> {out}"
          + (f"; no clone/ref for {', '.join(missing)}" if missing else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
