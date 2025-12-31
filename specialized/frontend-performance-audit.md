# Specialized: Frontend Performance & SEO Audit

## Overview

**Use Case:** Deep-dive audit for frontend performance optimization, Core Web Vitals compliance, and SEO best practices
**Use With:** Phase 6 (Frontend) or standalone
**Estimated Time:** 2-4 hours
**Frameworks:** React, Vue, Angular, Svelte, Next.js, Nuxt, Astro, vanilla JS, static sites

---

## Files to Provide

```
[ ] HTML entry files (index.html, main templates)
[ ] Build configuration (webpack.config.js, vite.config.ts, next.config.js, etc.)
[ ] CSS/SCSS/Tailwind configuration files
[ ] JavaScript/TypeScript entry points
[ ] Image optimization configuration
[ ] Font loading implementation
[ ] robots.txt and sitemap.xml
[ ] Meta tag templates or head management (react-helmet, next/head, etc.)
[ ] Third-party script integration code
[ ] Service worker configuration (if PWA)
[ ] Server configuration (nginx.conf, vercel.json, netlify.toml, etc.)
[ ] Package.json (for dependency analysis)
```

---

## Audit Prompt

```markdown
# Frontend Performance & SEO Audit

## Context
You are conducting a comprehensive frontend performance and SEO audit. This audit focuses on Core Web Vitals optimization, search engine optimization, asset delivery efficiency, and third-party script impact.

[PASTE: Phase 6 Carry-Forward Summary if available]

## Environment Details
- **Framework:** [React/Vue/Angular/Next.js/etc.]
- **Hosting:** [Vercel/Netlify/AWS/etc.]
- **CDN:** [Cloudflare/Fastly/etc. or none]
- **Target Audience:** [Geographic regions]

## Provided Materials
[PASTE: Relevant code and configuration files]

---

## Audit Checklist

### CWV-1: Largest Contentful Paint (LCP)

**Target:** < 2.5 seconds (Good) | < 4.0 seconds (Needs Improvement)

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| LCP element identified | | |
| Hero images preloaded (`<link rel="preload">`) | | |
| LCP element uses `fetchpriority="high"` | | |
| Server response time (TTFB) < 600ms | | |
| Critical CSS inlined or preloaded | | |
| No render-blocking resources before LCP | | |
| LCP image served in modern format (WebP/AVIF) | | |

Common LCP Issues:
- [ ] Large unoptimized hero images
- [ ] Slow server response times
- [ ] Render-blocking JavaScript
- [ ] Client-side rendering delays
- [ ] Web font blocking text display

---

### CWV-2: Cumulative Layout Shift (CLS)

**Target:** < 0.1 (Good) | < 0.25 (Needs Improvement)

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Images have explicit width/height or aspect-ratio | | |
| Ads/embeds have reserved space | | |
| Web fonts use `font-display: swap` or `optional` | | |
| Dynamic content injected below the fold | | |
| No late-loading above-the-fold content | | |
| Animations use `transform` instead of layout properties | | |
| No content inserted above existing content | | |

Common CLS Issues:
- [ ] Images without dimensions
- [ ] Ads loading without reserved space
- [ ] Font swap causing text reflow
- [ ] Dynamic banners/notifications shifting content
- [ ] Lazy-loaded content above the fold

---

### CWV-3: Interaction to Next Paint (INP)

**Target:** < 200ms (Good) | < 500ms (Needs Improvement)

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Event handlers optimized (debounced/throttled) | | |
| Long tasks broken up (< 50ms each) | | |
| Main thread not blocked during interactions | | |
| `requestIdleCallback` used for non-critical work | | |
| Heavy computations moved to Web Workers | | |
| React/Vue re-renders optimized | | |
| No synchronous layout thrashing | | |

Common INP Issues:
- [ ] Long-running JavaScript blocking interactions
- [ ] Excessive DOM manipulation
- [ ] Unoptimized React/Vue component re-renders
- [ ] Heavy third-party scripts on main thread
- [ ] Synchronous XHR requests

---

### CWV-4: First Input Delay (FID) / Time to Interactive

**Target:** FID < 100ms (Good) | < 300ms (Needs Improvement)

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| JavaScript execution optimized during load | | |
| Third-party scripts deferred or async | | |
| Hydration strategy optimized (for SSR frameworks) | | |
| No long tasks during page load | | |
| Critical JS prioritized over non-critical | | |

---

### CWV-5: Time to First Byte (TTFB)

**Target:** < 800ms (Good) | < 1800ms (Needs Improvement)

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| CDN or edge caching configured | | |
| Server-side caching implemented | | |
| Database queries optimized | | |
| Compression (gzip/brotli) enabled | | |
| HTTP/2 or HTTP/3 enabled | | |
| DNS prefetch for critical domains | | |

---

### SEO-1: Meta Tags & Title

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Unique `<title>` per page (50-60 characters) | | |
| Meta description present (150-160 characters) | | |
| `<meta name="viewport">` configured | | |
| `<meta charset="UTF-8">` present | | |
| Canonical URL specified (`<link rel="canonical">`) | | |
| Hreflang for multi-language sites | | |
| No duplicate titles across pages | | |

---

### SEO-2: Open Graph & Social Cards

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| `og:title`, `og:description`, `og:image` present | | |
| `og:url` and `og:type` specified | | |
| `og:image` dimensions (1200x630 recommended) | | |
| Twitter Card meta tags configured | | |
| `twitter:card` type specified | | |
| `twitter:image` with proper dimensions | | |

---

### SEO-3: Structured Data (Schema.org)

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| JSON-LD structured data implemented | | |
| Appropriate schema types used (Organization, Product, Article, etc.) | | |
| Schema validated with Google Rich Results Test | | |
| Breadcrumb markup for navigation | | |
| FAQ schema for Q&A content | | |
| No structured data errors or warnings | | |

---

### SEO-4: Sitemap & Robots

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| XML sitemap exists and accessible | | |
| Sitemap includes all indexable pages | | |
| Sitemap excludes non-indexable pages | | |
| `robots.txt` properly configured | | |
| Disallow directives for sensitive paths | | |
| Sitemap referenced in robots.txt | | |
| No critical pages blocked by robots.txt | | |

---

### SEO-5: Semantic HTML & Accessibility

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Proper heading hierarchy (single H1, logical H2-H6) | | |
| Alt text for all images | | |
| ARIA landmarks used appropriately | | |
| Skip navigation links for screen readers | | |
| Form labels associated with inputs | | |
| Sufficient color contrast | | |
| Focus states visible | | |

---

### SEO-6: URL Structure

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| URLs are descriptive and human-readable | | |
| Consistent trailing slash policy | | |
| No duplicate content (www vs non-www) | | |
| HTTPS enforced with redirects | | |
| URL parameters minimized | | |
| No session IDs in URLs | | |

---

### SEO-7: Crawlability

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| No critical content behind JavaScript-only rendering | | |
| Internal linking structure logical | | |
| No orphan pages (unreachable pages) | | |
| 404 pages return proper status code | | |
| Redirect chains minimized (< 3 hops) | | |
| No soft 404s (200 status for missing pages) | | |

---

### SEO-8: Mobile SEO

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Mobile-friendly design (responsive or adaptive) | | |
| No horizontal scrolling on mobile | | |
| Touch targets appropriately sized (48x48 minimum) | | |
| Font sizes readable without zooming (16px minimum) | | |
| Mobile page speed optimized | | |
| Viewport configured correctly | | |

---

### AST-1: Image Optimization

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Modern formats used (WebP, AVIF) with fallbacks | | |
| Responsive images with `srcset` and `sizes` | | |
| Images appropriately compressed | | |
| Lazy loading for below-the-fold images | | |
| Image dimensions specified (prevent CLS) | | |
| Critical images preloaded | | |
| No oversized images served | | |
| Image CDN used (optional) | | |

---

### AST-2: CSS Optimization

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Critical CSS inlined or preloaded | | |
| Non-critical CSS loaded asynchronously | | |
| CSS minified in production | | |
| Unused CSS removed (PurgeCSS, etc.) | | |
| CSS file size < 50KB (critical path) | | |
| No render-blocking stylesheets | | |
| CSS-in-JS extraction configured (if applicable) | | |

---

### AST-3: JavaScript Optimization

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Code splitting implemented | | |
| Tree shaking enabled | | |
| JavaScript minified and compressed | | |
| Non-critical JS deferred or async | | |
| Bundle size < 200KB (initial load) | | |
| Dynamic imports for route-based splitting | | |
| No duplicate dependencies in bundle | | |
| Source maps disabled in production (or separate) | | |

---

### AST-4: Font Optimization

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| `font-display: swap` or `optional` used | | |
| Font files preloaded for critical text | | |
| Font subsetting implemented | | |
| Variable fonts used where appropriate | | |
| Local fonts preferred over web fonts | | |
| WOFF2 format prioritized | | |
| Fallback fonts match web font metrics | | |

---

### AST-5: Caching Strategy

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Cache-Control headers properly configured | | |
| Immutable assets have long cache (1 year) | | |
| Content hashing in filenames for cache busting | | |
| Service worker caching strategy defined | | |
| ETags configured correctly | | |
| HTML has short/no cache (for updates) | | |

---

### AST-6: Compression & Delivery

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Gzip or Brotli compression enabled | | |
| HTTP/2 or HTTP/3 enabled | | |
| CDN configured for static assets | | |
| Resource hints used (`preconnect`, `dns-prefetch`) | | |
| Early hints (103) implemented where supported | | |

---

### AST-7: Lazy Loading & Code Splitting

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Route-based code splitting | | |
| Component-level lazy loading for heavy components | | |
| Images below fold lazy loaded | | |
| Intersection Observer used appropriately | | |
| Placeholder/skeleton states during loading | | |
| Suspense boundaries (React) or equivalent | | |

---

### TPS-1: Script Loading Strategy

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Third-party scripts loaded async or defer | | |
| Scripts not blocking main thread | | |
| `loading="lazy"` for third-party iframes | | |
| Scripts loaded after user interaction where possible | | |
| Facade pattern for heavy embeds (YouTube, Maps) | | |

---

### TPS-2: Analytics & Tracking Impact

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Analytics tag manager (GTM) optimized | | |
| Analytics scripts loaded conditionally | | |
| No duplicate tracking scripts | | |
| Beacon API used for non-blocking analytics | | |
| Privacy-focused analytics considered | | |

---

### TPS-3: Advertising Scripts

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Ad scripts lazy loaded | | |
| Reserved space for ad slots (prevent CLS) | | |
| Above-the-fold ads limited | | |
| Ad refresh strategy optimized | | |

---

### TPS-4: Third-Party Performance Audit

Inventory of third-party scripts:
| Script | Purpose | Load Time Impact | Main Thread Time | Recommendation |
|--------|---------|------------------|------------------|----------------|
| | | | | |
| | | | | |
| | | | | |

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Third-party scripts inventoried | | |
| Each script's performance impact measured | | |
| Unused third-party scripts removed | | |
| Third-party domains preconnected | | |
| Subresource Integrity (SRI) for third-party scripts | | |

---

### TPS-5: Third-Party Risk Assessment

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| Third-party script security reviewed | | |
| CSP (Content Security Policy) configured | | |
| Third-party cookie usage understood | | |
| Fallback behavior if third-party fails | | |
| Self-hosting considered for critical scripts | | |

---

### Air-Gap Considerations (if applicable)

Assessment:
| Check | Status | Notes |
|-------|--------|-------|
| All fonts hosted locally (no Google Fonts CDN) | | |
| All JavaScript dependencies bundled | | |
| No external analytics or tracking | | |
| No external image services | | |
| Service worker configured for offline | | |
| All assets available without internet | | |

---

## Carry-Forward Summary

Provide a summary including:
1. **Critical Performance Issues:** [List any Critical/High findings]
2. **Core Web Vitals Status:** [LCP/CLS/INP/FID scores and status]
3. **SEO Compliance Level:** [Compliant/Partial/Non-compliant]
4. **Top 3 Quick Wins:** [Highest impact, lowest effort fixes]
5. **Third-Party Impact:** [Total third-party load time contribution]
```

