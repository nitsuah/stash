#!/usr/bin/env bash
# Run inside the Playwright container: serve sample-site, scan it, and always stop the server.
set -euo pipefail
cd "$(dirname "$0")"
npm install --no-audit --no-fund --silent
node serve.cjs &
server_pid=$!
cleanup() {
  kill "$server_pid" 2>/dev/null || true
  wait "$server_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Wait for the server to become ready rather than scanning an old process or racing startup.
node --input-type=module -e '
const url = "http://127.0.0.1:8080/";
for (let i = 0; i < 50; i++) {
  try { const r = await fetch(url); if (r.ok) process.exit(0); } catch {}
  await new Promise(resolve => setTimeout(resolve, 100));
}
console.error("Sample server did not become ready");
process.exit(1);
'
node scan.mjs http://127.0.0.1:8080 /,/menu.html sample-bakery
