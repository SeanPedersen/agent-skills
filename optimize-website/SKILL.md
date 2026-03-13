---
name: optimize-website
description: Audit and optimize website performance targeting Core Web Vitals (LCP, CLS, INP). Use when the user wants to improve page speed, reduce bundle size, or fix performance issues.
---

# Optimize Website Performance

Systematic checklist for auditing and optimizing web performance. Focuses on Core Web Vitals — LCP, CLS, INP — and general asset/network efficiency.

## Pre-Audit

Before optimizing, establish a baseline:

1. **Identify the tech stack** — framework, hosting, CSS approach, build tool
2. **Run Lighthouse** (or PageSpeed Insights) and record scores
3. **Check Core Web Vitals** in Chrome DevTools → Performance tab
4. **Note the LCP element** — this is your highest-priority target

## Optimization Checklist

Work through each section top-to-bottom. Items are ordered by typical impact.

---

### 1. Largest Contentful Paint (LCP)

The single most impactful metric. Target: < 2.5s.

- [ ] **Identify the LCP element** (usually hero image, heading, or above-fold content)
- [ ] **Preload the LCP resource** in `<head>` with `fetchpriority="high"`
  ```html
  <link rel="preload" href="/hero.webp" as="image" type="image/webp" fetchpriority="high" />
  ```
- [ ] **Eliminate render-blocking resources** — defer non-critical CSS/JS
- [ ] **Use SSR or pre-rendering** for above-fold content (avoid client-only rendering)
- [ ] **Reduce server response time (TTFB)** — add caching, use CDN, optimize DB queries

### 2. Images

Images are usually the largest payload. Optimize aggressively.

- [ ] **Convert to modern formats** — WebP or AVIF (often 50-90% smaller than PNG/JPEG)
- [ ] **Resize to display dimensions** — never serve a 3000px image for a 512px slot
- [ ] **Set explicit `width` and `height`** on all `<img>` tags (prevents CLS)
- [ ] **Lazy-load below-fold images** — `loading="lazy"` (never lazy-load the LCP image)
- [ ] **Use responsive `srcset`** for varying viewport sizes
- [ ] **Use framework image components** when available (Next.js `<Image>`, SvelteKit enhanced images, etc.)

### 3. Fonts

Web fonts are a common source of render-blocking and layout shift.

- [ ] **Prefer system font stacks** — zero download, instant render
  ```css
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  ```
- [ ] **If custom fonts are required:**
  - [ ] Self-host instead of using CDN (eliminates extra DNS + connection)
  - [ ] Use `font-display: swap` or `optional` to prevent invisible text
  - [ ] Preload critical font files: `<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin />`
  - [ ] Subset fonts to only needed character ranges
  - [ ] Use WOFF2 format (best compression)
- [ ] **Remove unused font files** from the build/static directory

### 4. Cumulative Layout Shift (CLS)

Target: < 0.1. Prevent elements from moving after render.

- [ ] **Set dimensions on all media** — images, videos, iframes, ads
- [ ] **Reserve space for dynamic content** — skeleton screens, min-height
- [ ] **Avoid injecting content above existing content** (banners, cookie bars → use fixed/sticky)
- [ ] **Use `transform` animations** instead of layout-triggering properties (top, left, width, height)
- [ ] **Set `overflow-y: scroll`** on `<html>` to prevent scrollbar-induced shift
- [ ] **Avoid `position: sticky`** on hero sections that cause jump on scroll

### 5. JavaScript

- [ ] **Audit bundle size** — use build analyzer (e.g. `rollup-plugin-visualizer`, `webpack-bundle-analyzer`)
- [ ] **Code-split routes** — only load JS for the current page
- [ ] **Tree-shake unused exports** — ensure bundler is configured for it
- [ ] **Defer non-critical scripts** — `<script defer>` or dynamic `import()`
- [ ] **Remove unused dependencies** from `package.json`
- [ ] **Avoid large client-side libraries** when server-side alternatives exist

### 6. CSS

- [ ] **Remove unused CSS** — PurgeCSS, Tailwind's built-in purging, etc.
- [ ] **Inline critical CSS** for above-fold content
- [ ] **Avoid `@import` chains** in CSS (each is a serial request)
- [ ] **Minimize CSS specificity wars** — prefer utility classes or scoped styles

### 7. Caching & Network

- [ ] **Set Cache-Control headers** for static assets (long max-age + immutable for hashed filenames)
- [ ] **Enable gzip or Brotli compression** on the server/CDN
- [ ] **Add in-memory or edge caching** for frequently read data
  ```typescript
  // Example: simple TTL cache
  const CACHE_TTL_MS = 30_000;
  let cached: Data | null = null;
  let cacheTime = 0;

  function getData(): Data {
    if (cached && Date.now() - cacheTime < CACHE_TTL_MS) return cached;
    cached = readFromSource();
    cacheTime = Date.now();
    return cached;
  }
  ```
- [ ] **Invalidate cache on writes** — never serve stale data after mutations
- [ ] **Use a CDN** for static assets if not already
- [ ] **Minimize third-party scripts** — each adds DNS lookups, connections, and JS execution
- [ ] **Use `<link rel="preconnect">` / `<link rel="dns-prefetch">`** for essential third-party origins

### 8. Server & Hosting

- [ ] **Enable HTTP/2 or HTTP/3** on the web server
- [ ] **Use SSR where appropriate** — faster first paint vs. client-only SPA
- [ ] **Configure reverse proxy correctly** (Nginx: gzip, proxy_cache, keepalive)
- [ ] **Use `npm ci --omit=dev`** in production to minimize server footprint
- [ ] **Add security headers** that also improve perf (e.g. `Strict-Transport-Security` avoids HTTP→HTTPS redirects)

### 9. Interaction to Next Paint (INP)

Target: < 200ms. Ensure the page responds quickly to user input.

- [ ] **Break up long tasks** — use `requestAnimationFrame` or `scheduler.yield()` for heavy computation
- [ ] **Debounce expensive event handlers** (scroll, resize, input)
- [ ] **Avoid layout thrashing** — batch DOM reads before writes
- [ ] **Use CSS `content-visibility: auto`** for off-screen sections

---

## Post-Optimization

1. **Re-run Lighthouse** and compare against baseline
2. **Test on real devices** — throttled 4G, mid-range mobile
3. **Check for regressions** — visual diff, CLS on navigation
4. **Monitor in production** — use Web Vitals API or RUM (Real User Monitoring)

## Quick Wins Summary

| Action                        | Typical Impact |
|-------------------------------|----------------|
| Preload LCP resource          | LCP -0.5–2s   |
| Convert images to WebP/AVIF   | 50-90% smaller |
| Switch to system fonts        | LCP -0.3–1s   |
| Enable Brotli compression     | 15-25% smaller |
| Add Cache-Control headers     | Repeat visits  |
| Remove unused JS/CSS          | Varies widely  |
