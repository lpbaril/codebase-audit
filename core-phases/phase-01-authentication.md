# Phase 1: Authentication System Deep Dive

## Overview
**Purpose:** Validate all identity verification mechanisms  
**Duration:** 1-2 hours  
**Criticality:** CRITICAL — Authentication failures expose entire system  
**Output:** Auth vulnerability findings, session security assessment

## Files to Provide
- Login/logout handlers
- Registration flow
- Password reset/recovery
- Token generation and validation
- Session management code
- OAuth/SSO/SAML integrations
- MFA implementation
- User model/schema
- Auth middleware/decorators
- Auth configuration files

---

## Prompt

```markdown
# Phase 1: Authentication System Deep Dive

## Context
[PASTE: Phase 0 Carry-Forward Summary]

This application handles sensitive corporate secrets on air-gapped infrastructure. Authentication is the first line of defense — failures here expose the entire system.

## Provided Materials
[PASTE YOUR AUTH-RELATED CODE FILES HERE]

---

## Audit Sections

### 1.1 Credential Handling

**Password Storage Analysis:**
- [ ] **Hashing Algorithm:** What algorithm is used?
  - ✅ Acceptable: bcrypt, scrypt, Argon2, PBKDF2 (with sufficient iterations)
  - ❌ Unacceptable: MD5, SHA1, SHA256 (without key stretching), plaintext
  
- [ ] **Salt Implementation:**
  - Unique per user?
  - Sufficient length (≥16 bytes)?
  - Cryptographically random?

- [ ] **Password Policy:**
  - Minimum length enforced? (should be ≥12)
  - Complexity requirements?
  - Common password blocklist?
  - Password history (prevent reuse)?

- [ ] **Credential Transmission:**
  - Always over TLS?
  - No logging of passwords?
  - Credentials cleared from memory after use?

**Password Reset Flow:**
| Check | Status | Notes |
|-------|--------|-------|
| Token cryptographically random | | |
| Token single-use | | |
| Token expires (≤1 hour) | | |
| Old password not required for reset | | |
| Rate limited | | |
| Account lockout on abuse | | |
| Email enumeration prevented | | |

### 1.2 Session Management

**Session Token Security:**
- [ ] **Generation:** 
  - Cryptographically secure random number generator?
  - Sufficient entropy (≥128 bits)?

- [ ] **Storage (Server-side):**
  - Where stored? (Memory/Redis/Database)
  - Encrypted at rest?
  - Indexed for quick lookup?

- [ ] **Storage (Client-side):**
  - HttpOnly flag set?
  - Secure flag set?
  - SameSite attribute (Strict or Lax)?
  - Appropriate expiration?

**Session Lifecycle:**
| Event | Secure Behavior | Current Implementation |
|-------|-----------------|----------------------|
| Login success | New session ID generated | |
| Logout | Session completely destroyed | |
| Privilege change | Session regenerated | |
| Password change | All other sessions invalidated | |
| Inactivity | Session expires (configurable) | |
| Absolute timeout | Session expires regardless of activity | |

**Concurrent Session Handling:**
- Multiple simultaneous logins allowed?
- Can user see active sessions?
- Can user terminate other sessions?
- Maximum session limit?

### 1.3 Multi-Factor Authentication (if implemented)

- [ ] **MFA Enrollment:**
  - Requires password re-confirmation?
  - Backup codes generated securely?
  - Backup codes single-use?
  
- [ ] **MFA Validation:**
  - Timing-safe comparison?
  - Rate limited?
  - Replay protection (TOTP window)?
  - Brute force protection?

- [ ] **MFA Bypass Scenarios:**
  - Any code paths that skip MFA?
  - Recovery flow secure?
  - Admin can reset MFA?
  - Device trust/remember me secure?

### 1.4 Token/JWT Security (if applicable)

**JWT Analysis:**
| Security Check | Expected | Actual |
|----------------|----------|--------|
| Algorithm enforced server-side | HS256/RS256 hardcoded | |
| Algorithm "none" rejected | Always rejected | |
| Secret key strength | ≥256 bits | |
| Key rotation mechanism | Exists | |
| Issuer (iss) validated | Yes | |
| Audience (aud) validated | Yes | |
| Expiration (exp) enforced | Yes | |
| Not-before (nbf) checked | Yes | |
| JWT ID (jti) for revocation | Optional but recommended | |

**Token Storage:**
- Where stored on client? (Cookie vs localStorage)
- If localStorage, XSS risk assessed?
- If cookie, proper flags set?

**Refresh Token Flow:**
| Security Check | Status |
|----------------|--------|
| Refresh tokens are opaque (not JWT) | |
| Refresh tokens rotate on use | |
| Refresh tokens bound to user agent/IP (optional) | |
| Refresh token revocation works | |
| Token family tracking (detect theft) | |

### 1.5 Authentication Bypass Vectors

**Default/Backdoor Credentials:**
Search for:
- Hardcoded usernames/passwords
- Test accounts in production code
- Admin accounts with known credentials
- Development bypass flags

**Authentication State Attacks:**
- [ ] Can protected resources be accessed before auth completes?
- [ ] Race condition in login flow?
- [ ] TOCTOU in credential verification?
- [ ] Authentication state stored client-side and modifiable?

**Error Message Analysis:**
| Scenario | Error Message | Information Leakage? |
|----------|---------------|---------------------|
| Invalid username | | Does it reveal username exists? |
| Invalid password | | Different from invalid username? |
| Account locked | | Reveals account exists? |
| Account disabled | | Reveals account exists? |
| MFA required | | Reveals password was correct? |

### 1.6 Account Security

**Brute Force Protection:**
| Mechanism | Implemented | Configuration |
|-----------|-------------|---------------|
| Rate limiting (per IP) | | |
| Rate limiting (per account) | | |
| Account lockout | | Threshold: |
| Lockout duration | | Duration: |
| Lockout notification | | |
| CAPTCHA after failures | | |
| Progressive delays | | |

**Account Enumeration Prevention:**
- Registration: Same response for existing/new emails?
- Login: Same response for valid/invalid usernames?
- Password reset: Same response regardless of email existence?
- Timing attacks: Response time consistent?

**Account Takeover Paths:**
- [ ] Can attacker change email without verification?
- [ ] Can attacker change password without current password?
- [ ] Are security questions used (weak)?
- [ ] Is phone number used for recovery (SIM swap risk)?

### 1.7 Air-Gap Specific Authentication

**External Dependencies:**
- [ ] No OAuth providers requiring internet?
- [ ] No SAML IdP requiring internet?
- [ ] Certificate validation works offline?
- [ ] No external CAPTCHA services?
- [ ] Time synchronization available? (important for TOTP)

**Offline Considerations:**
- How is time synchronized for TOTP?
- Are there NTP dependencies?
- Certificate revocation checking (CRL/OCSP)?

### 1.8 Privilege Escalation via Authentication

- [ ] Can user register as admin?
- [ ] Role specified in registration request?
- [ ] Can user modify their own role via API?
- [ ] Admin impersonation feature secure?

---

## Vulnerability Scenarios to Test

### Scenario 1: External Attacker (Network Access Only)
- Can they enumerate valid usernames?
- Can they brute force credentials?
- Can they bypass MFA?
- Can they hijack sessions?

### Scenario 2: Low-Privilege User → Admin
- Can they elevate their role?
- Can they access admin auth endpoints?
- Can they forge tokens?

### Scenario 3: Session Hijacking
- If attacker gets session token, what's exposed?
- Can legitimate user detect/terminate hijacked session?
- How long until session expires?

### Scenario 4: Credential Theft
- If password database is stolen, how long to crack?
- Are there other credentials stored insecurely?
- What's the blast radius?

---

## Output Format

### Findings

For each vulnerability found:

```markdown
### [AUTH-001] Finding Title

