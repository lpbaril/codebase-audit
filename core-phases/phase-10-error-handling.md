# Phase 10: Error Handling & Failure Modes Security Audit

## Overview
**Purpose:** Ensure secure failure and error handling throughout the system  
**Estimated Time:** 2-3 hours  
**Prerequisites:** Phases 0-9 completed

## Files to Provide

```
□ Error handling middleware
□ Exception handling code
□ Global error handlers
□ Fallback mechanisms
□ Circuit breaker configurations
□ Graceful degradation implementations
□ Health check implementations
□ Retry logic
```

---

## Audit Prompt

```markdown
# Phase 10: Error Handling & Failure Mode Security Audit

## Context
[PASTE: Previous Carry-Forward Summaries from Phases 0-9]

Errors and failures can expose sensitive information or create exploitable conditions. Systems must fail securely - denying access by default and not leaking internal details.

## Environment Details
- **Air-gapped:** Yes - error recovery must work without external resources
- **Sensitivity Level:** Corporate secrets - errors must not expose sensitive data
- **Availability Requirements:** [Specify uptime requirements]

## Provided Materials
[PASTE: Error handling code, exception handlers, fallback logic]

---

## Audit Checklist

### 10.1 Error Information Disclosure

**Check for information leakage in:**

#### API Error Responses
- [ ] Stack traces: Hidden from users in production?
- [ ] Internal file paths: Not exposed in errors?
- [ ] Database details: No SQL errors, table names, or query details?
- [ ] Technology stack: Errors don't reveal frameworks/versions?
- [ ] Configuration details: No config values in errors?

#### Web Interface Errors
- [ ] Generic error pages: No detailed errors shown to users?
- [ ] Client-side errors: Console doesn't log sensitive data?
- [ ] Network errors: Response bodies don't contain secrets?

#### Log-based Disclosure
- [ ] Error logs: Don't contain passwords, tokens, or PII?
- [ ] Debug information: Disabled in production?

**Test with intentional errors:**
```
1. Invalid input → Should get generic "invalid input" not field details
2. Database error → Should get "service error" not SQL details
3. File not found → Should get 404 not file path
4. Auth error → Should get "unauthorized" not "user doesn't exist"
```

### 10.2 Error Handling Consistency

- [ ] **Global error handler:** All unhandled exceptions caught?
- [ ] **Consistent format:** Error response format same across all APIs?
- [ ] **Error codes:** Meaningful to operators, opaque to attackers?
- [ ] **HTTP status codes:** Appropriate codes used (not always 200 or 500)?
- [ ] **Error IDs:** Can correlate user-facing error to logs?

**Error Response Format Assessment:**
```json
// Good: Generic but traceable
{
  "error": "An error occurred processing your request",
  "error_id": "err_abc123",
  "status": 500
}

