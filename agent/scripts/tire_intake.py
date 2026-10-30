#!/usr/bin/env python3
"""TIRE section 2 (findings intake) without a model.

Reads the findings ledger, ingests the `## For TIRE` lines of open `bot:repo-health` issues (one
`gh issue list` per tracked repo), dedups by repo + target + problem, re-verifies advisory bumps
against the repo's lockfile on its default branch, and writes `agent/reports/tire-input.json`
holding only NEW or CHANGED items plus `skip_model` (true when none of them is a `quick` item
and nothing failed to load).

The ledger is edited only with --apply: matched rows get `Seen`/`Last seen` bumped, verified-fixed
rows are marked `done` with the evidence, new items are appended. With --apply and skip_model, a
stub `tire-kick-<date>.md` is written too, so the report cadence check stays green. The default
is a dry run that prints a summary. stash is PUBLIC: counts, repo names, packages and advisory IDs.

Usage:
  python agent/scripts/tire_intake.py [--apply] [--no-verify] [--today YYYY-MM-DD] [--ledger PATH]
Run it from the stash worktree that will carry the ledger PR (the ledger path is relative to
this file). Prose sources (metrics, pmo-audit, routine-run-findings, cloud, daily notes) cannot be
parsed mechanically; they are only listed in `prose_sources`.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import re
import sys
from collections.abc import Callable
from pathlib import Path

import prestep_common as pc

OUT = pc.REPORTS / "tire-input.json"
CLASSES = {"quick", "pmo", "human", "routine"}
CLOSED = {"done", "wontfix"}
BUMP_RE = re.compile(r"^bump\s+(\S+)\s+(\S+?)\s*(?:->|→)\s*(\S+?)(?:\s*\(([^)]*)\))?\s*$", re.I)
LOCKFILES = ("package-lock.json", "requirements.txt", "poetry.lock", "uv.lock")
MAX_LOCKFILES = 8

# checker(repo_row, pkg, from_ver, to_ver) -> (verdict, evidence); verdict: fixed|vulnerable|unknown
Checker = Callable[[dict, str, str, str], tuple[str, str]]


def parse_for_tire(body: str) -> list[dict]:
    """Lines of the `## For TIRE` section: `class | repo | finding | peer-dep risk: note`."""
    out, inside = [], False
    for line in (body or "").splitlines():
        if line.startswith("## "):
            inside = line.strip().lower() == "## for tire"
            continue
        if not inside or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3 or parts[0].lower() not in CLASSES:
            continue
        note = " | ".join(parts[3:])
        item = {"class": parts[0].lower(), "repo": parts[1], "finding": parts[2],
                "peer_dep_risk": re.sub(r"^peer-dep risk:\s*", "", note, flags=re.I) or "unknown"}
        m = BUMP_RE.match(parts[2])
        if m:
            item.update(pkg=m.group(1), frm=m.group(2), to=m.group(3),
                        advisories=[a.strip() for a in (m.group(4) or "").split(",") if a.strip()])
        out.append(item)
    return out


def group_items(lines: list[dict]) -> list[dict]:
    """Merge bump lines for the same repo + package + target version (one row, many advisories)."""
    grouped: dict[tuple, dict] = {}
    for it in lines:
        key = (it["repo"], it["pkg"], it["to"]) if "pkg" in it else (it["repo"], it["finding"])
        if key in grouped:
            cur = grouped[key]
            for adv in it.get("advisories", []):
                if adv not in cur["advisories"]:
                    cur["advisories"].append(adv)
            continue
        grouped[key] = dict(it)
    items = list(grouped.values())
    for it in items:
        if "pkg" in it:
            adv = f" ({', '.join(it['advisories'])})" if it["advisories"] else ""
            it["finding"] = f"Bump {it['pkg']} {it['frm']} -> {it['to']}{adv}"
    return sorted(items, key=lambda i: (i["repo"], i.get("pkg", ""), i["finding"]))


def row_has_repo(row: dict, repo: str) -> bool:
    return repo in [r.strip() for r in row["Repo"].split(",")]


def word_in(word: str, text: str) -> bool:
    return re.search(rf"(?<![\w@/.-]){re.escape(word)}(?![\w.-])", text, re.I) is not None


def match_row(item: dict, rows: list[dict]) -> tuple[dict | None, str]:
    """Return (row, kind): kind is 'open', 'closed' or '' when nothing matches."""
    mine = [r for r in rows if row_has_repo(r, item["repo"])]
    if "pkg" in item:
        hits = [r for r in mine if word_in(item["pkg"], r["Finding"])
                and re.search(r"\b(bump|raise|update|upgrade)\b", r["Finding"], re.I)]
    else:
        hits = [r for r in mine if item["finding"].lower() in r["Finding"].lower()]
    open_hits = [r for r in hits if r["Status"] not in CLOSED]
    if open_hits:
        return open_hits[0], "open"
    advs = item.get("advisories", [])
    for r in hits:
        if "pkg" not in item or not advs or any(a in r["Finding"] for a in advs):
            return r, "closed"
    return None, ""


def changed_reason(item: dict, row: dict) -> str:
    """Why a matched open row needs fresh attention: a new advisory or a new target version."""
    if "pkg" not in item:
        return ""
    text = row["Finding"]
    new_adv = [a for a in item["advisories"] if a not in text]
    bits = []
    if new_adv:
        bits.append(f"new advisory {', '.join(new_adv)}")
    if item["to"].lstrip("^~") not in text:
        bits.append(f"target now {item['to']}")
    return "; ".join(bits)


# ---- lockfile verification -------------------------------------------------------------------

def vkey(version: str) -> tuple[int, ...]:
    head = re.split(r"[-+]", version.lstrip("^~=v "), maxsplit=1)[0]
    return tuple(int(n) for n in re.findall(r"\d+", head)[:4])


def norm_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def lockfile_versions(name: str, text: str, pkg: str) -> list[str]:
    """Every version of `pkg` pinned in one lockfile's text (empty if absent or unparseable)."""
    base = name.rsplit("/", 1)[-1]
    found: list[str] = []
    if base == "package-lock.json":
        try:
            pkgs = json.loads(text).get("packages", {})
        except (json.JSONDecodeError, AttributeError):
            return []
        for path, meta in pkgs.items():
            is_pkg = path == f"node_modules/{pkg}" or path.endswith(f"/node_modules/{pkg}")
            if is_pkg and isinstance(meta, dict) and meta.get("version"):
                found.append(meta["version"])
    elif base.startswith("requirements"):
        for line in text.splitlines():
            m = re.match(r"\s*([A-Za-z0-9_.-]+)(?:\[[^\]]*\])?\s*==\s*([\w.+!-]+)", line)
            if m and norm_name(m.group(1)) == norm_name(pkg):
                found.append(m.group(2))
    elif base in ("poetry.lock", "uv.lock"):
        for m in re.finditer(r'name = "([^"]+)"\s*\nversion = "([^"]+)"', text):
            if norm_name(m.group(1)) == norm_name(pkg):
                found.append(m.group(2))
    return found