**Severity:** Critical/High/Medium/Low
**CWE:** CWE-XXX
**OWASP:** ASVS X.X.X

**Location:** 
- File: `path/to/file.py`
- Line: 123-145
- Function: `authenticate_user()`

**Description:**
[Clear explanation of the vulnerability]

**Proof of Concept:**
```code
# Steps or code to reproduce
```

**Exploit Scenario:**
[How an attacker would leverage this in practice]

**Impact:**
- Confidentiality: [High/Medium/Low]
- Integrity: [High/Medium/Low]  
- Availability: [High/Medium/Low]

**Recommendation:**
[Specific fix with code example]

```code
# Remediated code example
```

**References:**
- CWE-XXX: https://cwe.mitre.org/data/definitions/XXX.html
- OWASP: https://...
```

---

### Phase 1 Summary

**Authentication Security Score:** [1-10]

| Category | Status | Critical Issues |
|----------|--------|-----------------|
| Password Storage | ✅/⚠️/❌ | |
| Session Management | ✅/⚠️/❌ | |
| Token Security | ✅/⚠️/❌ | |
| Brute Force Protection | ✅/⚠️/❌ | |
| MFA (if applicable) | ✅/⚠️/❌ | |
| Air-Gap Compliance | ✅/⚠️/❌ | |

**Finding Summary:**
- Critical: X
- High: X
- Medium: X
- Low: X

---

### Phase 1 Carry-Forward Summary

```markdown
## Authentication Assessment
- Overall security: [Strong/Moderate/Weak]
- Session mechanism: [JWT/Cookie-Session/Custom]
- MFA status: [Implemented/Partial/None]

## Key Findings for Authorization Phase
- [Any auth issues that affect authorization]
- [Token claims that carry permissions]
- [Session data available for authz decisions]

## Concerns for Later Phases
- [API endpoints that need auth verification]
- [Data that should be protected by auth]
- [Services that trust auth tokens]

## Immediate Action Items
1. [Critical fix needed]
2. [High priority fix]
```
```

---

## Checklist Before Moving to Phase 2

- [ ] All auth flows analyzed
- [ ] Password storage verified secure
- [ ] Session management reviewed
- [ ] Token security validated
- [ ] Brute force protections checked
- [ ] Account enumeration tested
- [ ] Air-gap compliance verified
- [ ] Findings documented with severity
- [ ] Carry-forward summary prepared

---

## Next Phase
→ **Phase 2: Authorization & Access Control Audit**

Files needed for Phase 2:
- Role/permission definitions
- Authorization middleware/decorators
- Access control policies
- Resource ownership logic
- Admin function implementations
