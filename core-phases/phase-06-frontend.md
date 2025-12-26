# Phase 6: Frontend Security Audit

## Overview
**Purpose:** Validate client-side security, XSS prevention, data handling  
**Duration:** 1-2 hours  
**Criticality:** HIGH — Frontend handles user input and displays data  
**Output:** XSS vulnerabilities, data exposure, air-gap violations

## Files to Provide
- Frontend application code (React/Vue/Angular/etc.)
- Client-side authentication/session handling
- API client/fetch utilities
- Build and bundler configuration
- Environment variable handling
- Any HTML templates

---

## Prompt

```markdown
# Phase 6: Frontend Security Audit

## Context
[PASTE: Previous Carry-Forward Summaries]

For an air-gapped, sensitive data application, the frontend must not leak data and must properly delegate security to the backend.

## Provided Materials
[PASTE YOUR FRONTEND CODE FILES HERE]

---

## Audit Sections

### 6.1 Cross-Site Scripting (XSS) Analysis

**Output Encoding Review:**

| Location | Output Method | Escaped? | Risk |
|----------|---------------|----------|------|
| | innerHTML | ❌ | Critical |
| | textContent | ✅ | None |
| | {{value}} (React/Vue) | ✅ | Low |
| | dangerouslySetInnerHTML | ❌ | Critical |
| | v-html | ❌ | Critical |
| | [innerHTML] | ❌ | Critical |

**XSS Patterns to Find:**

```javascript
// Dangerous patterns:
element.innerHTML = userInput;
document.write(userInput);
$(element).html(userInput);
eval(userInput);
new Function(userInput);
setTimeout(userInput, 1000);

// React
<div dangerouslySetInnerHTML={{__html: userInput}} />

// Vue
<div v-html="userInput"></div>

// Angular
<div [innerHTML]="userInput"></div>
```

**DOM XSS Sinks:**
| Sink | Usage Found? | Input Source | Sanitized? |
|------|--------------|--------------|------------|
| innerHTML | | | |
| outerHTML | | | |
| document.write | | | |
| eval | | | |
| setTimeout/setInterval | | | |
| location.href | | | |
| location.hash | | | |
| window.open | | | |

**URL Handling:**
- [ ] `javascript:` URLs blocked?
- [ ] `data:` URLs restricted?
- [ ] URL parameters sanitized before display?
- [ ] Redirect URLs validated?

### 6.2 Sensitive Data Handling

**Client-Side Storage Analysis:**

| Storage | What's Stored | Sensitive? | Appropriate? |
|---------|---------------|------------|--------------|
| localStorage | | | |
| sessionStorage | | | |
| Cookies | | | |
| IndexedDB | | | |

**In-Memory Data:**
- [ ] Sensitive data cleared when not needed?
- [ ] Passwords cleared after submission?
- [ ] Tokens cleared on logout?
- [ ] Forms cleared after submission?

**Console/Debug Logging:**
```javascript
// Search for:
console.log(password);
console.log(token);
console.log(user);  // Contains sensitive fields?
```

### 6.3 Authentication Token Handling

**Token Storage:**
| Method | Current | Risk |
|--------|---------|------|
| localStorage | | XSS can steal |
| sessionStorage | | XSS can steal, tab-scoped |
| HttpOnly Cookie | | CSRF risk, secure if flags set |
| Memory only | | Lost on refresh |

**Token Security Checklist:**
- [ ] If using cookies: HttpOnly flag?
- [ ] If using cookies: Secure flag?
- [ ] If using cookies: SameSite attribute?
- [ ] If using localStorage: XSS protected?
- [ ] Token not included in URLs?
- [ ] Token not logged?
- [ ] Token cleared on logout?

### 6.4 Build & Bundle Security

**Build Configuration:**
```javascript
// Check webpack/vite/etc config:
{
  devtool: 'source-map',  // ❌ in production
  mode: 'development',     // ❌ in production
}
```

| Check | Status |
|-------|--------|
| Source maps disabled in production | |
| Console statements removed | |
| Development tools removed | |
| Minification enabled | |
| Environment variables safe | |

**Bundle Analysis:**
- [ ] No secrets in bundled code?
- [ ] No API keys compiled in?
- [ ] No internal URLs exposed?
- [ ] Dependencies audited?

### 6.5 Form Security

**Form Analysis:**
| Form | CSRF Token | Autocomplete Off (sensitive) | Input Validation |
|------|------------|------------------------------|------------------|
| Login | | password field | |
| Registration | | | |
| Settings | | | |
| Payment | | all fields | |

**Input Security:**
- [ ] Client-side validation (UX only)?
- [ ] Server-side validation relied upon?
- [ ] No SQL/NoSQL injection via forms?
- [ ] File upload validated client-side too?

### 6.6 API Communication

**API Client Review:**
| Check | Status |
|-------|--------|
| All requests use HTTPS | |
| Authorization header properly set | |
| Sensitive data not in query strings | |
| Error responses handled securely | |
| Response data not over-trusted | |

**Error Handling:**
```javascript
// Bad patterns:
catch (err) {
  alert(err.message);  // May expose internal details
  console.log(err);    // May log sensitive data
}
```

### 6.7 Air-Gap Compliance

**External Resource Check:**

| Resource Type | External URLs Found | Location |
|---------------|---------------------|----------|
| CDN scripts | | |
| External fonts | | |
| Analytics | | |
| External images | | |
| External APIs | | |
| Update checks | | |

**Search for patterns:**
```javascript
// External URLs
https://cdn.
https://fonts.
https://analytics.
https://api.external.com
googletagmanager
gtag
mixpanel
segment
hotjar
```

**Expected for air-gap:**
- [ ] All assets bundled locally
- [ ] No external script loading
- [ ] No external font loading  
- [ ] No analytics or telemetry
- [ ] No update checks
- [ ] No license validation calls

### 6.8 Content Security Policy

**CSP Analysis (if implemented):**
```
Content-Security-Policy: [current policy]
```

| Directive | Value | Secure? |
|-----------|-------|---------|
| default-src | | |
| script-src | | 'unsafe-inline' or 'unsafe-eval'? |
| style-src | | |
| img-src | | |
| connect-src | | |
| frame-ancestors | | |

### 6.9 Component Security (React/Vue/Angular)

**React-Specific:**
- [ ] `dangerouslySetInnerHTML` usage justified?
- [ ] Refs not exposing DOM manipulation?
- [ ] PropTypes/TypeScript for data validation?

**Vue-Specific:**
- [ ] `v-html` usage justified?
- [ ] Templates not using user input?
- [ ] Computed properties sanitized?

**Angular-Specific:**
- [ ] DomSanitizer used correctly?
- [ ] `[innerHTML]` binding safe?
- [ ] AOT compilation enabled?

---

## Output Format

### Findings

```markdown
### [FE-001] DOM XSS via User Profile Display

