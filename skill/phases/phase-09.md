# Phase 9: Logging & Monitoring

**Purpose:** Audit logging practices and monitoring coverage.

## Objectives

1. Review security event logging
2. Check log data protection
3. Analyze alerting configuration
4. Verify audit trail completeness

## Key Checks

### Event Coverage
- [ ] Authentication events logged
- [ ] Authorization failures logged
- [ ] Sensitive data access logged
- [ ] Admin actions logged
- [ ] Configuration changes logged
- [ ] Error conditions logged

### Log Security
- [ ] No sensitive data in logs
- [ ] Logs tamper-resistant
- [ ] Log access controlled
- [ ] Log rotation configured
- [ ] Centralized logging used

### Alerting
- [ ] Critical events trigger alerts
- [ ] Alert thresholds appropriate
- [ ] Escalation defined
- [ ] On-call rotation exists

### Audit Trail
- [ ] Actions attributable to users
- [ ] Timestamps accurate
- [ ] Logs retained appropriately
- [ ] Logs searchable

## What Should Be Logged

| Event | Required Fields |
|-------|-----------------|
| Login success | userId, IP, timestamp, method |
| Login failure | attemptedUser, IP, timestamp, reason |
| AuthZ failure | userId, resource, action, timestamp |
| Data access | userId, dataType, action, timestamp |
| Admin action | userId, action, target, timestamp |
| Config change | userId, setting, oldValue, newValue |

## Patterns to Search

```javascript
// Dangerous patterns
console.log(`Password: ${password}`)
logger.info(JSON.stringify(req.body))  // May include secrets
logger.debug(user)  // May include PII

// Good patterns
logger.info('User logged in', { userId, ip })
logger.warn('Access denied', { userId, resource })
```

## Air-Gap Considerations

- [ ] Logging works offline
- [ ] No external logging services required
- [ ] Local log aggregation available
- [ ] Alerting works internally

## Output

### Finding Format
```markdown
### [LOG-###] Finding Title
**Severity:** Medium/Low
**OWASP:** A09:2021 - Security Logging and Monitoring Failures
**CWE:** CWE-778 (Insufficient Logging)
**Location:** file:line
**Issue:** [Description]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Logging Framework:** [Winston/Pino/etc.]
2. **Log Destination:** [File/CloudWatch/ELK]
3. **Events Covered:** [Auth/AuthZ/Data/Admin]
4. **Sensitive Data in Logs:** [Yes/No]
5. **Alerting Status:** [Configured/Missing]

---

*For detailed guidance, see `../core-phases/phase-09-logging-monitoring.md`*