---

## Testing Procedures

### Tool Reference

| Tool | Purpose | URL/Command |
|------|---------|-------------|
| Lighthouse | Comprehensive audit | Chrome DevTools > Lighthouse |
| PageSpeed Insights | Real-world + lab data | https://pagespeed.web.dev |
| WebPageTest | Detailed waterfall analysis | https://webpagetest.org |
| Chrome DevTools | Network, Performance, Coverage | F12 in Chrome |
| web.dev/measure | Core Web Vitals | https://web.dev/measure |
| GTmetrix | Performance scoring | https://gtmetrix.com |
| Screaming Frog | SEO crawling | https://screamingfrog.co.uk |
| Google Search Console | Real-world CWV data | https://search.google.com/search-console |

### Lighthouse CI Commands

```bash
# Install Lighthouse CI
npm install -g @lhci/cli

# Run Lighthouse audit
lhci autorun --collect.url=https://example.com

# Run with specific categories
lighthouse https://example.com --output=json --output-path=./report.json \
  --only-categories=performance,seo,accessibility,best-practices

# Run in headless mode
lighthouse https://example.com --chrome-flags="--headless"
```

### Core Web Vitals Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | < 2.5s | 2.5s - 4.0s | > 4.0s |
| FID | < 100ms | 100ms - 300ms | > 300ms |
| CLS | < 0.1 | 0.1 - 0.25 | > 0.25 |
| INP | < 200ms | 200ms - 500ms | > 500ms |
| TTFB | < 800ms | 800ms - 1800ms | > 1800ms |
| FCP | < 1.8s | 1.8s - 3.0s | > 3.0s |

