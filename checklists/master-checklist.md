# Master Security Audit Checklist

This is a consolidated checklist covering all audit phases. Use this for quick reference and tracking.

---

## Pre-Audit Preparation

- [ ] Scope defined and documented
- [ ] Access to all code repositories granted
- [ ] Access to infrastructure configurations granted
- [ ] Secure workspace for audit established
- [ ] `.audit/` folder created for AI-generated artifacts
- [ ] `audit-context.md` initialized (AI session memory)
- [ ] User decision on `.gitignore` documented (add `.audit/` or not)
- [ ] Stakeholder contacts identified
- [ ] Timeline established

---

## Phase 0: Reconnaissance

### Architecture
- [ ] All components identified
- [ ] Data flows mapped
- [ ] Entry points inventoried
- [ ] Trust boundaries identified

### Dependencies
- [ ] All dependencies listed
- [ ] Known CVEs checked
- [ ] Air-gap compatibility verified

---

## Phase 1: Authentication

### Credentials
- [ ] Strong password hashing (bcrypt/argon2/scrypt)
- [ ] Unique salts per user
- [ ] Password policy enforced
- [ ] Secure password reset flow

### Sessions
- [ ] Cryptographically random tokens
- [ ] Appropriate timeouts (idle and absolute)
- [ ] Session invalidation on logout
- [ ] New session ID on auth state change

### Tokens (if JWT)
- [ ] Algorithm enforced server-side
- [ ] Strong secret/key
- [ ] All claims validated
- [ ] Secure token storage (HttpOnly, Secure)

### Security
- [ ] No default/backdoor accounts
- [ ] Brute force protection
- [ ] No account enumeration
- [ ] MFA implemented (if applicable)

---

## Phase 2: Authorization

### Access Control
- [ ] Consistent authorization model
- [ ] Authorization on all protected routes
- [ ] No IDOR vulnerabilities
- [ ] Horizontal access control enforced
- [ ] Vertical access control enforced

### Privilege Management
- [ ] Cannot self-escalate privileges
- [ ] Role changes properly controlled
- [ ] Service accounts least-privilege

### Configuration
- [ ] Default deny behavior
- [ ] Fail-secure on errors
- [ ] Permission changes immediate

---

## Phase 3: API Security

### Input Validation
- [ ] All inputs validated
- [ ] Schema validation used
- [ ] Length limits enforced
- [ ] Type coercion safe

### Injection Prevention
- [ ] Parameterized queries (SQL)
- [ ] No command injection
- [ ] No template injection

### Output Security
- [ ] No excessive data in responses
- [ ] Errors don't leak info
- [ ] Sensitive fields filtered

### Protection
- [ ] Rate limiting implemented
- [ ] CORS restrictive
- [ ] CSRF protection

---

## Phase 4: Business Logic

### State Management
- [ ] Valid state transitions enforced
- [ ] Race conditions prevented
- [ ] Atomicity maintained

### Business Rules
- [ ] All rules enforced
- [ ] Cannot bypass via ordering
- [ ] Edge cases handled

### Integrity
- [ ] Referential integrity maintained
- [ ] Soft delete properly handled
- [ ] Cascade operations correct

---

## Phase 5: Data Layer

### Query Security
- [ ] All queries parameterized
- [ ] ORM used safely
- [ ] Query limits enforced

### Encryption
- [ ] Sensitive data encrypted at rest
- [ ] Strong encryption algorithm
- [ ] Proper key management

### Access
- [ ] Database credentials secure
- [ ] Minimal privilege DB account
- [ ] Multi-tenancy isolated

### Lifecycle
- [ ] Retention policies implemented
- [ ] Secure deletion
- [ ] Backups encrypted

---

## Phase 6: Frontend

### XSS Prevention
- [ ] Output encoding used
- [ ] No dangerous innerHTML usage
- [ ] URLs validated

### Data Handling
- [ ] Sensitive data not in localStorage
- [ ] Tokens handled securely
- [ ] Autocomplete disabled for sensitive fields

