export async function readLimitedBody(response, limit) {
    if (!response.body) return Buffer.alloc(0);
    const reader = response.body.getReader();
    const chunks = [];
    let total = 0;
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        total += value.byteLength;
        if (total > limit) {
            await reader.cancel().catch(() => {});
            throw new Error('Response exceeds ' + limit + ' byte limit');
        }
        chunks.push(Buffer.from(value));
    }
    return Buffer.concat(chunks, total);
}

export function isSameHostname(url, origin) {
    try { return new URL(url).hostname === new URL(origin).hostname; }
    catch { return false; }
}

export function isValidLastmod(value) {
    const match = /^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(Z|[+-]\d{2}:\d{2})?)?$/.exec(value);
    if (!match) return false;
    const [, y, mo, d, hh, mm, ss, , zone] = match;
    const year = Number(y), month = Number(mo), day = Number(d);
    if (month < 1 || month > 12) return false;
    const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (day < 1 || day > days[month - 1]) return false;
    if (hh !== undefined && (Number(hh) > 23 || Number(mm) > 59 || Number(ss ?? 0) > 59)) return false;
    if (zone && zone !== 'Z') {
        const zh = Number(zone.slice(1, 3)), zm = Number(zone.slice(4, 6));
        if (zh > 14 || zm > 59 || (zh === 14 && zm !== 0)) return false;
    }
    return true;
}