### Bundle Analysis Commands

```bash
# Webpack bundle analyzer
npx webpack-bundle-analyzer stats.json

# Vite bundle analysis
npx vite-bundle-visualizer

# Next.js bundle analysis
ANALYZE=true npm run build

# Source map explorer
npx source-map-explorer build/static/js/*.js

# Bundle size check
npx bundlesize
```

### SEO Validation Tools

- **Structured Data:** https://validator.schema.org/
- **Rich Results Test:** https://search.google.com/test/rich-results
- **Robots.txt Tester:** Google Search Console
- **Mobile-Friendly Test:** https://search.google.com/test/mobile-friendly
- **Site Speed:** https://developers.google.com/speed/pagespeed/insights/

---

## Output Format

For each finding:

```markdown
### [CWV/SEO/AST/TPS-###] Finding Title

**Severity:** Critical/High/Medium/Low/Informational
**Category:** Core Web Vitals / SEO / Asset Optimization / Third-Party Scripts
**Metric Impact:** [Specific metric affected, e.g., "LCP +1.2s"]

**Current State:**
- Metric value: [Current measurement]
- Threshold: [Target threshold]
- Gap: [Difference]

**Location:**
- File: `path/to/file.js:line`
- URL: [Affected page(s)]

**Issue:**
[Description of the performance or SEO issue]

**Evidence:**
[Lighthouse score, waterfall data, or metric measurement]

**Recommendation:**
[Specific fix with code example if applicable]

**Expected Impact:**
- Metric improvement: [Estimated improvement]
- User experience: [UX improvement description]
```

