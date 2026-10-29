import test from 'node:test';
import assert from 'node:assert/strict';
import { readLimited, MAX_HTML_BYTES } from '../src/readLimited.js';

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

function mockStreamingReader(chunkSizes) {
    return {
        readCount: 0,
        cancelled: false,
        chunkSizes,
        async read() {
            this.readCount += 1;
            if (this.readCount > this.chunkSizes.length) {
                return { done: true, value: undefined };
            }
            return { done: false, value: new Uint8Array(this.chunkSizes[this.readCount - 1]) };
        },
        cancel() { this.cancelled = true; },
        releaseLock() {}
    };
}

function mockStreamingResponse(reader) {
    return {
        body: {
            getReader() { return reader; }
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

test('readLimited rejects single oversized chunk without allocating full chunk buffer', async () => {
    const reader = mockStreamingReader([10_000_000]);
    const res = mockStreamingResponse(reader);
    await assert.rejects(
        readLimited(res, 100),
        /exceeds.*byte limit/
    );
    assert.equal(reader.readCount, 1, 'should read at most once before rejecting');
});

test('readLimited cancels reader when body exceeds limit', async () => {
    const reader = mockStreamingReader([MAX_HTML_BYTES + 100]);
    const res = mockStreamingResponse(reader);
    let threw = false;
    try {
        await readLimited(res, MAX_HTML_BYTES);
    } catch {
        threw = true;
    }
    assert.ok(threw, 'readLimited should have thrown');
    assert.equal(reader.cancelled, true, 'reader.cancel() should be called on over-limit');
});

test('readLimited does not cancel reader under limit', async () => {
    const reader = mockStreamingReader([10, 20, 30]);
    const res = mockStreamingResponse(reader);
    const html = await readLimited(res, MAX_HTML_BYTES);
    assert.equal(reader.cancelled, false, 'reader.cancel() should not be called under limit');
});