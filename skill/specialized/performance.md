# Frontend Performance Audit

**Focus:** Core Web Vitals, SEO, Assets, Third-Party Scripts
**Type:** Non-security audit

## Core Web Vitals

### LCP (Largest Contentful Paint)
- [ ] Target: < 2.5 seconds
- [ ] Optimize largest element loading
- [ ] Preload critical resources
- [ ] Use CDN for assets

### CLS (Cumulative Layout Shift)
- [ ] Target: < 0.1
- [ ] Set dimensions on images/videos
- [ ] Reserve space for dynamic content
- [ ] Avoid inserting content above existing

### INP (Interaction to Next Paint)
- [ ] Target: < 200ms
- [ ] Minimize main thread work
- [ ] Break up long tasks
- [ ] Use web workers for heavy computation

### FID (First Input Delay)
- [ ] Target: < 100ms
- [ ] Reduce JavaScript execution time
- [ ] Defer non-critical scripts

### TTFB (Time to First Byte)
- [ ] Target: < 800ms
- [ ] Optimize server response time
- [ ] Use edge caching

## SEO Checks

- [ ] Meta titles and descriptions
- [ ] Open Graph tags
- [ ] Twitter Card tags
- [ ] Structured data (JSON-LD)
- [ ] Canonical URLs
- [ ] Sitemap.xml present
- [ ] Robots.txt configured
- [ ] Mobile-friendly (viewport)
- [ ] Semantic HTML (h1, h2, etc.)

## Asset Optimization

### Images
- [ ] Modern formats (WebP, AVIF)
- [ ] Lazy loading implemented
- [ ] Responsive images (srcset)
- [ ] Proper dimensions set

### CSS
- [ ] Critical CSS inlined
- [ ] Non-critical CSS deferred
- [ ] Minified
- [ ] Unused CSS removed

### JavaScript
- [ ] Code splitting
- [ ] Tree shaking
- [ ] Minified
- [ ] Deferred/async loading

### Fonts
- [ ] font-display: swap
- [ ] Preloaded critical fonts
- [ ] Subset fonts
- [ ] WOFF2 format

### Caching
- [ ] Cache-Control headers
- [ ] ETags configured
- [ ] Service worker (if applicable)

### Compression
- [ ] Brotli enabled
- [ ] Gzip fallback

## Third-Party Scripts

- [ ] Scripts inventoried
- [ ] Loaded async/defer
- [ ] Performance impact measured
- [ ] Facades for heavy embeds
- [ ] CSP configured

## Tools

```bash
# Lighthouse CLI
npx lighthouse https://example.com --view

# WebPageTest
# https://www.webpagetest.org

# Bundle analyzer
npx webpack-bundle-analyzer stats.json
npx source-map-explorer build/static/js/*.js
```

## Finding Format
```markdown
### [PERF-###] Title
**Category:** CWV/SEO/Assets/Third-Party
**Metric:** [LCP/CLS/INP/etc.]
**Current Value:** [Measured value]
**Target:** [Target value]
**Recommendation:** [Fix]
```

---

*Full guide: `../specialized/frontend-performance-audit.md`*
