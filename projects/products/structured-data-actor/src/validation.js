// Required properties make the entity unusable for rich results; recommended ones improve them. Kept deliberately small and documented in the README.
const RUBRIC = {
    Product: { required: ['name'], recommended: ['image', 'description', 'sku', 'brand', 'aggregateRating', 'offers'] },
    Offer: { required: ['priceCurrency'], recommended: ['availability', 'url'] },
    Article: { required: [], recommended: ['headline', 'image', 'datePublished', 'author', 'dateModified', 'publisher'] },
    LocalBusiness: { required: ['name', 'address'], recommended: ['telephone', 'openingHours', 'openingHoursSpecification', 'image', 'url', 'geo'] },
    Organization: { required: ['name', 'url'], recommended: ['logo', 'sameAs', 'contactPoint'] },
    FAQPage: { required: ['mainEntity'], recommended: [] },
    Question: { required: ['name', 'acceptedAnswer'], recommended: [] },
    BreadcrumbList: { required: ['itemListElement'], recommended: [] },
    ListItem: { required: ['position', 'name'], recommended: ['item'] },
    Event: { required: ['name', 'startDate', 'location'], recommended: ['endDate', 'image', 'offers', 'description'] },
    Recipe: { required: ['name', 'image', 'recipeIngredient'], recommended: ['recipeInstructions', 'author', 'aggregateRating', 'cookTime'] },
    WebSite: { required: ['name', 'url'], recommended: ['potentialAction'] },
    Person: { required: ['name'], recommended: ['url', 'sameAs'] },
    JobPosting: { required: ['title', 'description', 'datePosted', 'hiringOrganization', 'jobLocation'], recommended: ['validThrough', 'baseSalary', 'employmentType'] },
};
const ALIASES = {
    NewsArticle: 'Article', BlogPosting: 'Article', TechArticle: 'Article', Restaurant: 'LocalBusiness', Store: 'LocalBusiness', Dentist: 'LocalBusiness',
    ProfessionalService: 'LocalBusiness', HomeAndConstructionBusiness: 'LocalBusiness', AutoRepair: 'LocalBusiness', MedicalBusiness: 'LocalBusiness',
    CafeOrCoffeeShop: 'LocalBusiness', LegalService: 'LocalBusiness', RealEstateAgent: 'LocalBusiness', Corporation: 'Organization', NGO: 'Organization',
};
const SEVERITY = { required: 'high', recommended: 'low' };
export function normalizeType(rawType) {
    const raw = String(rawType);
    let local = raw;
    try {
        const parsed = new URL(raw);
        if (parsed.hostname.toLowerCase() === 'schema.org') local = parsed.pathname.split('/').filter(Boolean).at(-1) ?? raw;
    } catch {
        local = raw.replace(/^schema\.org\//i, '');
    }
    return ALIASES[local] ?? local;
}

const present = (v) => v !== undefined && v !== null && !(typeof v === 'string' && !v.trim()) && !(Array.isArray(v) && !v.length);
const asArray = (v) => (Array.isArray(v) ? v : v === undefined || v === null ? [] : [v]);

export function validate(entity) {
    const issues = [];
    for (const rawType of asArray(entity['@type'])) {
        const type = normalizeType(rawType);
        const rule = RUBRIC[type];
        if (!rule) continue;
        for (const level of ['required', 'recommended']) {
            for (const prop of rule[level]) {
                if (!present(entity[prop])) issues.push({ type: rawType, rule: `${level}-missing`, property: prop, severity: SEVERITY[level], detail: `${rawType} is missing ${level === 'required' ? 'required' : 'recommended'} property "${prop}"` });
            }
        }
        if (type === 'Product' && !['offers', 'aggregateRating', 'review'].some((key) => present(entity[key]))) {
            issues.push({ type: rawType, rule: 'required-missing', property: 'offers|aggregateRating|review', severity: 'high', detail: 'Product must provide offers, aggregateRating, or review for a product snippet' });
        }
        if (type === 'Offer') {
            const hasPrice = present(entity.price) || asArray(entity.priceSpecification).some((spec) => spec && typeof spec === 'object' && present(spec.price));
            if (!hasPrice) issues.push({ type: rawType, rule: 'required-missing', property: 'price|priceSpecification.price', severity: 'high', detail: 'Offer must provide price or priceSpecification.price' });
        }
    }
    return issues;
}
