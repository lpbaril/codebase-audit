# Phase 9: Logging, Monitoring & Audit Trail Audit

## Overview
**Purpose:** Ensure security events are captured and tamper-resistant  
**Estimated Time:** 2-3 hours  
**Prerequisites:** Phases 0-8 completed

## Files to Provide

```
□ Logging configuration files
□ Log aggregation setup (ELK, Splunk, etc.)
□ Audit logging implementation code
□ Monitoring/alerting configuration
□ Log retention policies
□ Security event definitions
□ Alert routing configuration
```

---

## Audit Prompt

```markdown
# Phase 9: Logging, Monitoring & Audit Trail Audit

## Context
[PASTE: Previous Carry-Forward Summaries from Phases 0-8]

For sensitive systems, comprehensive logging is essential for detecting incidents and forensic analysis. Audit trails must be tamper-resistant.

## Environment Details
- **Air-gapped:** Yes - logging infrastructure must be internal
- **Sensitivity Level:** Corporate secrets - logs themselves may be sensitive
- **Compliance Requirements:** [Specify any regulatory requirements]

## Provided Materials
[PASTE: Logging code, monitoring configs, audit trail implementation]

---

## Audit Checklist

### 9.1 Security Event Logging

**Verify these events are logged:**

#### Authentication Events
- [ ] Successful logins (who, when, from where)
- [ ] Failed login attempts (including username attempted)
- [ ] Logouts
- [ ] Session timeouts
- [ ] Password changes
- [ ] Password reset requests
- [ ] MFA enrollment/changes
- [ ] Account lockouts

#### Authorization Events
- [ ] Authorization failures (access denied)
- [ ] Privilege escalation attempts
- [ ] Role changes
- [ ] Permission modifications
- [ ] Access to sensitive resources

#### Data Access Events
- [ ] Access to sensitive data
- [ ] Data exports/downloads
- [ ] Bulk data operations
- [ ] Search queries on sensitive data
- [ ] Data modifications (create/update/delete)

#### Administrative Events
- [ ] User creation/deletion
- [ ] Configuration changes
- [ ] System settings modifications
- [ ] Backup operations
- [ ] Restore operations

#### Security Events
- [ ] Input validation failures
- [ ] CSRF token failures
- [ ] Rate limit triggers
- [ ] Unusual error patterns
- [ ] Certificate operations

### 9.2 Log Content Quality

**For each security event, verify logs include:**
- [ ] Timestamp (consistent format, UTC preferred)
- [ ] Event type/category
- [ ] Actor (who performed the action)
- [ ] Action (what was done)
- [ ] Target (what was affected)
- [ ] Outcome (success/failure)
- [ ] Source (IP address, service, component)
- [ ] Correlation ID (to trace across services)
- [ ] Session ID (to group user actions)

**Log Format Assessment:**
```
Example good log entry:
{
  "timestamp": "2024-01-15T10:23:45.123Z",
  "event_type": "authentication.login.success",
  "actor": {"user_id": "u123", "username": "jsmith"},
  "source": {"ip": "10.0.1.50", "user_agent": "..."},
  "session_id": "sess_abc123",
  "correlation_id": "req_xyz789",
  "details": {"auth_method": "password+mfa"}
}
```

### 9.3 Log Security

- [ ] **Sensitive data exclusion:** Passwords, tokens, PII not logged?
- [ ] **Log injection prevention:** User input sanitized before logging?
- [ ] **Integrity protection:** Logs signed, hashed, or write-once?
- [ ] **Access control:** Who can read logs? Who can modify/delete?
- [ ] **Encryption:** Logs encrypted at rest?
- [ ] **Transmission security:** Logs sent over encrypted channels?
- [ ] **Retention enforcement:** Logs deleted per policy? Cannot be deleted early?

### 9.4 Audit Trail Requirements

**Immutability:**
- [ ] Audit logs append-only?
- [ ] Cannot be modified after creation?
- [ ] Deletion requires special privileges and is itself logged?
- [ ] Hash chain or similar for integrity verification?

**Completeness:**
- [ ] All security-relevant actions captured?
- [ ] No gaps in audit trail?
- [ ] Covers all access tiers?

**Non-repudiation:**
- [ ] Can definitively prove who did what?
- [ ] Timestamps from trusted source?
- [ ] Actor identification reliable?

**Forensic Value:**
- [ ] Sufficient detail for incident investigation?
- [ ] Can reconstruct sequence of events?
- [ ] Can identify scope of breach?

### 9.5 Log Aggregation & Storage

- [ ] **Centralized logging:** All components send to central location?
- [ ] **Secure transmission:** TLS for log shipping?
- [ ] **No log loss:** Buffering/retry for network issues?
- [ ] **Storage security:** Log storage access controlled?
- [ ] **Storage capacity:** Sufficient for retention requirements?
- [ ] **Backup:** Logs backed up? Backup access controlled?
- [ ] **Air-gap compliance:** All logging infrastructure internal?

### 9.6 Monitoring & Alerting

**Real-time Alerts Configured For:**
- [ ] Multiple failed login attempts
- [ ] Login from new location/device (if applicable in air-gap)
- [ ] Privilege escalation
- [ ] Access to highly sensitive data
- [ ] Bulk data exports
- [ ] Configuration changes
- [ ] Service health issues
- [ ] Certificate expiration warnings
- [ ] Resource exhaustion

**Alert Configuration:**
- [ ] Appropriate thresholds (not too sensitive, not too loose)?
- [ ] Alert fatigue managed (not too many alerts)?
- [ ] Escalation paths defined?
- [ ] On-call rotation configured?
- [ ] Alert testing performed?

### 9.7 Detection Capabilities

- [ ] **Anomaly detection:** Unusual patterns flagged?
- [ ] **Brute force detection:** Repeated failures detected?
- [ ] **Account abuse:** Unusual account activity detected?
- [ ] **Privilege abuse:** Unusual privileged operations flagged?
- [ ] **Data exfiltration:** Large data access patterns detected?
- [ ] **Time-based anomalies:** Off-hours activity flagged?

### 9.8 Incident Response Support

- [ ] **Log search:** Can quickly search for specific indicators?
- [ ] **Timeline reconstruction:** Can build incident timeline easily?
- [ ] **Correlation:** Can correlate events across systems?
- [ ] **Evidence preservation:** Logs suitable as evidence?
- [ ] **Export capability:** Can export logs for analysis?
- [ ] **Playbook integration:** Logs support incident playbooks?

### 9.9 Air-Gap Specific Considerations

- [ ] **Internal log aggregation:** No external logging services?
- [ ] **Time synchronization:** NTP within air-gap for consistent timestamps?
- [ ] **Log analysis tools:** Available within air-gap?
- [ ] **SIEM:** Security monitoring tools available internally?
- [ ] **Update mechanism:** How are logging tools updated?

---

## Log Coverage Matrix

Create a matrix showing what's logged:

| Event Category | Logged? | Details Level | Alert? | Retention |
|----------------|---------|---------------|--------|-----------|
| Auth - Login Success | | | | |
| Auth - Login Failure | | | | |
| Auth - Logout | | | | |
| AuthZ - Access Denied | | | | |
| AuthZ - Privilege Change | | | | |
| Data - Read Sensitive | | | | |
| Data - Modify | | | | |
| Data - Delete | | | | |
| Data - Export | | | | |
| Admin - User Mgmt | | | | |
| Admin - Config Change | | | | |
| System - Errors | | | | |
| System - Health | | | | |

---

## Output Format

For each finding:
```
### [LOG-###] Finding Title
**Severity:** Critical/High/Medium/Low
**Gap Type:** Missing logging / Insufficient detail / Security risk / Detection gap
**Location:** Configuration file or code location
**Issue:** Description of what's missing or wrong
**Detection Impact:** What attacks/incidents would be missed
**Recommendation:** Specific fix with configuration example
**Effort:** Quick fix / Moderate / Significant
```

---

## Phase 9 Deliverables

1. **Security Event Coverage Matrix** - What's logged vs. what should be
2. **Blind Spots Summary** - Events that aren't being captured
3. **Log Security Assessment** - Are logs themselves secure?
4. **Detection Capability Gaps** - What attacks wouldn't be detected?
5. **Alerting Recommendations** - Alerts that should be added
6. **Phase 9 Carry-Forward Summary** - Key findings for subsequent phases
```

---

## Carry-Forward Template

```markdown
## Phase 9 Carry-Forward Summary

### Logging Architecture
- [Description of how logging works]

### Coverage Assessment
- Events logged: [percentage or list]
- Critical gaps: [list missing event types]

### Security of Logs
- [Assessment of log integrity and access control]

### Detection Capabilities
- [What can/cannot be detected]

### Critical Findings
- [List any Critical/High severity issues]

### Monitoring Gaps
- [What isn't being monitored that should be]

### Items for Phase 10+ Attention
- [Issues affecting error handling or other phases]
```

---

## Common Findings Reference

| Finding | Severity | Description |
|---------|----------|-------------|
| No authentication logging | Critical | Cannot detect unauthorized access |
| Sensitive data in logs | High | Passwords, tokens, or PII logged |
| Logs modifiable | High | Audit trail can be tampered |
| No failed login alerts | High | Brute force attacks undetected |
| Missing correlation IDs | Medium | Cannot trace requests across services |
| No log retention policy | Medium | Logs kept forever or deleted too soon |
| Timestamps inconsistent | Medium | Difficult to reconstruct timelines |
| No privilege change logging | Medium | Cannot detect privilege escalation |