### Severity Guidelines

| Severity | Performance Criteria | SEO Criteria |
|----------|---------------------|--------------|
| Critical | LCP > 6s, CLS > 0.5, INP > 1s | Blocked by robots.txt incorrectly, no indexing |
| High | LCP > 4s, CLS > 0.25, INP > 500ms | Missing canonical, major duplicate content |
| Medium | LCP > 2.5s, CLS > 0.1, INP > 200ms | Missing Open Graph, poor heading structure |
| Low | Slightly above thresholds | Minor SEO improvements |
| Informational | Optimization opportunities | Best practice suggestions |

---

## Deliverables

1. **Core Web Vitals Report** - All CWV metrics with current vs target values
2. **SEO Compliance Matrix** - Checklist of SEO requirements met/unmet
3. **Asset Optimization Inventory** - All assets with size, format, optimization status
4. **Third-Party Script Impact Analysis** - Performance cost of each third-party
5. **Prioritized Optimization Roadmap** - Ordered list of fixes by impact/effort
6. **Lighthouse Baseline Report** - JSON/HTML export for tracking progress

---

## Quick Reference: Optimization Patterns

### Image Optimization Pattern

```html
<!-- Modern image with fallback and lazy loading -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img
    src="image.jpg"
    alt="Descriptive alt text"
    width="800"
    height="600"
    loading="lazy"
    decoding="async"
  >
</picture>

<!-- Critical hero image (above the fold) -->
<link rel="preload" as="image" href="hero.webp" type="image/webp">
<img
  src="hero.webp"
  alt="Hero image"
  width="1200"
  height="600"
  fetchpriority="high"
>
```

