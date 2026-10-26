import test from 'node:test';
import assert from 'node:assert/strict';
import { tlsTarget } from '../src/tls-target.js';

test('TLS checks use the port of the URL being audited', () => {
    assert.deepEqual(tlsTarget('https://example.com/'), { hostname: 'example.com', port: 443 });
    assert.deepEqual(tlsTarget('https://example.com:8443/path'), { hostname: 'example.com', port: 8443 });
});
