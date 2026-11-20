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
