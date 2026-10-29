import test from 'node:test';
import assert from 'node:assert/strict';
import { readTextCapped } from '../src/body.js';

function endlessStream(chunkSize) {
    const state = { pulls: 0, cancelled: false };
    const body = new ReadableStream({
        pull(controller) { state.pulls += 1; controller.enqueue(new Uint8Array(chunkSize).fill(97)); },
        cancel() { state.cancelled = true; },
    });
    return { state, response: new Response(body) };
}

test('returns the whole body when it fits the budget', async () => {
    assert.equal(await readTextCapped(new Response('hello'), 100), 'hello');
    assert.equal(await readTextCapped(new Response(null), 100), '');
});

test('stops reading and cancels an endless stream at the byte budget', async () => {
    const { state, response } = endlessStream(1000);
    const text = await readTextCapped(response, 2500);
    assert.equal(text.length, 2500);
    assert.equal(state.cancelled, true);
    assert.ok(state.pulls < 20, 'must not keep pulling after the budget is reached');
});