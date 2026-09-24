# SkyView Dynamics — Platform Setup

This guide covers everything you need to do manually before the marketplace platform goes live. The code is already in place — these are the external accounts and configuration steps.

---

## 1. Neon (Database)

1. Sign up at **https://console.neon.tech** (free tier is fine to start)
2. Create a new project: `skyview-dynamics`
3. Copy the **Pooled connection string** (looks like `postgresql://user:pass@ep-xxx.aws.neon.tech/neondb?sslmode=require`)
4. Add it to Netlify env vars as `DATABASE_URL`
5. Run migrations once:
   ```bash
   DATABASE_URL="your-connection-string" node scripts/migrate.js
   ```
6. Create your admin user directly in the DB:
   ```sql
   -- After running the migration, open the Neon SQL editor:
   UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
   ```
   Or register through `/app/register` first, then promote in SQL.

---

## 2. Netlify Environment Variables

In **Netlify dashboard → your site → Site configuration → Environment variables**, add:

| Variable | Value | Where to get it |
|---|---|---|
| `DATABASE_URL` | Neon pooled connection string | Neon dashboard |
| `JWT_SECRET` | 32+ random chars | `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"` |
| `RESEND_API_KEY` | `re_...` | Resend dashboard (step 3 below) |
| `STRIPE_SECRET_KEY` | `sk_live_...` | Stripe dashboard (Phase 2) |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | Stripe dashboard (Phase 2) |
| `GOOGLE_CLIENT_ID` | `....apps.googleusercontent.com` | Google Cloud Console (optional) |
| `GOOGLE_CLIENT_SECRET` | `GOCSPX-...` | Google Cloud Console (optional) |

---

## 3. Resend (Email)

1. Sign up at **https://resend.com**
2. Go to **Domains → Add Domain** → add `skyviewdynamics.com`
3. Add the DNS records Resend gives you (MX + DKIM + SPF) to your domain registrar
4. Wait for verification (usually < 1 hour)
5. Go to **API Keys → Create API Key** → copy the key
6. Add to Netlify as `RESEND_API_KEY`

Emails sent by the platform:
- Email verification on signup
- Operator approval / rejection
- Job alerts to nearby operators
- FAA cert expiry warnings (daily cron at 9am UTC)

---

## 4. Google OAuth (Optional)

To enable "Continue with Google" on the login and register pages:

1. Go to **https://console.cloud.google.com** → your project → **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth 2.0 Client ID** (type: Web application)
3. Under **Authorized redirect URIs**, add:
   - `https://skyviewd.netlify.app/api/auth/google/callback`
   - `http://localhost:8888/api/auth/google/callback` (local dev)
4. Copy **Client ID** and **Client Secret** → add to Netlify as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

If these env vars are absent, the Google button redirects to a 503 — everything else keeps working.

---

## 5. Turn on the Platform

Once the DB is migrated and env vars are set, flip the feature flag in `config.js`:

```js
features: {
    platform: true,   // ← change this
    calendly: false,  // ← optionally disable Calendly
    ...
}
```

This replaces the Calendly embed with the "Find an Operator / Post a Job" CTA and redirects the hero button to `/app/register`.

---

## 6. Local Development

```bash
# Install deps
npm install
cd platform && npm install && cd ..

# Copy env file
cp .env.example .env
# → Fill in DATABASE_URL and JWT_SECRET at minimum

# Run migrations
node scripts/migrate.js

# Start everything (Netlify Functions + Vite dev server with proxy)
npm run dev
```

The marketing site is at `http://localhost:8888/`  
The platform app is at `http://localhost:8888/app/`  
API functions are at `http://localhost:8888/api/`

---

## 7. Creating an Admin Account

After registering normally via `/app/register`, run this in the Neon SQL editor:

```sql
UPDATE users SET role = 'admin', email_verified = true WHERE email = 'your-email@example.com';
```

The admin panel is at `/app/admin` — use it to approve operator certifications.

---

## Phase 2 Checklist (payments)

- [ ] Stripe account → enable **Connect** (for operator payouts)
- [ ] Set `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in Netlify
- [ ] Complete the Stripe Connect onboarding flow in the operator profile (already wired in the DB schema)
- [ ] Uncomment the Stripe transfer logic in `netlify/functions/api-bookings.mjs`

---

## What's Already Deployed Automatically

| Thing | How |
|---|---|
| Netlify Functions | Auto-deployed on every push (directory: `netlify/functions/`) |
| React platform app | Built by `scripts/build.js` during Netlify build → `dist/app/` |
| Cert expiry cron | Runs daily at 9am UTC via `cron-cert-expiry.mjs` scheduled function |
| File storage | Netlify Blobs (no S3/R2 account needed) |
