#!/usr/bin/env python3
"""
Lines of Code analysis script for eng-loc skill
Walks all repos in scope.md, counts lines per file, flags large/small files
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

CONFIG_PATH = "config/eng-loc.toml"
SCOPE_PATH = "stash/agent/projects/scope.md"
REPORTS_DIR = "stash/agent/reports"
LOGS_DIR = "stash/agent/logs"

DEFAULT_MAX_LINES = 500
DEFAULT_MIN_LINES = 30
DEFAULT_EXTENSIONS = [
    ".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".cs", ".java",
    ".rb", ".php", ".swift", ".kt", ".scala", ".cpp", ".cc", ".c",
    ".h", ".hpp", ".vue", ".svelte"
]

EXCLUDE_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".turbo",
    "coverage", ".pnpm-store", "vendor", "target", "bin", "obj",
    ".gradle", "out", ".claude"
}


def parse_toml_config(path):
    """Simple TOML parser for our config"""
    config = {
        "max_lines": DEFAULT_MAX_LINES,
        "min_lines": DEFAULT_MIN_LINES,
        "extensions": DEFAULT_EXTENSIONS,
        "repo_overrides": {}
    }
    current_section = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[repo.") and line.endswith("]"):
                current_section = line[6:-1]
                config["repo_overrides"][current_section] = {}
            elif "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"\' ')
                if val.isdigit():
                    val = int(val)
                elif val.startswith("[") and val.endswith("]"):
                    val = [v.strip().strip('"\' ') for v in val[1:-1].split(",")]
                if current_section:
                    config["repo_overrides"][current_section][key] = val
                else:
                    config[key] = val
    return config


def parse_scope(path):
    """Parse scope.md for repo list"""
    repos = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            m = re.match(r"-\s*\[(.+?)\]\(https://github\.com/nitsuah/(.+?)\)", line)
            if m:
                repos.append({"name": m.group(1), "slug": m.group(2)})
    return repos


def count_lines(filepath):
    """Count lines in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def scan_large_file(filepath, ext):
    """Secondary scan for large files"""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return findings

    lines = content.split('\n')

    # Check for unused imports (JS/TS)
    if ext in (".ts", ".tsx", ".js", ".jsx"):
        import_pattern = re.compile(r'^import\s+.*\s+from\s+["\']|^import\s+["\']')
        for line in lines:
            if import_pattern.match(line.strip()):
                # Extract imported names from { ... }
                m = re.search(r'import\s+\{([^}]+)\}', line)
                if m:
                    names = [n.strip() for n in m.group(1).split(',')]
                    for name in names:
                        if name and not re.search(rf'(?<![a-zA-Z0-9_]){re.escape(name)}(?![a-zA-Z0-9_])', content):
                            findings.append(f"Unused import (heuristic): {name}")

    # Check for functions defined but not referenced
    if ext in (".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs"):
        funcs = []
        if ext == ".py":
            funcs = re.findall(r'^\s*def\s+(\w+)', content, re.MULTILINE)
        elif ext == ".go":
            funcs = re.findall(r'^\s*func\s+(\w+)', content, re.MULTILINE)
        elif ext == ".rs":
            funcs = re.findall(r'^\s*fn\s+(\w+)', content, re.MULTILINE)
        else:
            # JS/TS - simplified
            funcs = re.findall(
                r'^\s*(?:async\s+)?function\s+(\w+)|^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(|^\s*(\w+)\s*\([^)]*\)\s*=>|^\s*(\w+)\s*\([^)]*\)\s*\{',
                content, re.MULTILINE
            )
            funcs = [f for g in funcs for f in g if f]

        for fn in funcs:
            if fn and fn not in ("main", "init", "test", "Test"):
                # Count references (rough heuristic)
                refs = len(re.findall(rf'(?<![a-zA-Z0-9_]){re.escape(fn)}(?![a-zA-Z0-9_])', content))
                if refs <= 1:
                    findings.append(f"Unused function (heuristic): {fn}")

    # Check for copy-paste blocks (>10 lines repeated)
    if len(lines) > 20:
        for i in range(len(lines) - 9):
            block = '\n'.join(lines[i:i+10])
            if len(block.strip()) > 50:
                count = content.count(block)
                if count > 1:
                    findings.append(f"Repeated block ({count} occurrences, 10+ lines): {block[:80]}...")
                    break

    return findings


