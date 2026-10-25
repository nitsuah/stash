const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');

const root = fs.realpathSync(path.join(__dirname, 'sample-site'));
const isWithinRoot = (candidate) => candidate === root || candidate.startsWith(root + path.sep);

http.createServer((req, res) => {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
        res.writeHead(405, { Allow: 'GET, HEAD' });
        return res.end();
    }

    let pathname;
    try {
        pathname = decodeURIComponent(new URL(req.url || '/', 'http://localhost').pathname);
    } catch {
        res.writeHead(400);
        return res.end('Bad request');
    }
    if (pathname.includes('\0') || pathname.includes('\\')) {
        res.writeHead(400);
        return res.end('Bad request');
    }

    const relative = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
    const candidate = path.resolve(root, relative);
    if (!isWithinRoot(candidate)) {
        res.writeHead(403);
        return res.end('Forbidden');
    }

    let target;
    try {
        target = fs.realpathSync(candidate);
        if (!isWithinRoot(target) || !fs.statSync(target).isFile()) {
            res.writeHead(403);
            return res.end('Forbidden');
        }
    } catch {
        res.writeHead(404);
        return res.end('Not found');
    }

    if (req.method === 'HEAD') return res.end();
    try {
        res.end(fs.readFileSync(target));
    } catch {
        res.writeHead(404);
        res.end('Not found');
    }
}).listen(8080);
