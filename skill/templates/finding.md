# Finding Template

## Quick Format

```markdown
### [PHASE-###] Title

| Field | Value |
|-------|-------|
| **ID** | PHASE-### |
| **Severity** | Critical / High / Medium / Low / Info |
| **Phase** | Phase # - Name |
| **Status** | Open / In Progress / Resolved / Accepted Risk |
| **OWASP** | A##:2021 - Name |
| **CWE** | CWE-### |

**Location:** `path/to/file.ext:line`

**Description:**
Brief description of the vulnerability.

**Impact:**
What could an attacker do with this vulnerability?

**Evidence:**
```
Code snippet or request/response showing the issue
```

**Recommendation:**
How to fix this issue.

**Secure Code Example:**
```
Fixed code example
```
```

## Detailed Format

```markdown
# [PHASE-###] Vulnerability Title

## Classification

| Field | Value |
|-------|-------|
| **Finding ID** | PHASE-### |
| **Phase** | Phase # - Name |
| **Severity** | Critical / High / Medium / Low / Info |
| **CVSS Score** | #.# |
| **CWE** | CWE-### - Name |
| **OWASP Top 10** | A##:2021 - Name |
| **Status** | Open / In Progress / Resolved / Accepted Risk |

## Affected Component

| Field | Value |
|-------|-------|
| **File** | `path/to/file.ext` |
| **Line** | ### |
| **Function/Method** | functionName() |
| **Endpoint** | GET /api/endpoint |

## Description

[Detailed description of the vulnerability]

## Technical Details

### Vulnerable Code

```language
// Vulnerable code snippet
```

### Attack Vector

[How an attacker could exploit this]

### Proof of Concept

```http
POST /api/vulnerable HTTP/1.1
Host: example.com
Content-Type: application/json

{"payload": "..."}
```

## Impact Assessment

| Category | Impact |
|----------|--------|
| Confidentiality | High / Medium / Low / None |
| Integrity | High / Medium / Low / None |
| Availability | High / Medium / Low / None |

## Remediation

### Short-term Fix

[Immediate mitigation steps]

### Long-term Fix

[Permanent solution]

### Secure Code Example

```language
// Fixed code
```

## References

- [Link to documentation]
- [Link to OWASP]
- [Link to CWE]

## Audit Notes

- **Discovered:** YYYY-MM-DD
- **Verified:** Yes / No
- **Exploited:** Yes / No (in test environment)
```

## Severity Guidelines

| Severity | Criteria |
|----------|----------|
| Critical | RCE, auth bypass, mass data leak, immediate exploitation |
| High | Significant data exposure, privilege escalation, stored XSS |
| Medium | Limited data exposure, reflected XSS, CSRF on important functions |
| Low | Information disclosure, minor security weakness |
| Info | Best practice, hardening recommendation |
