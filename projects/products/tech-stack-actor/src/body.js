// Reads a fetch() response body as text under a strict byte budget. fetch() already decodes gzip/br, so this bounds DECODED bytes.
// Stops and cancels the stream once maxBytes have been read; the text is truncated, never an error.
export async function readTextCapped(response, maxBytes) {
    if (!response.body) return '';
    const reader = response.body.getReader();
    const chunks = [];
    let total = 0;
    while (total < maxBytes) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = value.byteLength > maxBytes - total ? value.subarray(0, maxBytes - total) : value;
        chunks.push(chunk);
        total += chunk.byteLength;
    }
    await reader.cancel().catch(() => {});
    return new TextDecoder('utf-8').decode(Buffer.concat(chunks, total));
}
