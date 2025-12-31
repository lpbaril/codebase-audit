# Phase 3: API Security

**Purpose:** Audit all API endpoints for security vulnerabilities.

## Objectives

1. Review input validation and sanitization
2. Check for injection vulnerabilities
3. Analyze output encoding and data exposure
4. Verify rate limiting and CORS configuration

## Key Checks

### Input Validation
- [ ] All inputs validated (type, length, format)
- [ ] Schema validation used (JSON Schema, Zod, etc.)
- [ ] File uploads validated (type, size, content)
- [ ] Content-Type enforced

### Injection Prevention
- [ ] Parameterized queries (SQL, NoSQL)
- [ ] No command injection (shell commands)
- [ ] No template injection (SSTI)
- [ ] No LDAP/XPath injection
- [ ] No header injection

### Output Security
- [ ] No excessive data in responses
- [ ] Sensitive fields filtered (passwords, tokens)
- [ ] Error messages don't leak info
- [ ] Proper Content-Type headers

### API Protection
- [ ] Rate limiting implemented
- [ ] CORS properly configured (not `*`)
- [ ] CSRF protection for state-changing operations
- [ ] API versioning implemented

## Patterns to Search

```javascript
// SQL Injection
query(`SELECT * FROM users WHERE id = ${id}`)
.query("SELECT * FROM " + table)

// Command Injection
exec(userInput)
spawn(command + args)

// Good patterns
query("SELECT * FROM users WHERE id = ?", [id])
execFile(command, [arg1, arg2])
```

## OWASP API Security Top 10

- [ ] API1: Broken Object Level Authorization
- [ ] API2: Broken Authentication
- [ ] API3: Broken Object Property Level Authorization
- [ ] API4: Unrestricted Resource Consumption
- [ ] API5: Broken Function Level Authorization
- [ ] API6: Unrestricted Access to Sensitive Business Flows
- [ ] API7: Server Side Request Forgery
- [ ] API8: Security Misconfiguration
- [ ] API9: Improper Inventory Management
- [ ] API10: Unsafe Consumption of APIs

## Output

### Finding Format
```markdown
### [API-###] Finding Title
**Severity:** Critical/High/Medium/Low
**OWASP:** A03:2021 - Injection
**CWE:** CWE-89 (SQL) / CWE-78 (OS Command)
**Location:** file:line
**Issue:** [Description]
**PoC:** [Request/Response example]
**Recommendation:** [Fix with code example]
```

### Carry-Forward Summary

Document for next phase:
1. **API Endpoints:** [Count and types]
2. **Validation Framework:** [Zod/Joi/Manual/None]
3. **Injection Issues:** [Any SQL/Command/etc.]
4. **Rate Limiting:** [Implemented/Missing]
5. **CORS Config:** [Restrictive/Permissive]

---

*For detailed guidance, see `../core-phases/phase-03-api-security.md`*
