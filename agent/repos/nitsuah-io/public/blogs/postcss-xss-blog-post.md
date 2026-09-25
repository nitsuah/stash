# The </style> Escape Hatch: How PostCSS Quietly Enabled XSS in Your Build Pipeline

If you're running a Next.js, Vite, or any modern frontend stack, there's a good chance PostCSS is somewhere in your dependency tree — and until very recently, it had a surprisingly simple XSS vector hiding in plain sight.

Here's what happened, why it matters, and how to fix it in under five minutes.

---

## What Is PostCSS?

PostCSS is the CSS transformation engine that powers Tailwind, Autoprefixer, CSS Modules, and dozens of other tools. It parses CSS into an abstract syntax tree (AST), lets plugins transform it, then stringifies the AST back into CSS. Chances are it's already in your `node_modules`, even if you've never imported it directly.

---

## The Vulnerability (CVE-2026-41305)

**CVSS: 6.1 Medium | CWE-79: Improper Neutralization of Input During Web Page Generation**

PostCSS versions below `8.5.10` do not escape `</style>` sequences when stringifying a CSS AST back to a string. This is harmless in most build pipelines — but becomes a serious problem the moment user-supplied CSS is passed through PostCSS and the output is embedded in an HTML `<style>` tag server-side.

### Proof of concept

```js
const postcss = require('postcss');

const userCSS = 'body { content: "</style><script>alert(1)</script><style>"; }';
const ast = postcss.parse(userCSS);
const output = ast.toResult().css;
const html = `<style>${output}</style>`;

console.log(html);
// <style>body { content: "</style><script>alert(1)</script><style>"; }</style>
//
// The browser sees </style> and closes the style tag.
// <script>alert(1)</script> executes freely.
```

The `</style>` in the CSS value closes the `<style>` tag in the browser's HTML parser before CSS parsing has a chance to scope it. Anything after that point is interpreted as raw HTML — including `<script>` tags.

---

## Who Is Actually At Risk?

This is important to understand before you panic. The vulnerability requires a specific chain:

1. Your app accepts **user-supplied CSS** as input
2. That CSS is passed through **PostCSS** (parsed and re-stringified)
3. The output is **embedded in an HTML `<style>` tag** at runtime (server-side rendering or dynamic injection)

**Build-time-only use (Next.js, Vite, Tailwind, etc.):** PostCSS processes your source files at build time, not user input at runtime. Your XSS risk from this specific CVE is low to none.

**At-risk patterns:** Theme editors, CSS sandboxes, style customization features, any SaaS product that lets users write or paste CSS that gets server-rendered into a page.

That said — Dependabot will flag it regardless, and the fix is trivial, so there's no reason not to patch it.

---

## The Fix

PostCSS `8.5.10` resolves this by escaping `</style` sequences in all stringified output:

```js
output = output.replace(/<\/(style)/gi, '<\\/$1');
```

Since `postcss` is typically a **transitive dependency** (something else pulls it in), you can't just add it to your `dependencies` directly and call it done. You need to **override** the resolved version.

### npm

Add to `package.json`:

```json
{
  "overrides": {
    "postcss": ">=8.5.10"
  }
}
```

### yarn

```json
{
  "resolutions": {
    "postcss": ">=8.5.10"
  }
}
```

### pnpm

```json
{
  "pnpm": {
    "overrides": {
      "postcss": ">=8.5.10"
    }
  }
}
```

Then regenerate your lockfile and verify:

```bash
npm install
npm ls postcss
# Every entry in the tree should show 8.5.10 or higher
```

---

## Docker Users: One Extra Step

If your app ships as a Docker image, the fix isn't live until the image is **rebuilt**. The lockfile gets baked into the image at build time via `npm ci` — so you need to:

1. Apply the override and regenerate the lockfile locally
2. Commit both `package.json` and the updated lockfile
3. Rebuild the Docker image
4. Verify inside the container:

```bash
docker run --rm <your-image> npm ls postcss
```

If your CI/CD pipeline builds the image on push, steps 3 and 4 happen automatically after the commit lands.

---

## Verify Dependabot Closes the Alert

After merging, GitHub will rescan your lockfile and auto-close the alert — usually within 24 hours. If it stays open, trigger a manual rescan: **Security → Dependabot alerts → Check for updates**.

---

## Takeaway

CVE-2026-41305 is a clean example of why transitive dependencies matter. PostCSS is in virtually every modern frontend project, and most developers have never thought about it as an attack surface — because in a build-time context, it isn't one. But the moment you build a feature that processes user CSS at runtime, the threat model shifts and that invisible dependency becomes the weak link.

The fix is a one-liner override and a lockfile regeneration. Ship it.

---

*Discovered and reported by [Sunil Kumar](https://tharvid.in/) ([@TharVid](https://github.com/TharVid)). Patched in PostCSS 8.5.10.*