def verdict_for(versions: list[str], to_ver: str) -> tuple[str, str]:
    """fixed only when every pinned copy is at or above the target; any older copy is vulnerable."""
    if not versions:
        return "unknown", "package not found in a lockfile on the default branch"
    low = sorted(versions, key=vkey)[0]
    if vkey(low) < vkey(to_ver):
        return "vulnerable", f"lockfile still pins {low} (target {to_ver})"
    return "fixed", f"lockfile pins {low}, at or above {to_ver}"


class LockfileChecker:
    """Default checker: reads lockfiles via `gh api` on the default branch, cached per repo."""

    def __init__(self) -> None:
        self.cache: dict[str, list[tuple[str, str]] | str] = {}

    def lockfiles(self, repo: dict) -> list[tuple[str, str]] | str:
        full = repo["full_name"]
        if full in self.cache:
            return self.cache[full]
        try:
            branch = pc.default_branch(full)
            tree = pc.gh_json(["api", f"repos/{full}/git/trees/{branch}?recursive=1"])
            paths = [t["path"] for t in tree.get("tree", []) if t.get("type") == "blob"
                     and "node_modules/" not in t["path"]
                     and t["path"].rsplit("/", 1)[-1] in LOCKFILES]
            files = []
            for path in paths[:MAX_LOCKFILES]:
                blob = pc.gh_json(["api", f"repos/{full}/contents/{path}?ref={branch}"])
                files.append((path, base64.b64decode(blob["content"]).decode("utf-8", "replace")))
            result: list[tuple[str, str]] | str = files
        except (pc.GhError, KeyError, ValueError) as exc:
            result = f"lockfile read failed: {exc}"
        self.cache[full] = result
        return result

    def __call__(self, repo: dict, pkg: str, frm: str, to: str) -> tuple[str, str]:
        files = self.lockfiles(repo)
        if isinstance(files, str):
            return "unknown", files
        versions = [v for name, text in files for v in lockfile_versions(name, text, pkg)]
        return verdict_for(versions, to)


# ---- intake ----------------------------------------------------------------------------------

