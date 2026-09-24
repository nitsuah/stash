#!/usr/bin/env bash
set -euo pipefail

# Blocks personal data and credentials from landing in this PUBLIC repo.
#
# By default scans every folder that routines publish to automatically:
# agent/reports/ (incl. agent/reports/cloud/), Daily Notes/, Weekly Notes/.
# Fails on:
#   - email addresses (each address is checked on its own; noreply/bot and
#     example.* addresses are allowed)
#   - North American phone numbers
#   - common credential formats (GitHub, Anthropic, OpenAI incl. sk-proj-,
#     AWS, Slack, Google, PEM private keys)
# Output is location-only (file:line + category), never the matched text, so
# CI logs don't become a second copy of whatever leaked.
#
# Runs in CI inside "Install & syntax check", so a leaky report can't auto-merge.
# Usage: agent/scripts/pii-scan.sh [path ...]

if [ "$#" -gt 0 ]; then
  paths=("$@")
else
  paths=("agent/reports" "Daily Notes" "Weekly Notes")
fi

existing=()
for p in "${paths[@]}"; do
  if [ -e "$p" ]; then existing+=("$p"); fi
done
if [ "${#existing[@]}" -eq 0 ]; then
  echo "pii-scan: nothing to scan (${paths[*]} not present)."
  exit 0
fi

email='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
email_ok='^(noreply@|no-reply@|.*@users\.noreply\.github\.com$|.*@example\.(com|org|net)$)'
phone='(^|[^0-9])(\+?1[ .-]?)?\(?[2-9][0-9]{2}\)?[ .-][0-9]{3}[ .-][0-9]{4}([^0-9]|$)'
secret='(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|gh[osu]_[A-Za-z0-9]{30,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|xox[abpr]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'

# Scan file by file so paths (which may contain ':' or spaces) never have to be
# parsed back out of grep output. grep -no prints "line:match" per match.
# $2 is an optional allowlist regex applied to each individual match.
scan() {
  local pattern="$1" allow="${2:-}" file line match
  while IFS= read -r -d '' file; do
    grep -noE "$pattern" "$file" | while IFS= read -r row; do
      line="${row%%:*}"
      match="${row#*:}"
      if [ -n "$allow" ] && printf '%s\n' "$match" | grep -qiE "$allow"; then continue; fi
      printf '%s:%s\n' "$file" "$line"
    done || true
  done < <(find "${existing[@]}" -type f -print0) | sort -u
}

# Emails are classified one address at a time, so an allowed bot address on
# the same line can't hide a personal one.
email_hits="$(scan "$email" "$email_ok")"
phone_hits="$(scan "$phone")"
secret_hits="$(scan "$secret")"

fail=0
report() {
  local label="$1" hits="$2"
  if [ -z "$hits" ]; then return 0; fi
  echo "::error::pii-scan found possible $label at:"
  printf '%s\n' "$hits" | sed 's/^/  /'
  fail=1
}
report "email addresses" "$email_hits"
report "phone numbers" "$phone_hits"
report "credentials" "$secret_hits"

if [ "$fail" -ne 0 ]; then
  echo "pii-scan: remove or generalize those lines (content not printed on purpose). This repo is PUBLIC."
  exit 1
fi
echo "pii-scan: clean (${existing[*]})."
