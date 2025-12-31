# Phase 6: Frontend Security

**Purpose:** Audit client-side security and browser-based vulnerabilities.

## Objectives

1. Check XSS prevention
2. Review sensitive data handling
3. Analyze build security
4. Verify CSP and security headers

## Key Checks

### XSS Prevention
- [ ] Output encoding used consistently
- [ ] No dangerous `innerHTML` or `dangerouslySetInnerHTML`
- [ ] URLs validated before use
- [ ] User content sanitized
- [ ] Template escaping enabled

### Sensitive Data Handling
- [ ] No sensitive data in localStorage
- [ ] Tokens handled securely
- [ ] Autocomplete disabled for sensitive fields
- [ ] No secrets in client-side code

### Build Security
- [ ] Source maps disabled in production
- [ ] No secrets in bundle
- [ ] Dependencies audited
- [ ] Dead code eliminated

### Security Headers & CSP
- [ ] Content-Security-Policy configured
- [ ] X-Frame-Options set
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy configured

### Air-Gap Considerations
- [ ] No external resources (CDNs, fonts)
- [ ] No analytics/telemetry
- [ ] All assets bundled locally

## Patterns to Search

```javascript
// XSS vulnerabilities
innerHTML = userInput
dangerouslySetInnerHTML={{__html: data}}
document.write(userInput)
eval(userInput)

// Data exposure
localStorage.setItem('token', token)
console.log(password)
window.API_KEY = "..."

// Good patterns
textContent = userInput
DOMPurify.sanitize(html)
```

## Framework-Specific Checks

### React
- [ ] No `dangerouslySetInnerHTML` with user input
- [ ] Props validated
- [ ] useEffect dependencies correct

### Vue
- [ ] No `v-html` with user input
- [ ] Props validated

### Angular
- [ ] No `bypassSecurityTrust*` methods misused
- [ ] Template injection prevented

## Output

### Finding Format
```markdown
### [FE-###] Finding Title
**Severity:** Critical/High/Medium/Low
**OWASP:** A03:2021 - Injection (XSS)
**CWE:** CWE-79
**Location:** file:line
**Issue:** [Description]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Framework:** [React/Vue/Angular/etc.]
2. **XSS Status:** [Protected/Vulnerable areas]
3. **Data Storage:** [What's stored client-side]
4. **CSP:** [Implemented/Missing]
5. **External Dependencies:** [CDNs, scripts]

---

*For detailed guidance, see `../core-phases/phase-06-frontend.md`*
