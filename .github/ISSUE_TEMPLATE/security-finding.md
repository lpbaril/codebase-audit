---
name: Security Finding
about: Document a security vulnerability discovered during audit
title: '[PHASE-###] '
labels: security, audit-finding
assignees: ''
---

## Finding Classification

**Finding ID:** <!-- e.g., AUTH-001, API-003 -->
**Phase:** <!-- e.g., Phase 1 - Authentication -->
**Severity:** <!-- Critical / High / Medium / Low / Informational -->

---

## Summary

<!-- One or two sentence description of the vulnerability -->

---

## Technical Details

### Affected Component(s)
- **File(s):** `path/to/file.ts:line_number`
- **Function/Class:** 
- **Endpoint:** <!-- If applicable -->

### Description
<!-- Detailed technical explanation -->

### Vulnerable Code
```
// Paste relevant code snippet
```

---

## Exploitation

### Prerequisites
<!-- What does an attacker need? -->

### Steps to Reproduce
1. 
2. 
3. 

### Proof of Concept
```bash
# Command or request demonstrating the issue
```

---

## Impact

- **Confidentiality:** <!-- None / Low / Medium / High -->
- **Integrity:** <!-- None / Low / Medium / High -->
- **Availability:** <!-- None / Low / Medium / High -->

### Business Impact
<!-- Description of business consequences -->

---

## Recommendation

### Fix
<!-- How to remediate -->

### Secure Code Example
```
// Example fix
```

### Effort Estimate
<!-- Quick Fix / Moderate / Significant -->

---

## References

- CWE: <!-- CWE-XXX -->
- OWASP: <!-- Reference if applicable -->

---

## Checklist

- [ ] Finding verified
- [ ] Severity confirmed
- [ ] Fix implemented
- [ ] Fix tested
- [ ] Regression tests added