def main():
    config = parse_toml_config(CONFIG_PATH)
    repos = parse_scope(SCOPE_PATH)

    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)
    Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = Path(LOGS_DIR) / "eng-loc.log"
    log_lines = [f"=== ENG LOC Run: {date_str} ==="]

    all_large = []
    all_small = []

    for repo in repos:
        repo_path = Path(repo["slug"])
        if not repo_path.exists():
            log_lines.append(f"SKIP: {repo_path} does not exist locally")
            continue

        log_lines.append(f"Processing: {repo['name']} ({repo_path})")

        max_lines = config["max_lines"]
        if repo["slug"] in config["repo_overrides"] and "max_lines" in config["repo_overrides"][repo["slug"]]:
            max_lines = config["repo_overrides"][repo["slug"]]["max_lines"]
        min_lines = config["min_lines"]
        extensions = config["extensions"]

        large_files = []
        small_files = []

        for root, dirs, files in os.walk(repo_path, topdown=True):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for filename in files:
                filepath = Path(root) / filename
                if filepath.suffix not in extensions:
                    continue

                try:
                    line_count = count_lines(filepath)
                except (OSError, PermissionError):
                    continue

                rel_path = filepath.relative_to(repo_path).as_posix()

                if line_count >= max_lines:
                    findings = scan_large_file(filepath, filepath.suffix)
                    large_files.append({
                        "lines": line_count,
                        "path": rel_path,
                        "findings": findings
                    })
                    all_large.append({
                        "repo": repo["name"],
                        "slug": repo["slug"],
                        "lines": line_count,
                        "path": rel_path,
                        "findings": findings
                    })
                elif 0 < line_count <= min_lines:
                    small_files.append({
                        "lines": line_count,
                        "path": rel_path
                    })
                    all_small.append({
                        "repo": repo["name"],
                        "slug": repo["slug"],
                        "lines": line_count,
                        "path": rel_path
                    })

        large_files.sort(key=lambda x: -x["lines"])
        small_files.sort(key=lambda x: x["lines"])

        # Write per-repo report
        report_path = Path(REPORTS_DIR) / f"eng-loc-{repo['slug']}-{date_str}.md"
        report = [
            f"# ENG LOC Report: {repo['name']}",
            f"**Date:** {date_str}",
            f"**Repo:** {repo['name']} ({repo_path})",
            f"**Thresholds:** max_lines={max_lines}, min_lines={min_lines}",
            "",
            "## Large Files (> {max_lines} lines) — Refactor Candidates",
            ""
        ]

        if large_files:
            report.append("| Lines | Path | Secondary Findings |")
            report.append("|-------|------|---------------------|")
            for lf in large_files:
                findings_str = "; ".join(lf["findings"]) if lf["findings"] else "—"
                findings_str = findings_str.replace("|", "\\|")
                report.append(f"| {lf['lines']} | `{lf['path']}` | {findings_str} |")
        else:
            report.append("_None_")

        report.extend(["", f"## Small Files (<= {min_lines} lines) — Merge Candidates", ""])

        if small_files:
            report.append("| Lines | Path | Suggested Merge Target |")
            report.append("|-------|------|------------------------|")
            for sf in small_files:
                dir_path = os.path.dirname(sf["path"])
                siblings = [s for s in small_files if os.path.dirname(s["path"]) == dir_path and s["path"] != sf["path"]]
                target = siblings[0]["path"] if siblings else "—"
                report.append(f"| {sf['lines']} | `{sf['path']}` | {target} |")
        else:
            report.append("_None_")

        report.append("")
        report_path.write_text("\n".join(report), encoding="utf-8")
        log_lines.append(f"  Report: {report_path} (Large: {len(large_files)}, Small: {len(small_files)})")

    # Write summary log
    log_lines.extend([
        "",
        "=== SUMMARY ===",
        f"Total repos processed: {len(repos)}",
        f"Total large files: {len(all_large)}",
        f"Total small files: {len(all_small)}"
    ])

    if all_large:
        log_lines.append("")
        log_lines.append("Largest files across all repos:")
        for lf in sorted(all_large, key=lambda x: -x["lines"])[:20]:
            log_lines.append(f"  {lf['lines']} lines — {lf['slug']}/{lf['path']}")

    log_path.write_text("\n".join(log_lines), encoding="utf-8")

    # Print summary
    for line in log_lines:
        print(line)

    # Output Odysseus notes as JSON
    odysseus_notes = []
    for f in sorted(all_large, key=lambda x: (x["repo"], -x["lines"])):
        note = {
            "title": f"[eng-loc] Refactor: {f['repo']}/{f['path']} ({f['lines']} lines)",
            "tags": ["eng-loc", "refactor"],
            "body": f"File: {f['repo']}/{f['path']}\nLines: {f['lines']}\n\n"
        }
        if f["findings"]:
            note["body"] += "Secondary scan findings:\n"
            for finding in f["findings"]:
                note["body"] += f"- {finding}\n"
            note["body"] += "\n*Findings are heuristics, not ground truth.*"
        odysseus_notes.append(note)

    print("\n--- ODYSSEUS NOTES ---")
    print(json.dumps(odysseus_notes, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())