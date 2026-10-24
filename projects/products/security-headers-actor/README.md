# Security Headers and TLS Check (grade A to F)

Give this Actor a list of URLs and get a grade from A to F for each, plus a plain-language list of what to fix. It checks the things that agencies and developers review before a launch or a client audit.

## What it checks
- Response headers: Strict-Transport-Security (present, long enough, covers subdomains), Content-Security-Policy (present, not obviously weak), clickjacking protection (X-Frame-Options or CSP frame-ancestors), X-Content-Type-Options, Referrer-Policy, Permissions-Policy.
- Information leaks: a Server header with a version number, X-Powered-By.
- Cookies: Secure, HttpOnly and SameSite flags on every cookie the response sets.
- HTTPS: whether plain HTTP redirects to HTTPS.
- Certificate: trusted or not, expired or expiring within 14 days, issuer, and the negotiated TLS version (flags TLS 1.0 and 1.1).

## Scoring
Each finding takes points off 100: high 20, medium 10, low 4. Grades: A 90 and up, B 75, C 60, D 40, F below 40. The score is a simple review aid, not a penetration test or a compliance result.

## Output
One row per URL: url, finalUrl after redirects, status, grade, score, findings (rule, severity, detail), tls details and the cookie count. A SUMMARY record has the totals. A URL that cannot be fetched returns a row with an error and no grade, and is not charged.

## Limits
Only the response to a single GET of each URL is examined, so headers set on other pages are not seen. A missing header is a finding, even when the site has a reason to omit it. This Actor makes ordinary requests and never attempts to exploit anything. Only test sites you are allowed to test.

Pricing is per checked URL (pay per event).
