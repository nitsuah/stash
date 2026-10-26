import test from 'node:test';
import assert from 'node:assert/strict';
import { validate, normalizeType } from '../src/validation.js';

const high = (entity) => validate(entity).filter((issue) => issue.severity === 'high');

test('Product accepts aggregateRating as an alternative to offers', () => {
    assert.deepEqual(high({ '@type': 'Product', name: 'Mug', aggregateRating: { ratingValue: 4 } }), []);
    assert.equal(high({ '@type': 'Product', name: 'Mug' }).some((issue) => issue.property === 'offers|aggregateRating|review'), true);
});

test('Offer accepts priceSpecification.price', () => {
    assert.deepEqual(high({ '@type': 'Offer', priceCurrency: 'USD', priceSpecification: { price: '9.99' } }), []);
    assert.equal(high({ '@type': 'Offer', priceCurrency: 'USD' }).some((issue) => issue.property === 'price|priceSpecification.price'), true);
});

test('Article fields are recommendations rather than required properties', () => {
    const issues = validate({ '@type': 'Article', headline: 'A short article' });
    assert.equal(issues.some((issue) => issue.severity === 'high'), false);
    assert.equal(issues.some((issue) => issue.property === 'author' && issue.severity === 'low'), true);
});

test('absolute schema.org type IRIs normalize before validation', () => {
    assert.equal(normalizeType('https://schema.org/Person'), 'Person');
    assert.equal(normalizeType('http://schema.org/Person'), 'Person');
    assert.equal(normalizeType('Person'), 'Person');
    assert.deepEqual(high({ '@type': 'https://schema.org/Person', name: 'Ada' }), []);
});
