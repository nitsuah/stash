// Tiny local site with known SEO problems: a good page, a page with no title/description, a noindex page, two pages sharing a title, a 404 link.
import http from 'node:http';

const good = '<html lang="en"><head><title>A good page title for search</title><meta name="description" content="A meta description that is long enough to be useful in search results and short enough to avoid truncation."><link rel="canonical" href="http://localhost:8080/"><meta property="og:title" content="x"></head><body><h1>Hi</h1><a href="/bare">bare</a><a href="/noindex">noindex</a><a href="/dup1">d1</a><a href="/dup2">d2</a><a href="/gone">gone</a><img src="a.png" alt="a"></body></html>';
const pages = {
    '/': good,
    '/bare': '<html><head></head><body><p>no title, no h1</p><img src="a.png"></body></html>',
    '/noindex': '<html lang="en"><head><title>Hidden page that should not be indexed</title><meta name="robots" content="noindex"></head><body><h1>x</h1></body></html>',
    '/dup1': '<html lang="en"><head><title>Same title on two pages here</title></head><body><h1>1</h1></body></html>',
    '/dup2': '<html lang="en"><head><title>Same title on two pages here</title></head><body><h1>2</h1></body></html>',
    '/robots.txt': 'User-agent: *\nDisallow:\nSitemap: http://localhost:8080/sitemap.xml',
    '/sitemap.xml': '<urlset><url><loc>http://localhost:8080/</loc></url><url><loc>http://localhost:8080/bare</loc></url></urlset>',
};
http.createServer((req, res) => {
    const body = pages[req.url];
    res.writeHead(body ? 200 : 404, { 'content-type': req.url.endsWith('.xml') ? 'application/xml' : req.url.endsWith('.txt') ? 'text/plain' : 'text/html' });
    res.end(body ?? 'not found');
}).listen(8080, () => console.log('test server on 8080'));