def next_ids(rows: list[dict], today: str) -> Callable[[], str]:
    stamp = today.replace("-", "")
    used = [int(m.group(1)) for r in rows if (m := re.match(rf"F-{stamp}-(\d+)$", r["ID"]))]
    counter = [max(used, default=0)]

    def alloc() -> str:
        counter[0] += 1
        return f"F-{stamp}-{counter[0]:02d}"
    return alloc


def collect_items(repos: list[dict]) -> tuple[list[dict], list[str], dict[str, int]]:
    """For TIRE lines from every repo's open bot:repo-health issues, plus load errors."""
    lines, errors, issues = [], [], {}
    for repo in repos:
        try:
            data = pc.gh_json(["issue", "list", "-R", repo["full_name"], "--label",
                               "bot:repo-health", "--state", "open", "--json", "number,body"])
        except pc.GhError as exc:
            errors.append(f"{repo['repo']}: {exc}")
            continue
        issues[repo["repo"]] = len(data)
        for issue in data:
            lines.extend(parse_for_tire(issue.get("body", "")))
    return group_items(lines), errors, issues


def prose_sources(last_intake: str | None, today: str) -> list[str]:
    """Report files after `Last intake` that need a model to read (not parsed by this script)."""
    cutoff = last_intake or (dt.date.fromisoformat(today) - dt.timedelta(days=35)).isoformat()
    found: list[Path] = []
    for pat in ("metrics-*.md", "pmo-audit-*.md", "routine-run-findings-*.md"):
        found += pc.REPORTS.glob(pat)
    cloud = pc.REPORTS / "cloud"
    if cloud.is_dir():
        found += [p for p in cloud.rglob("*.md") if "daily-brief" not in p.parts]
    out = []
    for p in sorted(found):
        m = re.search(r"(\d{4}-\d{2}-\d{2})", p.name)
        if m and m.group(1) > cutoff:
            out.append(str(p.relative_to(pc.VAULT)).replace("\\", "/"))
    notes = pc.VAULT / "notes"
    for p in sorted(notes.glob("????-??-??.md")) if notes.is_dir() else []:
        if p.stem > cutoff and re.search(r"^## Notes\s*\n+\s*\S", p.read_text("utf-8"), re.M):
            out.append(f"notes/{p.name}")
    return out


def intake(rows: list[dict], items: list[dict], repos: list[dict], today: str,
           checker: Checker | None) -> dict:
    """Classify each item as new/changed/deduped/fixed. Pure: touches no files."""
    by_name = {r["repo"]: r for r in repos}
    alloc = next_ids(rows, today)
    res: dict = {"items": [], "touch": [], "fixed": [], "new_rows": [], "deduped": 0,
                 "recurred_unverified": []}
    for item in items:
        row, kind = match_row(item, rows)
        verdict, evidence = "skipped", ""
        if checker and "pkg" in item and item["repo"] in by_name:
            verdict, evidence = checker(by_name[item["repo"]], item["pkg"], item["frm"], item["to"])
        if verdict == "fixed":
            if row and kind == "open":
                res["fixed"].append({"id": row["ID"], "evidence": evidence})
            elif not row:
                new_id = alloc()
                res["fixed"].append({"id": new_id, "evidence": evidence})
                res["new_rows"].append({"id": new_id, "item": item, "status": "done",
                                        "link": f"Verified {today}: {evidence}"})
            continue
        if row and kind == "closed":
            if verdict == "skipped":
                # Reported again after a `done` row and not re-checked: count it, don't reopen.
                res["recurred_unverified"].append(row["ID"])
                continue
            row = None  # verified still vulnerable: a regression, so it is a new item
        out = {k: item[k] for k in ("class", "repo", "finding", "peer_dep_risk")}
        for k in ("pkg", "frm", "to", "advisories"):
            if k in item:
                out[k] = item[k]
        if verdict != "skipped":
            out["verify"] = {"verdict": verdict, "evidence": evidence}
        if row:
            why = changed_reason(item, row)
            res["touch"].append({"id": row["ID"], "update": why})
            if not why:
                res["deduped"] += 1
                continue
            out.update(status="changed", ledger_id=row["ID"], reason=why)
        else:
            new_id = alloc()
            out.update(status="new", ledger_id=new_id)
            res["new_rows"].append({"id": new_id, "item": item, "status": "open", "link": ""})
        res["items"].append(out)
    return res


