// Tiny local site for testing: one page with a good link, a broken internal link, a broken external host and an unreachable host.
import http from 'node:http';

const pages = {
    '/': '<a href="/about">About</a> <a href="/missing">Missing</a> <a href="https://example.com/">Ok external</a> <a href="https://this-domain-does-not-exist-12345.invalid/">Dead host</a> <a href="mailto:a@b.c">mail</a>',
    '/about': '<a href="/">Home</a> <a href="/also-missing">Also missing</a>',
};
http.createServer((req, res) => {
    const body = pages[req.url];
    res.writeHead(body ? 200 : 404, { 'content-type': 'text/html' });
    res.end(body ?? 'not found');
}).listen(8080, () => console.log('test server on 8080'));