### Build Security
- [ ] Source maps disabled in prod
- [ ] No secrets in bundle
- [ ] Dependencies audited

### Air-Gap
- [ ] No external resources
- [ ] No CDN references
- [ ] No telemetry/analytics

---

## Phase 7: Infrastructure

### Container Security
- [ ] Minimal base images
- [ ] Non-root user
- [ ] Capabilities dropped
- [ ] Read-only filesystem
- [ ] Resource limits set

### Kubernetes (if applicable)
- [ ] RBAC least-privilege
- [ ] Network policies enforced
- [ ] Pod security standards applied
- [ ] Secrets encrypted

### Network
- [ ] Proper segmentation
- [ ] Internal TLS
- [ ] Air-gap enforced

---

## Phase 8: Secrets Management

### Storage
- [ ] No hardcoded secrets
- [ ] Secrets in vault/manager
- [ ] Encryption at rest

### Access
- [ ] Least privilege access
- [ ] Access audited
- [ ] Scoped appropriately

### Lifecycle
- [ ] Rotation capability
- [ ] Rotation documented
- [ ] Emergency rotation tested

---

## Phase 9: Logging & Monitoring

### Event Coverage
- [ ] Auth events logged
- [ ] AuthZ failures logged
- [ ] Sensitive access logged
- [ ] Admin actions logged

### Log Security
- [ ] No sensitive data in logs
- [ ] Logs tamper-resistant
- [ ] Access controlled

### Alerting
- [ ] Critical events trigger alerts
- [ ] Alert thresholds appropriate
- [ ] Escalation defined

---

## Phase 10: Error Handling

### Information Control
- [ ] Stack traces hidden
- [ ] No internal paths exposed
- [ ] No technology fingerprinting

### Fail-Secure
- [ ] Default deny on errors
- [ ] No auth bypass on failure
- [ ] Resources bounded

### Recovery
- [ ] Timeouts configured
- [ ] Circuit breakers present
- [ ] Graceful degradation

---

## Phase 11: Cross-Cutting

### Trust Boundaries
- [ ] All boundaries identified
- [ ] Auth verified at each boundary
- [ ] Input validated at receiving side

### Service Security
- [ ] Service-to-service auth
- [ ] Least privilege between services
- [ ] Context propagated correctly

### Data Flows
- [ ] Sensitive data encrypted in transit
- [ ] No unintended data copies
- [ ] Output properly filtered

---

## Phase 12: Synthesis

### Report
- [ ] All findings documented
- [ ] Severity validated
- [ ] Attack chains identified
- [ ] Root causes analyzed

### Prioritization
- [ ] Immediate fixes identified
- [ ] Roadmap created
- [ ] Quick wins highlighted

### Handoff
- [ ] Executive summary prepared
- [ ] Findings walkthrough done
- [ ] Follow-up scheduled

---

## Air-Gap Compliance Summary

| Requirement | Status |
|-------------|--------|
| No external network calls | ☐ |
| No external runtime dependencies | ☐ |
| Internal CA/certificates | ☐ |
| Internal time sync | ☐ |
| Internal logging | ☐ |
| Offline updates possible | ☐ |
| No telemetry | ☐ |

---

## Audit Sign-Off

| Phase | Completed | Date | Auditor |
|-------|-----------|------|---------|
| 0 - Reconnaissance | ☐ | | |
| 1 - Authentication | ☐ | | |
| 2 - Authorization | ☐ | | |
| 3 - API Security | ☐ | | |
| 4 - Business Logic | ☐ | | |
| 5 - Data Layer | ☐ | | |
| 6 - Frontend | ☐ | | |
| 7 - Infrastructure | ☐ | | |
| 8 - Secrets | ☐ | | |
| 9 - Logging | ☐ | | |
| 10 - Error Handling | ☐ | | |
| 11 - Cross-Cutting | ☐ | | |
| 12 - Synthesis | ☐ | | |

**Final Report Delivered:** ☐  
**Date:** ___________  
**Lead Auditor:** ___________