### Critical CSS Pattern

```html
<head>
  <!-- Critical CSS inlined -->
  <style>
    /* Above-the-fold styles only */
    .hero { ... }
    .nav { ... }
  </style>

  <!-- Non-critical CSS loaded async -->
  <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

### Font Loading Pattern

```css
/* Optimized font loading */
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2'),
       url('font.woff') format('woff');
  font-display: swap;
  font-weight: 400;
  font-style: normal;
  unicode-range: U+0000-00FF; /* Subset to Latin characters */
}
```

```html
<!-- Preload critical font -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
```

### Third-Party Script Facade Pattern

```html
<!-- YouTube facade - loads iframe only on interaction -->
<div class="youtube-facade" data-video-id="VIDEO_ID">
  <img src="https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg"
       alt="Video thumbnail"
       loading="lazy">
  <button aria-label="Play video">
    <svg><!-- Play icon --></svg>
  </button>
</div>

<script>
document.querySelectorAll('.youtube-facade').forEach(facade => {
  facade.addEventListener('click', function() {
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube.com/embed/${this.dataset.videoId}?autoplay=1`;
    iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope';
    iframe.allowFullscreen = true;
    this.replaceWith(iframe);
  });
});
</script>
```

### Resource Hints Pattern

```html
<head>
  <!-- DNS prefetch for third-party domains -->
  <link rel="dns-prefetch" href="//fonts.googleapis.com">
  <link rel="dns-prefetch" href="//www.google-analytics.com">

  <!-- Preconnect for critical third-party (includes TLS handshake) -->
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Preload critical assets -->
  <link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/critical.js" as="script">

  <!-- Prefetch next page (on hover/likely navigation) -->
  <link rel="prefetch" href="/next-page.html">
</head>
```

### Meta Tags Template

```html
<head>
  <!-- Basic Meta -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Site Name (50-60 chars)</title>
  <meta name="description" content="Page description with keywords (150-160 chars)">
  <link rel="canonical" href="https://example.com/page">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Site Name">
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="Description for social sharing">
  <meta property="og:image" content="https://example.com/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="https://example.com/page">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@username">
  <meta name="twitter:title" content="Page Title">
  <meta name="twitter:description" content="Description for Twitter">
  <meta name="twitter:image" content="https://example.com/twitter-image.jpg">
</head>
```

### JSON-LD Structured Data Patterns

```html
<!-- Organization -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/company"
  ]
}
</script>

<!-- Breadcrumb -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com"},
    {"@type": "ListItem", "position": 2, "name": "Category", "item": "https://example.com/category"},
    {"@type": "ListItem", "position": 3, "name": "Page"}
  ]
}
</script>

<!-- Article -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {"@type": "Person", "name": "Author Name"},
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "image": "https://example.com/article-image.jpg"
}
</script>
```

### Code Splitting Pattern (React)

```jsx
import { lazy, Suspense } from 'react';

// Lazy load heavy components
const HeavyComponent = lazy(() => import('./HeavyComponent'));
const Chart = lazy(() => import('./Chart'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}

// Route-based code splitting
const routes = [
  { path: '/', component: lazy(() => import('./pages/Home')) },
  { path: '/dashboard', component: lazy(() => import('./pages/Dashboard')) },
];
```

### Service Worker Caching Strategy

```javascript
// Cache-first for static assets
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image' ||
      event.request.destination === 'style' ||
      event.request.destination === 'script') {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          const clone = response.clone();
          caches.open('static-v1').then((cache) => cache.put(event.request, clone));
          return response;
        });
      })
    );
  }
});
```
