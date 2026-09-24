#!/usr/bin/env bash
# Blocks personal data and credentials from landing in this PUBLIC repo.
#
# Scans the report folders that cloud routines publish to automatically
# (agent/reports/cloud/ by default). Fails with file:line matches for:
#   - email addresses (except noreply/bot and example.* addresses)
#   - North American phone numbers
#   - common credential formats (GitHub, Anthropic, OpenAI, AWS, Slack, Google, private keys)
# Run in CI inside "Install & syntax check", so a report that trips it can't auto-merge.
#
# Usage: agent/scripts/pii-scan.sh [path ...]
set -uo pipefail

paths=("$@")
[ ${#paths[@]} -eq 0 ] && paths=(agent/reports/cloud)

existing=()
for p in "${paths[@]}"; do [ -e "$p" ] && existing+=("$p"); done
if [ ${#existing[@]} -eq 0 ]; then
  echo "pii-scan: nothing to scan (${paths[*]} not present)."
  exit 0
fi

email='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
email_ok='(noreply@|no-reply@|@users\.noreply\.github\.com|@example\.(com|org|net))'
phone='(^|[^0-9])(\+?1[ .-]?)?\(?[2-9][0-9]{2}\)?[ .-][0-9]{3}[ .-][0-9]{4}([^0-9]|$)'
secret='(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|gh[osu]_[A-Za-z0-9]{30,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|xox[abpr]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'

fail=0
report() {
  local label="$1" hits="$2"
  [ -z "$hits" ] && return
  echo "::error::pii-scan found possible $label:"
  echo "$hits" | sed 's/^/  /'
  fail=1
}

report "email addresses" "$(grep -rInE "$email" "${existing[@]}" | grep -vE "$email_ok" || true)"
report "phone numbers" "$(grep -rInE "$phone" "${existing[@]}" || true)"
report "credentials" "$(grep -rInE "$secret" "${existing[@]}" || true)"

if [ "$fail" -ne 0 ]; then
  echo "pii-scan: remove or generalize the lines above. This repo is PUBLIC."
  exit 1
fi
echo "pii-scan: clean (${existing[*]})."
