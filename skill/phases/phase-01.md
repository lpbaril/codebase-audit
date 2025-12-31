# Phase 1: Authentication

**Purpose:** Validate identity verification mechanisms and credential handling.

## Objectives

1. Review password handling and storage
2. Analyze session management
3. Evaluate token security (JWT, OAuth)
4. Check multi-factor authentication implementation

## Key Checks

### Password Security
- [ ] Strong hashing algorithm (bcrypt, argon2, scrypt)
- [ ] Unique salts per user
- [ ] Password policy enforced (length, complexity)
- [ ] Secure password reset flow
- [ ] No password in logs or error messages

### Session Management
- [ ] Cryptographically random session tokens
- [ ] Appropriate timeouts (idle and absolute)
- [ ] Session invalidation on logout
- [ ] New session ID on authentication state change
- [ ] Session stored securely (HttpOnly, Secure flags)

### Token Security (JWT)
- [ ] Algorithm enforced server-side (no `alg: none`)
- [ ] Strong secret key (256+ bits)
- [ ] All claims validated (exp, iss, aud)
- [ ] Token stored securely (not localStorage)
- [ ] Refresh token rotation implemented

### MFA & Security
- [ ] MFA available for sensitive operations
- [ ] No default/backdoor accounts
- [ ] Brute force protection (rate limiting, lockout)
- [ ] No account enumeration (consistent responses)

## Patterns to Search

```javascript
// Dangerous patterns
password.*=.*["']       // Hardcoded passwords
.compare(password       // Direct comparison (not constant-time)
jwt.decode(             // Decoding without verification

// Good patterns
bcrypt.hash(            // Proper hashing
argon2.hash(
jwt.verify(             // Proper verification
```

## Output

### Finding Format
```markdown
### [AUTH-###] Finding Title
**Severity:** Critical/High/Medium/Low
**OWASP:** A07:2021 - Identification and Authentication Failures
**CWE:** CWE-XXX
**Location:** file:line
**Issue:** [Description]
**Recommendation:** [Fix with code example]
```

### Carry-Forward Summary

Document for next phase:
1. **Auth Mechanism:** [Sessions/JWT/OAuth/etc.]
2. **Password Storage:** [Algorithm used]
3. **Session Configuration:** [Timeout, storage]
4. **MFA Status:** [Available/Required/None]
5. **Critical Findings:** [List any Critical/High issues]

---

*For detailed guidance, see `../core-phases/phase-01-authentication.md`*