// Bad: Too much information
{
  "error": "NullPointerException at UserService.java:142",
  "query": "SELECT * FROM users WHERE id = '1; DROP TABLE users'",
  "stack": "..."
}
```

### 10.3 Fail-Secure Behavior

**Authorization Failures:**
- [ ] Unknown user → Deny access (not default allow)
- [ ] Missing permissions → Deny access
- [ ] Authorization service unavailable → Deny access
- [ ] Malformed token → Deny access
- [ ] Expired token → Deny access

**Data Access Failures:**
- [ ] Database unavailable → Return error, not cached/stale data
- [ ] Partial data retrieval → Clear indication, not silent partial response
- [ ] Decryption failure → Deny access to data

**General Principle:**
- [ ] **Default deny:** When in doubt, deny access?
- [ ] **No silent failures:** All failures visible in logs/monitoring?
- [ ] **No security bypass:** Errors don't skip remaining security checks?

### 10.4 Resource Exhaustion Handling

- [ ] **Memory exhaustion:** Graceful handling, not crash with core dump?
- [ ] **Connection pool exhaustion:** Queued or rejected, not hanging?
- [ ] **Disk space full:** Graceful error, critical data protected?
- [ ] **Thread pool exhaustion:** Bounded, with rejection policy?
- [ ] **File descriptor limits:** Handled gracefully?

**Timeout Configuration:**
- [ ] All external calls have timeouts?
- [ ] Database queries have timeouts?
- [ ] HTTP requests have connect and read timeouts?
- [ ] Long operations have overall timeout?

### 10.5 Recovery Security

- [ ] **State recovery:** Recovery doesn't bypass security checks?
- [ ] **Session recovery:** Sessions properly validated on recovery?
- [ ] **Transaction rollback:** Rollbacks maintain data integrity?
- [ ] **Crash recovery:** No sensitive data in crash dumps?
- [ ] **Restart security:** Services require re-authentication?

### 10.6 Denial of Service Resistance

- [ ] **Expensive error paths:** Can attackers trigger resource-intensive errors?
- [ ] **Error rate limiting:** Rapid error generation handled?
- [ ] **Error log flooding:** Can't fill disk with error logs?
- [ ] **Error-triggered retries:** No infinite retry loops?
- [ ] **Cascading failures:** One component failure doesn't crash system?

**DoS via Errors Test Cases:**
```
1. Send malformed input rapidly → System remains responsive
2. Trigger expensive validation errors → Resources bounded
3. Cause repeated auth failures → Account lockout, not system slowdown
4. Generate large error responses → Response size limited
```

### 10.7 Circuit Breakers & Fallbacks

- [ ] **Circuit breakers implemented:** For all external dependencies?
- [ ] **Fallback security:** Fallback paths enforce same security?
- [ ] **Degraded mode security:** What's available when degraded?
- [ ] **Circuit state monitoring:** Can see circuit breaker status?
- [ ] **Recovery testing:** Tested that circuits close properly?

**Circuit Breaker Inventory:**

| Dependency | Circuit Breaker? | Fallback | Security in Fallback |
|------------|------------------|----------|----------------------|
| Database | | | |
| Cache | | | |
| Auth Service | | | |
| Other Services | | | |

### 10.8 Validation Error Handling

- [ ] **Input validation errors:** Don't reveal expected format in detail?
- [ ] **Type coercion errors:** Handled securely?
- [ ] **Boundary errors:** Integer overflow, buffer limits handled?
- [ ] **Encoding errors:** Character encoding issues handled?

### 10.9 Async Error Handling

- [ ] **Promise rejections:** All caught and handled?
- [ ] **Background job failures:** Logged and monitored?
- [ ] **Message queue errors:** Dead letter handling secure?
- [ ] **Webhook failures:** Retry logic doesn't expose data?

### 10.10 Air-Gap Specific

- [ ] **No external error reporting:** No crash reporting to external services?
- [ ] **Internal error aggregation:** Errors aggregated internally?
- [ ] **Offline recovery:** System recovers without internet?
- [ ] **Manual intervention:** Procedures for errors requiring manual fix?

---

## Failure Scenario Testing

Test these scenarios:

| Scenario | Expected Behavior | Security Concern |
|----------|-------------------|------------------|
| Database down | Graceful error, deny data access | Don't serve stale data |
| Auth service down | Deny all access | Don't bypass auth |
| Memory pressure | Shed load, remain stable | Don't expose data in OOM |
| Disk full | Stop writes, alert | Don't corrupt data |
| Invalid input flood | Rate limit, remain stable | Don't DoS via validation |
| Concurrent failures | Isolated failures | Don't cascade |

---

## Output Format

For each finding:
```
### [ERR-###] Finding Title
**Severity:** Critical/High/Medium/Low
**Failure Type:** Information disclosure / Insecure failure / DoS / Recovery issue
**Location:** file:line or component
**Issue:** Description of the vulnerability
**Trigger Condition:** How to cause this error condition
**Security Impact:** What an attacker gains
**Recommendation:** Specific fix with code example
**Effort:** Quick fix / Moderate / Significant
```

---

## Phase 10 Deliverables

1. **Error Handling Maturity Assessment** - Overall error handling quality
2. **Information Disclosure Inventory** - What's leaked in errors
3. **Fail-Secure Gaps** - Where failures don't deny access
4. **DoS Resistance Assessment** - Vulnerability to error-based DoS
5. **Circuit Breaker Map** - Dependencies and their failure handling
6. **Phase 10 Carry-Forward Summary** - Key findings for subsequent phases
```

---

## Carry-Forward Template

```markdown
## Phase 10 Carry-Forward Summary

### Error Handling Architecture
- [Description of error handling approach]

### Information Disclosure Risks
- [What sensitive data might leak via errors]

### Fail-Secure Assessment
- [Does system deny access on failure?]

### DoS Resistance
- [Vulnerability to error-based denial of service]

### Critical Findings
- [List any Critical/High severity issues]

### Recovery Concerns
- [Issues with system recovery after failures]

### Items for Phase 11+ Attention
- [Cross-cutting concerns related to errors]
```

---

## Common Findings Reference

| Finding | Severity | Description |
|---------|----------|-------------|
| Stack traces exposed | High | Full stack traces in API responses |
| SQL errors exposed | High | Database errors shown to users |
| Auth bypass on error | Critical | Authorization skipped when service errors |
| No global error handler | Medium | Unhandled exceptions crash or leak info |
| Missing timeouts | Medium | Calls can hang indefinitely |
| Error log injection | Medium | User input in error messages unsanitized |
| Crash dumps with secrets | High | Memory dumps contain sensitive data |
| No circuit breakers | Medium | Cascading failures possible |
