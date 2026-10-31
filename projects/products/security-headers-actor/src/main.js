// Security headers and TLS check: grades each URL A to F from its HTTP response headers, cookie flags, HTTPS redirect and certificate.
import tls from 'node:tls';
import { Actor, log } from 'apify';
import { hasWeakScriptSources } from './csp.js';
import { tlsTarget } from './tls-target.js';

const clamp = (n, lo, hi) => Math.min(Math.max(Number.isFinite(n) ? n : lo, lo), hi);
const UA = 'Mozilla/5.0 (compatible; SecurityHeadersCheck/1.0; +https://apify.com)';
const MAX_URLS = 200;

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const urls = [...new Set((input.startUrls ?? []).map((u) => (typeof u === 'string' ? u : u.url)).filter((u) => /^https?:\/\//i.test(u ?? '')))].slice(0, MAX_URLS);
const timeoutMs = clamp(input.timeoutSecs ?? 15, 3, 60) * 1000;
if (!urls.length) await Actor.fail('Provide at least one http(s) URL in startUrls.');

// Each finding costs points off 100. Severity weights are deliberately simple and documented in the README.
const WEIGHT = { high: 20, medium: 10, low: 4 };

function checkHeaders(h) {
    const out = [];
    const add = (rule, severity, detail) => out.push({ rule, severity, detail });
    const hsts = h.get('strict-transport-security');
    if (!hsts) add('hsts-missing', 'high', 'No Strict-Transport-Security header');
    else {
        const age = Number((hsts.match(/max-age=(\d+)/i) ?? [])[1] ?? 0);
        if (age < 15552000) add('hsts-short', 'medium', `HSTS max-age is ${age} seconds (recommend at least 15552000)`);
        if (!/includeSubDomains/i.test(hsts)) add('hsts-subdomains', 'low', 'HSTS does not include subdomains');
    }
    const csp = h.get('content-security-policy');
    if (!csp) add('csp-missing', 'high', 'No Content-Security-Policy header');
    else if (hasWeakScriptSources(csp)) add('csp-weak', 'medium', 'CSP allows unsafe-inline, unsafe-eval or a wildcard script source');
    if (!h.get('x-frame-options') && !/frame-ancestors/i.test(csp ?? '')) add('clickjacking', 'medium', 'No X-Frame-Options or CSP frame-ancestors');
    if (!/nosniff/i.test(h.get('x-content-type-options') ?? '')) add('nosniff-missing', 'medium', 'X-Content-Type-Options is not nosniff');
    if (!h.get('referrer-policy')) add('referrer-policy-missing', 'low', 'No Referrer-Policy header');
    if (!h.get('permissions-policy')) add('permissions-policy-missing', 'low', 'No Permissions-Policy header');
    const server = h.get('server') ?? '';
    if (/\d+\.\d+/.test(server)) add('server-version', 'low', `Server header exposes a version: ${server}`);
    if (h.get('x-powered-by')) add('x-powered-by', 'low', `X-Powered-By reveals the stack: ${h.get('x-powered-by')}`);
    return out;
}

function checkCookies(h) {
    const cookies = typeof h.getSetCookie === 'function' ? h.getSetCookie() : [];
    const out = [];
    for (const c of cookies) {
        const name = c.split('=')[0];
        const flags = [];
        if (!/;\s*secure/i.test(c)) flags.push('Secure');
        if (!/;\s*httponly/i.test(c)) flags.push('HttpOnly');
        if (!/;\s*samesite=/i.test(c)) flags.push('SameSite');
        if (flags.length) out.push({ rule: 'cookie-flags', severity: 'medium', detail: `Cookie "${name}" is missing: ${flags.join(', ')}` });
    }
    return { cookies: cookies.length, findings: out };
}

function certInfo(hostname, port = 443) {
    return new Promise((resolve) => {
        const socket = tls.connect({ host: hostname, port, servername: hostname, timeout: timeoutMs, rejectUnauthorized: false }, () => {  // Intentional: we check cert.authorized and authorizationError below to grade TLS/cert issues
            const cert = socket.getPeerCertificate();
            const validTo = cert?.valid_to ? new Date(cert.valid_to) : null;
            resolve({
                protocol: socket.getProtocol(),
                authorized: socket.authorized,
                authorizationError: socket.authorizationError ? String(socket.authorizationError) : null,
                issuer: cert?.issuer?.O ?? cert?.issuer?.CN ?? null,
                validTo: validTo?.toISOString() ?? null,
                daysToExpiry: validTo ? Math.floor((validTo - Date.now()) / 86400000) : null,
            });
            socket.end();
        });
        socket.on('error', (e) => resolve({ error: e.code ?? e.message }));
        socket.on('timeout', () => { socket.destroy(); resolve({ error: 'timeout' }); });
    });
}

async function audit(url) {
    const u = new URL(url);
    const findings = [];
    const row = { url, finalUrl: null, status: null, grade: null, score: null, findings, tls: null, cookies: 0, checkedAt: new Date().toISOString() };
    try {
        const res = await fetch(url, { redirect: 'follow', headers: { 'user-agent': UA }, signal: AbortSignal.timeout(timeoutMs) });
        row.status = res.status;
        row.finalUrl = res.url;
        findings.push(...checkHeaders(res.headers));
        const c = checkCookies(res.headers);
        row.cookies = c.cookies;
        findings.push(...c.findings);
        // We only need status and headers; release the response body/socket promptly.
        await res.body?.cancel().catch(() => {});
    } catch (err) {
        const code = err.cause?.code ?? err.message;
        // A certificate that fails validation is the finding itself, so grade it instead of reporting a fetch error.
        if (u.protocol === 'https:' && /CERT|SELF_SIGNED|UNABLE_TO_VERIFY|ALTNAME|SSL/i.test(String(code))) {
            const target = tlsTarget(u.href);
            row.tls = await certInfo(target.hostname, target.port);
            findings.push({ rule: 'cert-invalid', severity: 'high', detail: `Certificate failed validation: ${code}` });
            row.score = 0;
            row.grade = 'F';
            return row;
        }
        row.error = code;
        return row;
    }
    const finalHost = new URL(row.finalUrl).hostname;
    if (new URL(row.finalUrl).protocol === 'http:') findings.push({ rule: 'no-https', severity: 'high', detail: 'The site is served over plain HTTP' });
    else {
        // Does plain HTTP upgrade to HTTPS?
        try {
            const r = await fetch(`http://${u.host}${u.pathname}`, { redirect: 'manual', headers: { 'user-agent': UA }, signal: AbortSignal.timeout(timeoutMs) });
            const loc = r.headers.get('location') ?? '';
            const upgrades = r.status >= 300 && r.status < 400 && /^https:/i.test(loc);
            await r.body?.cancel().catch(() => {});
            if (!upgrades) findings.push({ rule: 'http-no-redirect', severity: 'medium', detail: 'HTTP does not redirect to HTTPS' });
        } catch { /* port 80 closed is fine */ }
        const target = tlsTarget(row.finalUrl);
        row.tls = await certInfo(target.hostname, target.port);
        if (row.tls.error) findings.push({ rule: 'tls-error', severity: 'high', detail: `TLS connection failed: ${row.tls.error}` });
        else {
            if (!row.tls.authorized) findings.push({ rule: 'cert-invalid', severity: 'high', detail: `Certificate not trusted: ${row.tls.authorizationError}` });
            if (row.tls.daysToExpiry !== null && row.tls.daysToExpiry < 0) findings.push({ rule: 'cert-expired', severity: 'high', detail: 'Certificate has expired' });
            else if (row.tls.daysToExpiry !== null && row.tls.daysToExpiry < 14) findings.push({ rule: 'cert-expiring', severity: 'medium', detail: `Certificate expires in ${row.tls.daysToExpiry} days` });
            if (['TLSv1', 'TLSv1.1'].includes(row.tls.protocol)) findings.push({ rule: 'old-tls', severity: 'high', detail: `Negotiated ${row.tls.protocol}` });
        }
    }
    const penalty = findings.reduce((s, f) => s + WEIGHT[f.severity], 0);
    row.score = Math.max(0, 100 - penalty);
    row.grade = row.score >= 90 ? 'A' : row.score >= 75 ? 'B' : row.score >= 60 ? 'C' : row.score >= 40 ? 'D' : 'F';
    return row;
}

let next = 0;
let audited = 0;
let stopForChargeLimit = false;
let chargeFailure = null;
async function worker() {
    while (next < urls.length && !stopForChargeLimit) {
        const url = urls[next++];
        const row = await audit(url);
        if (stopForChargeLimit) return;
        if (!row.error) {
            let charge;
            try { charge = await Actor.charge({ eventName: 'url-checked' }); }
            catch (e) { chargeFailure = e; stopForChargeLimit = true; return; }
            if (typeof charge?.chargedCount === 'number' && charge.chargedCount < 1) { stopForChargeLimit = true; return; }
            audited += 1;
            // This row was charged; stop other workers from publishing later unpaid work.
            if (charge?.eventChargeLimitReached) stopForChargeLimit = true;
        }
        await Actor.pushData(row);
    }
}
await Promise.all(Array.from({ length: 5 }, worker));
await Actor.setValue('SUMMARY', { urls: urls.length, audited, chargeLimitReached: stopForChargeLimit && !chargeFailure, chargeError: chargeFailure?.message ?? null, finishedAt: new Date().toISOString() });
if (chargeFailure) await Actor.fail('Could not charge for URL audit: ' + chargeFailure.message);
await Actor.exit();
