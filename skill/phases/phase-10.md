# Phase 10: Error Handling

**Purpose:** Verify secure error handling and failure modes.

## Objectives

1. Check information disclosure in errors
2. Verify fail-secure behavior
3. Review exception handling
4. Analyze recovery mechanisms

## Key Checks

### Information Control
- [ ] Stack traces hidden in production
- [ ] No internal paths exposed
- [ ] No technology fingerprinting
- [ ] Error IDs for support (not details)
- [ ] Consistent error format

### Fail-Secure Behavior
- [ ] Default deny on errors
- [ ] No auth bypass on failure
- [ ] Resources bounded on error
- [ ] Transactions rolled back
- [ ] State remains consistent

### Exception Handling
- [ ] All exceptions caught appropriately
- [ ] No silent failures
- [ ] Errors logged (without sensitive data)
- [ ] User-friendly error messages

### Recovery
- [ ] Timeouts configured
- [ ] Circuit breakers implemented
- [ ] Graceful degradation
- [ ] Retry with backoff

## Patterns to Search

```javascript
// Dangerous patterns
res.send(err.stack)
res.json({ error: err.message, details: err })
catch (e) { /* silent */ }

// Good patterns
res.status(500).json({ error: 'Internal error', id: correlationId })
catch (e) { logger.error(e); throw new AppError('...') }
```

## Error Response Review

Check that error responses do NOT include:
- Stack traces
- Database query details
- Internal file paths
- Server software versions
- Debug information
- SQL error messages

## Fail-Secure Checklist

| Scenario | Expected Behavior |
|----------|-------------------|
| Auth service down | Deny access |
| Database error | Return safe error, log details |
| Rate limit hit | Block request |
| Invalid input | Reject, don't process |
| Timeout | Cancel operation, clean up |

## Output

### Finding Format
```markdown
### [ERR-###] Finding Title
**Severity:** Medium/Low
**OWASP:** A05:2021 - Security Misconfiguration
**CWE:** CWE-209 (Information Exposure Through Error)
**Location:** file:line
**Issue:** [Description]
**Example Error:** [Sanitized example]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Error Handling:** [Centralized/Scattered]
2. **Information Leakage:** [Areas found]
3. **Fail-Secure:** [Implemented/Missing]
4. **Recovery Patterns:** [Circuit breakers/retries]

---

*For detailed guidance, see `../core-phases/phase-10-error-handling.md`*
