import test from 'node:test';
import assert from 'node:assert/strict';
import { hasWeakScriptSources } from '../src/csp.js';

test('CSP weakness is scoped to effective script sources', () => {
    assert.equal(hasWeakScriptSources("default-src 'self'; style-src 'unsafe-inline'"), false);
    assert.equal(hasWeakScriptSources("default-src 'self'; script-src 'self'"), false);
    assert.equal(hasWeakScriptSources("script-src 'self' 'unsafe-inline'; style-src 'self'"), true);
    assert.equal(hasWeakScriptSources("script-src *; object-src 'none'"), true);
    assert.equal(hasWeakScriptSources("default-src *"), true);
    assert.equal(hasWeakScriptSources("img-src *; script-src 'self'"), false);
});
