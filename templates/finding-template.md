# Security Finding Template

Use this template for documenting each security finding during the audit.

---

## Finding Template

```markdown
# [PHASE-###] Finding Title

## Classification

| Attribute | Value |
|-----------|-------|
| **ID** | [PHASE-###] (e.g., AUTH-001, API-003) |
| **Phase** | [Phase number and name] |
| **Severity** | Critical / High / Medium / Low / Informational |
| **CVSS Score** | [If applicable, 0.0 - 10.0] |
| **CWE** | [CWE-XXX: Name] |
| **OWASP** | [OWASP Top 10 Reference if applicable] |
| **Status** | Open / In Progress / Resolved / Accepted Risk |

---

## Summary

[One or two sentence description of the vulnerability]

---

## Technical Details

### Affected Component(s)
- **File(s):** `path/to/file.ts:line_number`
- **Function/Class:** `functionName()` or `ClassName`
- **Endpoint:** `[METHOD] /api/path` (if applicable)

### Description
[Detailed technical explanation of the vulnerability, including:
- What the vulnerability is
- Why it exists
- How it works technically]

### Vulnerable Code
```[language]
// Code snippet showing the vulnerability
// Include enough context to understand the issue
```

---

## Exploitation

### Prerequisites
- [What an attacker needs to exploit this]
- [Access level required]
- [Other conditions]

### Attack Scenario
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Proof of Concept
```bash
# Command or request to demonstrate the vulnerability
curl -X POST $API_URL/endpoint \
  -H "Content-Type: application/json" \
  -d '{"exploit": "payload"}'
```

### Expected vs. Actual Result
- **Expected:** [What should happen if properly secured]
- **Actual:** [What actually happens]

---

## Impact Assessment

### Confidentiality Impact
[None / Low / Medium / High]
[Explanation of data that could be exposed]

### Integrity Impact
[None / Low / Medium / High]
[Explanation of data that could be modified]

### Availability Impact
[None / Low / Medium / High]
[Explanation of how service could be disrupted]

### Business Impact
[Description of business consequences if exploited]

---

## Recommendation

### Short-term Fix
[Immediate mitigation that can be applied quickly]

### Long-term Fix
[Proper remediation approach]

### Secure Code Example
```[language]
// Example of how the code should be written
// to properly address the vulnerability
```

---

## Remediation

### Effort Estimate
Quick Fix (< 1 day) / Moderate (1-3 days) / Significant (> 3 days)

### Testing Required
- [ ] Unit tests for the fix
- [ ] Integration tests
- [ ] Security regression tests
- [ ] Penetration testing

### Verification Steps
1. [How to verify the fix works]
2. [How to verify no regression]

---

## References

- [Link to relevant documentation]
- [Link to CWE entry]
- [Link to similar vulnerabilities/advisories]

---

## Audit Notes

| Date | Action | By |
|------|--------|----|
| YYYY-MM-DD | Finding identified | [Auditor] |
| YYYY-MM-DD | [Update] | [Name] |
```

---

## Quick Finding Format

For less critical findings or during rapid documentation:

```markdown
### [ID] Short Title
**Severity:** Medium | **Location:** `file.ts:42` | **Effort:** Quick Fix

**Issue:** [Brief description]

**Recommendation:** [Brief fix]
```

---

## Severity Guidelines

### Critical
- Direct compromise of admin/root access
- Remote code execution
- Complete bypass of authentication
- Direct access to all sensitive data
- SQL injection with data access

### High
- Significant authorization bypass
- Access to other users' sensitive data
- Stored XSS in sensitive areas
- Privilege escalation
- Hardcoded credentials
- Secrets in logs/code

### Medium
- Information disclosure (non-sensitive)
- Missing security headers
- Reflected XSS
- CSRF on non-critical functions
- Missing rate limiting
- Weak password policy

### Low
- Minor information disclosure
- Best practice violations
- Missing optional security features
- Verbose error messages (non-sensitive)

### Informational
- Code quality observations
- Recommendations for improvement
- Defense-in-depth suggestions

---

## Common CWE References

| Issue Type | CWE |
|------------|-----|
| SQL Injection | CWE-89 |
| Command Injection | CWE-78 |
| XSS | CWE-79 |
| Path Traversal | CWE-22 |
| CSRF | CWE-352 |
| Broken Auth | CWE-287 |
| Broken Access Control | CWE-284 |
| Sensitive Data Exposure | CWE-200 |
| Hardcoded Credentials | CWE-798 |
| Missing Encryption | CWE-311 |
| Insecure Deserialization | CWE-502 |
| Insufficient Logging | CWE-778 |
