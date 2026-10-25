#!/usr/bin/env python3
"""Verify or refresh the pack-host archive manifest against staged ZIP files.

Default mode checks the manifest against --archive-dir (defaults to site/).
Use --refresh only after the exact release ZIPs have been staged.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
NAME = re.compile(r"^(?P<slug>.+)-(?P<digest>[0-9a-f]{12})\.zip$")


def read_manifest(path):
    rows = []
    seen_slugs = set()
    seen_files = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split()
        if len(fields) != 2:
            raise ValueError(f"{path}:{line_no}: expected exactly <slug> <archive.zip>")
        slug, filename = fields
        if slug in seen_slugs or filename in seen_files:
            raise ValueError(f"{path}:{line_no}: duplicate slug or archive: {slug} {filename}")
        if Path(filename).name != filename or not filename.endswith(".zip"):
            raise ValueError(f"{path}:{line_no}: unsafe archive filename: {filename}")
        seen_slugs.add(slug)
        seen_files.add(filename)
        rows.append((slug, filename))
    return rows


def staged_rows(directory):
    rows = []
    for path in sorted(directory.glob("*.zip")):
        match = NAME.fullmatch(path.name)
        if not match:
            raise ValueError(f"unexpected staged ZIP name (expected <slug>-<12-hex>.zip): {path.name}")
        rows.append((match.group("slug"), path.name))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-dir", type=Path, default=ROOT / "site")
    parser.add_argument("--refresh", action="store_true", help="replace map.txt from staged ZIPs")
    args = parser.parse_args()
    if not args.archive_dir.is_dir():
        raise SystemExit(f"archive directory does not exist: {args.archive_dir}")
    expected = read_manifest(ROOT / "map.txt")
    actual = staged_rows(args.archive_dir)
    if args.refresh:
        if not actual:
            raise SystemExit(f"refusing to empty the manifest: no staged ZIPs found in {args.archive_dir}")
        (ROOT / "map.txt").write_text("".join(f"{slug} {name}\n" for slug, name in actual), encoding="utf-8")
        print(f"refreshed map.txt with {len(actual)} staged archives")
        return
    expected_by_name = {name: slug for slug, name in expected}
    actual_by_name = {name: slug for slug, name in actual}
    missing = sorted(set(expected_by_name) - set(actual_by_name))
    extra = sorted(set(actual_by_name) - set(expected_by_name))
    wrong_slug = sorted(name for name in set(expected_by_name) & set(actual_by_name)
                        if expected_by_name[name] != actual_by_name[name])
    if missing or extra or wrong_slug:
        for name in missing:
            print(f"missing staged archive: {name}", file=sys.stderr)
        for name in extra:
            print(f"unlisted staged archive: {name}", file=sys.stderr)
        for name in wrong_slug:
            print(f"slug mismatch for {name}: manifest={expected_by_name[name]} staged={actual_by_name[name]}", file=sys.stderr)
        raise SystemExit(1)
    print(f"verified {len(actual)} staged archives against map.txt")


if __name__ == "__main__":
    main()
