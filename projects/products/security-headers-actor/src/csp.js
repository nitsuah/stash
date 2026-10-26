export function hasWeakScriptSources(csp) {
    const directives = new Map();
    for (const raw of csp.split(';')) {
        const parts = raw.trim().split(/\s+/);
        const name = (parts.shift() ?? '').toLowerCase();
        if (name && !directives.has(name)) directives.set(name, parts);
    }
    // script-src overrides default-src; style-src does not weaken script policy.
    const sources = directives.get('script-src') ?? directives.get('default-src');
    return Boolean(sources?.some((source) => /^(?:'unsafe-inline'|'unsafe-eval'|\*)$/i.test(source)));
}
