// Fetch that follows redirects by hand: every hop is re-checked before it is requested.
// A hop is allowed only on http(s), without credentials, and on the same host as the
// original URL (a leading "www." and an http -> https upgrade are tolerated).
const MAX_HOPS = 5;
const bare = h => h.toLowerCase().replace(/^www\\./, '');
const BLOCKED_METADATA_HOSTS = new Set([
  'metadata', 'metadata.google.internal', 'instance-data',
  '169.254.169.254', '169.254.170.2', '100.100.100.200', 'fd00:ec2::254',
  // WHATWG URL serializes IPv4-mapped IPv6 literals in canonical hexadecimal form.
  '::ffff:a9fe:a9fe', '::ffff:a9fe:aa02', '::ffff:6464:64c8',
]);
function isAllowedTarget(url) {
  const host = url.hostname.toLowerCase().replace(/^\\[|\\]$/g, '').replace(/\\.$/, '');
  return ['http:', 'https:'].includes(url.protocol)
    && !url.username && !url.password
    && !BLOCKED_METADATA_HOSTS.has(host);
}

export function hopAllowed(from, to) {
  if (!isAllowedTarget(to)) return false;
  if (from.protocol === 'https:' && to.protocol === 'http:') return false;
  return bare(to.hostname) === bare(from.hostname) && (to.port || '') === (from.port || '');
}

export async function fetchFollow(url, init, fetchImpl = fetch) {
  const origin = new URL(url);
  if (!isAllowedTarget(origin)) throw new Error('url-blocked');
  let current = origin;
  for (let hop = 0; ; hop++) {
    const r = await fetchImpl(current.href, { ...init, redirect: 'manual' });
    const loc = r.status >= 300 && r.status < 400 ? r.headers.get('location') : null;
    if (!loc) return { response: r, finalUrl: current.href };
    try { await r.body?.cancel(); } catch {}
    let next;
    try { next = new URL(loc, current); } catch { throw new Error('bad-redirect'); }
    // Check against the original host, and never step down from https after an upgrade.
    if (!hopAllowed(origin, next) || !hopAllowed(current, next)) throw new Error('redirect-blocked');
    if (hop >= MAX_HOPS) throw new Error('too-many-redirects');
    current = next;
  }
}
