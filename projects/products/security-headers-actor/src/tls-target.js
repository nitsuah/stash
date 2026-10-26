export function tlsTarget(url) {
    const parsed = new URL(url);
    return { hostname: parsed.hostname, port: parsed.port ? Number(parsed.port) : 443 };
}
