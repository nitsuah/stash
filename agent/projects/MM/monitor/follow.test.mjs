import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fetchFollow, hopAllowed } from './follow.mjs';

const res = (status, location) => ({ status, headers: { get: () => location ?? null }, body: null, url: '' });

test('hopAllowed: same host, www and https upgrade only', () => {
  const u = s => new URL(s);
  assert.ok(hopAllowed(u('http://a.com/'), u('https://a.com/x')));
  assert.ok(hopAllowed(u('https://a.com/'), u('https://www.a.com/')));
  assert.ok(!hopAllowed(u('https://a.com/'), u('http://a.com/')));
  assert.ok(!hopAllowed(u('https://a.com/'), u('https://b.com/')));
  assert.ok(!hopAllowed(u('https://a.com/'), u('http://127.0.0.1/')));
  assert.ok(!hopAllowed(u('https://a.com/'), u('http://169.254.169.254/latest')));
  assert.ok(!hopAllowed(u('https://a.com/'), u('file:///etc/passwd')));
});

test('metadata destinations are blocked before the first request', async () => {
  const seen = [];
  const fetchImpl = async href => { seen.push(href); return res(200); };
  for (const url of [
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.170.2/v2/metadata',
    'http://metadata.google.internal/computeMetadata/v1/',
    'http://metadata./',
  ]) {
    await assert.rejects(fetchFollow(url, {}, fetchImpl), /url-blocked/);
  }
  assert.deepEqual(seen, []);
});

test('IPv4-mapped IPv6 metadata destinations are blocked before the first request', async () => {
  const seen = [];
  const fetchImpl = async href => { seen.push(href); return res(200); };
  for (const url of [
    'http://[::ffff:169.254.169.254]/latest/meta-data/',
    'http://[::ffff:169.254.170.2]/v2/metadata',
    'http://[::ffff:100.100.100.200]/latest/meta-data/',
  ]) {
    await assert.rejects(fetchFollow(url, {}, fetchImpl), /url-blocked/);
  }
  assert.deepEqual(seen, []);
});

test('redirects to cloud metadata hostnames are refused before requesting them', async () => {
  const seen = [];
  const fetchImpl = async href => {
    seen.push(href);
    return res(302, 'http://metadata.google.internal/computeMetadata/v1/');
  };
  await assert.rejects(fetchFollow('https://a.com/', {}, fetchImpl), /redirect-blocked/);
  assert.deepEqual(seen, ['https://a.com/']);
});

test('fetchFollow follows allowed hops and uses manual redirect mode', async () => {
  const calls = [];
  const f = async (href, init) => {
    calls.push([href, init.redirect]);
    return href === 'http://a.com/' ? res(301, 'https://a.com/home') : res(200);
  };
  const { response, finalUrl } = await fetchFollow('http://a.com/', {}, f);
  assert.equal(response.status, 200);
  assert.equal(finalUrl, 'https://a.com/home');
  assert.deepEqual(calls.map(c => c[1]), ['manual', 'manual']);
});

test('fetchFollow refuses a redirect to another host without requesting it', async () => {
  const seen = [];
  const f = async href => { seen.push(href); return res(302, 'http://169.254.169.254/latest'); };
  await assert.rejects(fetchFollow('https://a.com/', {}, f), /redirect-blocked/);
  assert.deepEqual(seen, ['https://a.com/']);
});

test('fetchFollow caps redirect loops', async () => {
  const f = async href => res(302, href.endsWith('/a') ? '/b' : '/a');
  await assert.rejects(fetchFollow('https://a.com/a', {}, f), /too-many-redirects/);
});

test('fetchFollow refuses an https -> http downgrade after an upgrade, before requesting it', async () => {
  const hops = { 'http://a.com/': res(301, 'https://a.com/secure'), 'https://a.com/secure': res(302, 'http://a.com/plain') };
  const seen = [];
  const fetchImpl = async u => { seen.push(u); return hops[u] ?? res(200); };
  await assert.rejects(fetchFollow('http://a.com/', {}, fetchImpl), /redirect-blocked/);
  assert.deepEqual(seen, ['http://a.com/', 'https://a.com/secure']);
});
