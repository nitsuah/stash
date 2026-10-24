// Zero-LLM uptime + broken-link checker. Usage: node monitor.mjs <url> [<url>...]
// Prints JSON: per-URL status/latency, plus internal links on the page that return >=400.
const urls = process.argv.slice(2);
const timeout = ms => AbortSignal.timeout(ms);
async function check(url, method = 'GET') {
  const t0 = Date.now();
  try {
    const r = await fetch(url, { method, redirect: 'follow', signal: timeout(15000), headers: { 'user-agent': 'mm-monitor/0.1' } });
    return { url, status: r.status, ok: r.ok, ms: Date.now() - t0, html: method === 'GET' ? await r.text() : null };
  } catch (e) { return { url, status: null, ok: false, ms: Date.now() - t0, error: String(e.cause?.code || e.message), html: null }; }
}
const out = [];
for (const url of urls) {
  const res = await check(url);
  const broken = [];
  if (res.html) {
    const base = new URL(url);
    const links = [...new Set([...res.html.matchAll(/href=["']([^"'#]+)["']/gi)].map(m => { try { return new URL(m[1], base).href; } catch { return null; } })
      .filter(h => h && h.startsWith(base.origin)))].slice(0, 25);
    for (const l of links) { const c = await check(l, 'HEAD'); if (!c.ok) broken.push({ url: l, status: c.status, error: c.error }); }
  }
  const { html, ...rest } = res;
  out.push({ ...rest, checked_at: new Date().toISOString(), broken_links: broken });
}
console.log(JSON.stringify(out, null, 2));
