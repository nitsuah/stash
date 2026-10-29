const MAX_HTML_BYTES = 2_000_000;

async function readLimited(res, limit) {
    const reader = res.body.getReader();
    const chunks = [];
    let total = 0;
    try {
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            total += value.length;
            if (total > limit) {
                reader.releaseLock();
                throw new Error(`Response body exceeds ${limit} byte limit`);
            }
            chunks.push(value);
        }
    } finally {
        reader.releaseLock();
    }
    return new TextDecoder().decode(Buffer.concat(chunks));
}

export { readLimited, MAX_HTML_BYTES };