def parse_last_intake(text: str) -> str | None:
    m = re.search(r"^Last intake:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    return m.group(1) if m else None


def esc(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def apply_ledger(text: str, rows: list[dict], res: dict, today: str, set_intake: bool) -> str:
    """Return the ledger text with the intake result applied."""
    lines = text.splitlines()
    by_id = {r["ID"]: r for r in rows}

    def rewrite(row: dict) -> None:
        lines[row["_line"]] = "| " + " | ".join(row[c] for c in pc.LEDGER_COLS) + " |"

    for t in res["touch"]:
        row = by_id[t["id"]]
        if row["Last seen"] != today:
            row["Seen"] = str(int(row["Seen"] or 0) + 1)
            row["Last seen"] = today
        if t["update"] and t["update"] not in row["Finding"]:
            row["Finding"] += esc(f"; {today}: {t['update']}")
        rewrite(row)
    for f in res["fixed"]:
        row = by_id.get(f["id"])
        if row and row["Status"] not in CLOSED:
            row["Status"] = "done"
            row["Link"] = esc(f"Verified {today}: {f['evidence']}")
            row["Last seen"] = today
            rewrite(row)
    table_end = max((r["_line"] for r in rows), default=None)
    if table_end is None:
        table_end = next((i for i, ln in enumerate(lines) if ln.startswith("|---")), len(lines) - 1)
    adds = []
    for n in res["new_rows"]:
        it = n["item"]
        cells = [n["id"], today, today, "1", "repo-health", it["repo"], esc(it["finding"]),
                 it["class"], n["status"], esc(n["link"])]
        adds.append("| " + " | ".join(cells) + " |")
    lines[table_end + 1:table_end + 1] = adds
    out = "\n".join(lines) + "\n"
    if set_intake:
        out = re.sub(r"^Last intake:.*$", f"Last intake: {today} (TIRE)", out, count=1,
                     flags=re.M)
    return out


def stub_report(today: str, res: dict, issues: int, prose: int) -> str:
    return (
        f"---\nkind: tire-kick\ndate: {today}\n---\n\n# Tire Kick {today}\n\n"
        "Script-only run (`tire_intake.py --apply`, `skip_model: true`): no new or changed "
        "`quick` items, so no model pass, no fix PRs and no Docker sweep.\n\n## Intake\n\n"
        f"- **Sources:** {issues} open `bot:repo-health` issues across tracked repos.\n"
        f"- **New / changed:** {len(res['items'])}. **Deduplicated:** {res['deduped']}. "
        f"**Already fixed (verified):** {len(res['fixed'])}.\n"
        f"- **Prose sources not read:** {prose} (the ledger's `Last intake` date was "
        f"{'left unchanged' if prose else 'advanced'}).\n")


def main(argv: list[str] | None = None, checker: Checker | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="edit the ledger (default: dry run)")
    ap.add_argument("--no-verify", action="store_true", help="skip the lockfile network checks")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--ledger", default=str(pc.LEDGER))
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)

    ledger = Path(a.ledger)
    text = ledger.read_text("utf-8") if ledger.exists() else ""
    rows = pc.parse_ledger(text)
    repos = pc.tracked_repos()
    items, errors, issues = collect_items(repos)
    if a.no_verify:
        checker = None
    elif checker is None:
        checker = LockfileChecker()
    res = intake(rows, items, repos, a.today, checker)
    prose = prose_sources(parse_last_intake(text), a.today)
    quick = [i for i in res["items"] if i["class"] == "quick"]
    skip = not quick and not errors
    open_issues = sum(issues.values())
    counts = {"new": sum(i["status"] == "new" for i in res["items"]),
              "changed": sum(i["status"] == "changed" for i in res["items"]),
              "quick": len(quick), "deduped": res["deduped"],
              "already_fixed": len(res["fixed"]),
              "recurred_unverified": len(res["recurred_unverified"]),
              "open_issues": open_issues, "load_errors": len(errors)}
    data = {"generated": a.today, "applied": a.apply, "verified": not a.no_verify,
            "skip_model": skip, "counts": counts, "load_errors": errors,
            "prose_sources": prose, "items": res["items"]}
    pc.write_json(Path(a.out), data)
    print(f"tire_intake {'APPLY' if a.apply else 'dry run'}: "
          + " ".join(f"{k}={v}" for k, v in counts.items())
          + f" prose_sources={len(prose)} skip_model={str(skip).lower()}")
    if a.apply:
        # Last intake moves only when no prose source is waiting for a model to read it.
        ledger.write_text(apply_ledger(text, rows, res, a.today, not prose), encoding="utf-8")
        stub = pc.REPORTS / f"tire-kick-{a.today}.md"
        if skip and not stub.exists() and ledger.parent == pc.REPORTS:
            stub.write_text(stub_report(a.today, res, open_issues, len(prose)), encoding="utf-8")
        print(f"ledger updated: {ledger.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
