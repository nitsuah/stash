// Zero-dependency uptime check with Discord/Slack-compatible webhook alerts. Node 18+.
// node monitor.mjs [--dry]   (run from cron or a scheduled task; --dry prints instead of posting)
import { readFileSync } from "node:fs";
const cfg = JSON.parse(readFileSync(new URL("./targets.json", import.meta.url), "utf8"));
const dry = process.argv.includes("--dry");
const bad = [];
for (const url of cfg.urls) {
  const t0 = Date.now();
  try {
    const r = await fetch(url, { method: "GET", redirect: "follow", signal: AbortSignal.timeout(cfg.timeout_ms ?? 8000) });
    console.log(url, r.status, Date.now() - t0 + "ms");
    if (r.status >= 400) bad.push(`${url} returned ${r.status}`);
  } catch (e) {
    console.log(url, "ERROR", e.name);
    bad.push(`${url} unreachable (${e.name})`);
  }
}
if (bad.length) {
  const text = "Uptime alert:\n" + bad.join("\n");
  if (dry) console.log("[dry] would post:", text);
  else await fetch(cfg.webhook, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ content: text, text }) });
}
process.exit(bad.length ? 1 : 0);
