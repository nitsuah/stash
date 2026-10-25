// Zero-LLM uptime + broken-link checker. Usage: node monitor.mjs <url> [<url>...]
// Prints JSON: per-URL status/latency, plus internal links on the page that return >=400.
const urls = process.argv.slice(2);
const timeout = ms => AbortSignal.timeout(ms);

async function check(url, method = 'GET', includeBody = false) {
  const t0 = Date.now();
  try {
    const r = await fetch(url, {
      method,
      redirect: 'follow',
      signal: timeout(15000),
      headers: { 'user-agent': 'mm-monitor/0.1' }
    });
    // Discard response bodies for status-only checks.
    if (!includeBody) {
      try { await r.body?.cancel(); } catch {}
    }
    return {
      url,
      finalUrl: r.url || url,
      status: r.status,
      ok: r.ok,
      ms: Date.now() - t0,
      html: includeBody ? await r.text() : null
    };
  } catch (e) {
    return { url, finalUrl: url, status: null, ok: false, ms: Date.now() - t0, error: String(e.cause?.code || e.message), html: null };
  }
}

const out = [];
for (const url of urls) {
  const res = await check(url, 'GET', true);
  const broken = [];
  if (res.html && res.ok) {
    let base;
    try { base = new URL(res.finalUrl); } catch { base = null; }
    if (base && ['http:', 'https:'].includes(base.protocol)) {
      const links = [...new Set([...res.html.matchAll(/href=["']([^"']+)["']/gi)]
        .map(m => {
          const raw = m[1].trim();
          if (!raw || raw.startsWith('#')) return null;
          try {
            const parsed = new URL(raw, base);
            if (!['http:', 'https:'].includes(parsed.protocol) || parsed.origin !== base.origin) return null;
            return parsed.href;
          } catch { return null; }
        })
        .filter(Boolean))];
      const concurrency = 5;
      for (let i = 0; i < links.length; i += concurrency) {
        const batch = await Promise.all(links.slice(i, i + concurrency).map(async link => {
          let result = await check(link, 'HEAD');
          if (result.status === 405 || result.status === 501) {
            result = await check(link, 'GET');
          }
          return result;
        }));
        for (const c of batch) if (!c.ok) broken.push({ url: c.url, status: c.status, error: c.error });
      }
    }
  }
  const { html, finalUrl, ...rest } = res;
  out.push({ ...rest, final_url: finalUrl, checked_at: new Date().toISOString(), broken_links: broken });
}
console.log(JSON.stringify(out, null, 2));
