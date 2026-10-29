import test from 'node:test';
import assert from 'node:assert/strict';
import { readLimited, MAX_HTML_BYTES } from '../src/main.js';

function mockResponse(bodyBytes) {
    const uint8 = new Uint8Array(bodyBytes);
    return {
        body: {
            getReader() {
                let done = false;
                return {
                    async read() {
                        if (done) return { done: true, value: undefined };
                        done = true;
                        return { done: false, value: uint8 };
                    },
                    releaseLock() {}
                };
            }
        }
    };
}

test('readLimited accepts body under limit', async () => {
    const res = mockResponse([72, 101, 108, 108, 111]);
    const html = await readLimited(res, MAX_HTML_BYTES);
    assert.equal(html, 'Hello');
});

test('readLimited rejects body over limit without buffering all', async () => {
    const oversized = new Uint8Array(MAX_HTML_BYTES + 100);
    const res = mockResponse(oversized);
    await assert.rejects(
        readLimited(res, MAX_HTML_BYTES),
        /exceeds.*byte limit/
    );
});

test('readLimited enforces exact limit boundary', async () => {
    const exact = new Uint8Array(MAX_HTML_BYTES);
    const res = mockResponse(exact);
    const html = await readLimited(res, MAX_HTML_BYTES);
    assert.equal(html.length, MAX_HTML_BYTES);
});