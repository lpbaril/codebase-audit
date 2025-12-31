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

## Specialized: Frontend Performance (Optional)

### Core Web Vitals
- [ ] LCP (Largest Contentful Paint) < 2.5 seconds
- [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] INP (Interaction to Next Paint) < 200ms
- [ ] FID (First Input Delay) < 100ms
- [ ] TTFB (Time to First Byte) < 800ms

### SEO
- [ ] Meta tags and titles optimized
- [ ] Open Graph and Twitter Cards configured
- [ ] Structured data (JSON-LD) implemented
- [ ] Sitemap and robots.txt present
- [ ] Mobile-friendly design verified

### Assets
- [ ] Images optimized (WebP/AVIF, lazy loading)
- [ ] CSS/JS minified and code-split
- [ ] Fonts optimized (font-display: swap)
- [ ] Caching headers configured
- [ ] Compression (Brotli/Gzip) enabled

### Third-Party Scripts
- [ ] Third-party scripts inventoried
- [ ] Scripts loaded async/defer
- [ ] Performance impact measured
- [ ] CSP (Content Security Policy) configured

---

## Specialized: Mobile Security (Optional)

*Use when auditing iOS, Android, React Native, or Flutter applications*

### Secure Storage
- [ ] Keychain (iOS) / Keystore (Android) for sensitive data
- [ ] No secrets in SharedPreferences/UserDefaults
- [ ] No hardcoded API keys or tokens
- [ ] Encrypted local database

### Mobile Authentication
- [ ] Biometric authentication properly implemented
- [ ] Secure token storage
- [ ] Session timeout on background
- [ ] Device binding / attestation

### Network Security
- [ ] Certificate pinning implemented
- [ ] HTTPS only (no HTTP)
- [ ] App Transport Security (iOS) configured
- [ ] Network Security Config (Android) configured

### Code Protection
- [ ] Obfuscation enabled (ProGuard/R8)
- [ ] Root/jailbreak detection
- [ ] Debugger detection
- [ ] No sensitive logic in JavaScript (React Native)

### Data Leakage Prevention
- [ ] No sensitive data in logs
- [ ] No sensitive data in crash reports
- [ ] Screenshot protection for sensitive screens
- [ ] Clipboard protection
- [ ] Backup exclusion for sensitive data

### Platform-Specific (iOS)
- [ ] Keychain access groups configured
- [ ] Data protection classes used
- [ ] Universal Links validated
- [ ] URL scheme handling secure

### Platform-Specific (Android)
- [ ] Exported components secured (android:exported)
- [ ] Content providers protected
- [ ] Broadcast receivers secured
- [ ] WebView security configured

### Third-Party SDKs
- [ ] SDK permissions reviewed
- [ ] SDK data collection understood
- [ ] SDK vulnerabilities checked

---

## Specialized: AWS Security (Optional)

*Use when auditing AWS-deployed applications*

### IAM Security
- [ ] No root account usage
- [ ] MFA enabled for all users
- [ ] Least privilege policies
- [ ] No wildcard (*) permissions
- [ ] Service roles scoped appropriately
- [ ] No hardcoded credentials

### S3 Security
- [ ] No unintended public buckets
- [ ] Bucket policies restrictive
- [ ] Server-side encryption enabled
- [ ] Versioning enabled for critical buckets
- [ ] Block public access settings enabled

### VPC & Network
- [ ] Security groups least privilege
- [ ] No 0.0.0.0/0 ingress (except LBs)
- [ ] VPC Flow Logs enabled
- [ ] Private subnets for databases
- [ ] Network ACLs configured

### Lambda Security
- [ ] Minimal IAM permissions
- [ ] VPC attached if needed
- [ ] Environment variables encrypted
- [ ] No secrets in code
- [ ] Timeout and memory limits set

### RDS/Database Security
- [ ] Not publicly accessible
- [ ] Encryption at rest enabled
- [ ] Encryption in transit (SSL/TLS)
- [ ] Automated backups enabled
- [ ] Security groups restrictive

### Secrets Management
- [ ] Secrets Manager or Parameter Store used
- [ ] Secrets rotated automatically
- [ ] KMS encryption for secrets

### Logging & Monitoring
- [ ] CloudTrail enabled (all regions)
- [ ] CloudWatch Logs configured
- [ ] GuardDuty enabled
- [ ] Config Rules enabled
- [ ] Alerting configured

### EC2/Compute Security
- [ ] IMDSv2 required (no IMDSv1)
- [ ] Latest AMIs used
- [ ] SSM for access (not SSH keys)
- [ ] EBS encryption enabled

---

## Compliance Quick Reference (Optional)

*Tag findings with relevant compliance frameworks*

### OWASP Top 10 (2021)
- [ ] A01: Broken Access Control → Phase 2
- [ ] A02: Cryptographic Failures → Phase 5
- [ ] A03: Injection → Phase 3
- [ ] A04: Insecure Design → Phase 4
- [ ] A05: Security Misconfiguration → Phase 7
- [ ] A06: Vulnerable Components → Phase 0
- [ ] A07: Auth Failures → Phase 1
- [ ] A08: Software/Data Integrity → Phase 7
- [ ] A09: Logging Failures → Phase 9
- [ ] A10: SSRF → Phase 3

### SOC 2 Trust Services
- [ ] CC6.1: Logical Access → Phases 1, 2
- [ ] CC6.6: External Threats → Phases 3, 6, 7
- [ ] CC6.7: Data Transmission → Phases 3, 5
- [ ] CC7.1: Monitoring → Phase 9
- [ ] CC7.3: Incident Evaluation → Phase 10

### GDPR Article 32
- [ ] Encryption (Art. 32.1.a) → Phase 5
- [ ] Confidentiality (Art. 32.1.b) → Phases 1, 2, 8
- [ ] Integrity (Art. 32.1.b) → Phases 5, 11
- [ ] Availability (Art. 32.1.b) → Phases 7, 10

### PCI-DSS v4.0
- [ ] Req 3: Protect Stored Data → Phase 5
- [ ] Req 4: Encryption in Transit → Phases 3, 5
- [ ] Req 6: Secure Development → Phases 3-6
- [ ] Req 7: Restrict Access → Phase 2
- [ ] Req 8: Strong Auth → Phase 1
- [ ] Req 10: Logging → Phase 9

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