**Severity:** High
**CWE:** CWE-79

**Location:**
- File: `src/components/UserProfile.jsx`
- Line: 45

**Vulnerable Code:**
```jsx
<div 
  className="user-bio"
  dangerouslySetInnerHTML={{__html: user.biography}}
/>
```

**Proof of Concept:**
1. Set biography to: `<img src=x onerror=alert(document.cookie)>`
2. View user profile
3. JavaScript executes

**Impact:**
- Session token theft
- Account takeover
- Data exfiltration

**Recommendation:**
```jsx
// Option 1: Use textContent/innerText
<div className="user-bio">{user.biography}</div>

// Option 2: Use sanitizer if HTML needed
import DOMPurify from 'dompurify';
<div 
  dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(user.biography)}}
/>
```
```

---

### Phase 6 Summary

**Frontend Security Score:** [1-10]

| Category | Status |
|----------|--------|
| XSS Prevention | ✅/⚠️/❌ |
| Sensitive Data Handling | ✅/⚠️/❌ |
| Token Security | ✅/⚠️/❌ |
| Build Security | ✅/⚠️/❌ |
| Air-Gap Compliance | ✅/⚠️/❌ |
| CSP | ✅/⚠️/❌ |

---

### Phase 6 Carry-Forward Summary

```markdown
## Frontend Security Assessment
- XSS vulnerabilities: [Count/None]
- Data exposure risks: [List]
- Air-gap violations: [List]

## For Infrastructure Phase
- [CSP implementation needs]
- [Security headers needed]

## For Integration Phase
- [Frontend-backend trust issues]
- [API security reliance]

## Immediate Action Items
1. [XSS fix priority]
2. [Air-gap fix priority]
```
```

---

## Next Phase
→ **Phase 7: Infrastructure as Code Audit**
