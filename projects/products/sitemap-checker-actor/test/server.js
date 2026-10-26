// Local test site: robots.txt points to a sitemap index; children contain a good URL, a 404, a redirect, a duplicate, a noindex header and a bad lastmod.
import http from 'node:http';

const B = 'http://localhost:8080';
const routes = {
    '/robots.txt': ['text/plain', `User-agent: *\nDisallow:\nSitemap: ${B}/sitemap-index.xml`],
    '/sitemap-index.xml': ['application/xml', `<sitemapindex><sitemap><loc>${B}/sm1.xml</loc></sitemap><sitemap><loc>${B}/sm2.xml</loc></sitemap></sitemapindex>`],
    '/sm1.xml': ['application/xml', `<urlset><url><loc>${B}/good</loc><lastmod>2026-02-30T25:00:00+15:00</lastmod></url><url><loc>${B}/gone</loc></url><url><loc>${B}/moved</loc></url></urlset>`],
    '/sm2.xml': ['application/xml', `<urlset><url><loc>${B}/good</loc></url><url><loc>${B}/hidden</loc><lastmod>last tuesday</lastmod></url><url><loc>http://other.example/x</loc></url><url><loc>not-a-url</loc></url><url><loc>https://localhost:8080/good</loc></url></urlset>`],
    '/good': ['text/html', 'ok'],
    '/hidden': ['text/html', 'ok', { 'x-robots-tag': 'noindex' }],
};
http.createServer((req, res) => {
    if (req.url === '/moved') { res.writeHead(301, { location: `${B}/good` }); return res.end(); }
    const r = routes[req.url];
    res.writeHead(r ? 200 : 404, { 'content-type': r?.[0] ?? 'text/plain', ...(r?.[2] ?? {}) });
    res.end(r?.[1] ?? 'not found');
}).listen(8080, () => console.log('test server on 8080'));
