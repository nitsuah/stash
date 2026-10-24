// Local test site: a complete product page, a product missing offers and image, a broken JSON-LD block, an FAQ page and a page with none.
import http from 'node:http';

const ld = (o) => `<script type="application/ld+json">${typeof o === 'string' ? o : JSON.stringify(o)}</script>`;
const page = (body, head = '') => `<html lang="en"><head><title>t</title>${head}</head><body>${body}</body></html>`;
const pages = {
    '/': page('<a href="/good">g</a><a href="/bad-product">b</a><a href="/broken">x</a><a href="/faq">f</a><a href="/none">n</a>'),
    '/good': page('<h1>Good</h1>', ld({ '@context': 'https://schema.org', '@type': 'Product', name: 'Mug', image: 'https://x/mug.png', description: 'A mug', sku: '1', brand: 'Acme', aggregateRating: { '@type': 'AggregateRating', ratingValue: 4 }, offers: { '@type': 'Offer', price: '9.99', priceCurrency: 'USD', availability: 'InStock', url: 'https://x/mug' } })),
    '/bad-product': page('<h1>Bad</h1>', ld({ '@context': 'https://schema.org', '@type': 'Product', name: 'Cup' })),
    '/broken': page('<h1>Broken</h1>', ld('{ "@type": "Product", "name": "Oops",')),
    '/faq': page('<h1>FAQ</h1>', ld({ '@context': 'https://schema.org', '@graph': [{ '@type': 'FAQPage', mainEntity: [{ '@type': 'Question', name: 'Why?' }] }, { '@type': 'Organization', name: 'Acme' }] })),
    '/none': page('<h1>Nothing</h1>'),
};
http.createServer((req, res) => {
    const body = pages[req.url];
    res.writeHead(body ? 200 : 404, { 'content-type': 'text/html' });
    res.end(body ?? 'not found');
}).listen(8080, () => console.log('test server on 8080'));
