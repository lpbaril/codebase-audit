# Compliance Mapping Guide

This guide maps audit phases and findings to common compliance frameworks, enabling compliance-aware security audits and reporting.

---

## How to Use This Guide

1. **Identify your compliance requirements** before starting the audit
2. **Use the mappings** to prioritize phases relevant to your compliance needs
3. **Tag findings** with compliance references during the audit
4. **Generate compliance-specific reports** using the templates below

---

## OWASP Top 10 (2021) Mapping

| OWASP ID | Vulnerability | Primary Phase | Additional Phases | Severity Guide |
|----------|---------------|---------------|-------------------|----------------|
| **A01:2021** | Broken Access Control | Phase 2 (Authorization) | Phases 3, 4, 11 | Critical/High |
| **A02:2021** | Cryptographic Failures | Phase 5 (Data Layer) | Phases 1, 8, 3 | Critical/High |
| **A03:2021** | Injection | Phase 3 (API Security) | Phases 5, 6 | Critical |
| **A04:2021** | Insecure Design | Phase 4 (Business Logic) | Phase 0, 11 | High/Medium |
| **A05:2021** | Security Misconfiguration | Phase 7 (Infrastructure) | Phases 3, 8, 9 | High/Medium |
| **A06:2021** | Vulnerable Components | Phase 0 (Reconnaissance) | Phase 7 | High/Medium |
| **A07:2021** | Auth Failures | Phase 1 (Authentication) | Phase 2 | Critical/High |
| **A08:2021** | Software/Data Integrity | Phase 7 (Infrastructure) | Phase 11 | High |
| **A09:2021** | Logging Failures | Phase 9 (Logging) | Phase 10 | Medium |
| **A10:2021** | SSRF | Phase 3 (API Security) | Phase 11 | High |

### OWASP Finding Tag Format
```markdown
**OWASP Top 10:** A03:2021 - Injection
```

---

## SOC 2 Trust Service Criteria Mapping

### Security (Common Criteria)

| Criteria | Description | Audit Phases | Key Checks |
|----------|-------------|--------------|------------|
| **CC6.1** | Logical and Physical Access Controls | Phases 1, 2 | Authentication mechanisms, access control lists |
| **CC6.2** | Registration and Authorization | Phase 1 | User provisioning, role assignment |
| **CC6.3** | Removal of Access | Phase 2 | Deprovisioning, access revocation |
| **CC6.6** | Security Against External Threats | Phases 3, 6, 7 | Input validation, WAF, network security |
| **CC6.7** | Data Transmission Protection | Phases 3, 5 | TLS/SSL, encryption in transit |
| **CC6.8** | Prevention of Malicious Software | Phase 7 | Dependency scanning, container security |
| **CC7.1** | Detection Monitoring | Phase 9 | Logging, monitoring, alerting |
| **CC7.2** | Anomaly Detection | Phase 9 | Security event monitoring, SIEM |
| **CC7.3** | Incident Evaluation | Phase 10 | Error handling, incident classification |
| **CC7.4** | Incident Response | Phase 10 | Response procedures, notification |
| **CC7.5** | Recovery from Incidents | Phases 7, 10 | Backup, disaster recovery |

### Availability

| Criteria | Description | Audit Phases | Key Checks |
|----------|-------------|--------------|------------|
| **A1.1** | Capacity Planning | Phase 7 | Resource limits, scaling policies |
| **A1.2** | Environmental Protection | Phase 7 | Infrastructure redundancy |

### Confidentiality

| Criteria | Description | Audit Phases | Key Checks |
|----------|-------------|--------------|------------|
| **C1.1** | Confidential Information Identification | Phase 5 | Data classification |
| **C1.2** | Confidential Information Disposal | Phase 5 | Data retention, secure deletion |

### SOC 2 Finding Tag Format
```markdown
**SOC 2 Criteria:** CC6.6 - Security Against External Threats
```

---

## GDPR (General Data Protection Regulation) Mapping

### Article 32 - Security of Processing

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **32(1)(a)** | Pseudonymization and Encryption | Phase 5 | Data encryption, anonymization |
| **32(1)(b)** | Confidentiality | Phases 1, 2, 8 | Access control, secrets management |
| **32(1)(b)** | Integrity | Phases 5, 11 | Data validation, checksums |
| **32(1)(b)** | Availability | Phases 7, 10 | Redundancy, failover |
| **32(1)(b)** | Resilience | Phases 7, 10 | DDoS protection, circuit breakers |
| **32(1)(c)** | Restore Access | Phase 7 | Backup and recovery |
| **32(1)(d)** | Testing & Assessment | All Phases | Regular security audits |

### Article 25 - Data Protection by Design

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **25(1)** | Privacy by Design | Phase 0, 4 | Data minimization in architecture |
| **25(2)** | Privacy by Default | Phase 5 | Default privacy settings |

### Article 33/34 - Breach Notification

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **33** | Breach Detection | Phase 9 | Logging, monitoring |
| **34** | Data Subject Notification | Phase 10 | Incident response procedures |

### GDPR Finding Tag Format
```markdown
**GDPR Article:** Article 32(1)(a) - Encryption
```

---

## PCI-DSS v4.0 Mapping

### Requirement 1: Network Security Controls

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **1.2** | Network Security Controls | Phase 7 | Firewall rules, network segmentation |
| **1.3** | Network Access Controls | Phase 7, 2 | Access control lists |
| **1.4** | Public-Facing Systems | Phase 3, 7 | DMZ, WAF |

### Requirement 2: Secure Configurations

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **2.2** | System Hardening | Phase 7 | Baseline configurations |
| **2.3** | Wireless Security | Phase 7 | N/A for most cloud apps |

### Requirement 3: Protect Stored Account Data

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **3.1** | Data Retention | Phase 5 | Data lifecycle, purging |
| **3.4** | Render PAN Unreadable | Phase 5 | Encryption, tokenization |
| **3.5** | Protect Cryptographic Keys | Phase 8 | Key management |

### Requirement 4: Protect Data in Transit

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **4.1** | Strong Cryptography | Phases 3, 5 | TLS 1.2+, certificate validation |
| **4.2** | Secure Transmission | Phase 3 | No cleartext transmission |

### Requirement 6: Develop Secure Systems

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **6.2** | Security Patches | Phase 0, 7 | Dependency updates |
| **6.3** | Secure Development | Phases 3, 4, 5, 6 | Secure coding practices |
| **6.4** | Change Control | Phase 7 | CI/CD security |
| **6.5** | Common Vulnerabilities | Phases 3, 5, 6 | OWASP Top 10 |

### Requirement 7: Restrict Access

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **7.1** | Access Control Policy | Phase 2 | RBAC, least privilege |
| **7.2** | Access Management | Phases 1, 2 | User provisioning |

### Requirement 8: Identify Users

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **8.2** | User Identification | Phase 1 | Unique IDs |
| **8.3** | Strong Authentication | Phase 1 | MFA, password policies |
| **8.6** | Application/System Accounts | Phase 8 | Service accounts |

### Requirement 10: Logging and Monitoring

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **10.1** | Audit Trail | Phase 9 | Comprehensive logging |
| **10.2** | Audit Events | Phase 9 | Security event logging |
| **10.3** | Log Protection | Phase 9 | Log integrity |
| **10.4** | Log Review | Phase 9 | Monitoring, alerting |

### Requirement 11: Regular Testing

| Requirement | Description | Audit Phases | Key Checks |
|-------------|-------------|--------------|------------|
| **11.3** | Vulnerability Scanning | All Phases | Regular security audits |
| **11.4** | Penetration Testing | All Phases | Pentesting |

### PCI-DSS Finding Tag Format
```markdown
**PCI-DSS v4.0:** Requirement 3.4 - Render PAN Unreadable
```

---

## HIPAA Security Rule Mapping

### Administrative Safeguards (164.308)

| Standard | Description | Audit Phases | Key Checks |
|----------|-------------|--------------|------------|
| **164.308(a)(1)** | Security Management | All Phases | Risk analysis |
| **164.308(a)(3)** | Workforce Security | Phase 2 | Access authorization |
| **164.308(a)(4)** | Information Access | Phase 2 | Access controls |
| **164.308(a)(5)** | Security Awareness | Phase 9 | Audit controls |
| **164.308(a)(6)** | Incident Procedures | Phase 10 | Incident response |
| **164.308(a)(7)** | Contingency Plan | Phases 7, 10 | Backup, DR |

### Physical Safeguards (164.310)

| Standard | Description | Audit Phases | Key Checks |
|----------|-------------|--------------|------------|
| **164.310(d)** | Device and Media Controls | Phase 5 | Data disposal |

### Technical Safeguards (164.312)

| Standard | Description | Audit Phases | Key Checks |
|----------|-------------|--------------|------------|
| **164.312(a)(1)** | Access Control | Phases 1, 2 | Unique user ID, emergency access |
| **164.312(b)** | Audit Controls | Phase 9 | Activity logging |
| **164.312(c)(1)** | Integrity | Phase 5 | Data integrity controls |
| **164.312(d)** | Authentication | Phase 1 | User authentication |
| **164.312(e)(1)** | Transmission Security | Phases 3, 5 | Encryption in transit |

### HIPAA Finding Tag Format
```markdown
**HIPAA:** 164.312(e)(1) - Transmission Security
```

---

## ISO 27001:2022 Mapping

### Annex A Controls

| Control | Description | Audit Phases | Key Checks |
|---------|-------------|--------------|------------|
| **A.5.15** | Access Control | Phases 1, 2 | Access management |
| **A.5.17** | Authentication | Phase 1 | Authentication mechanisms |
| **A.5.18** | Access Rights | Phase 2 | Privilege management |
| **A.8.2** | Privileged Access | Phase 2 | Admin access |
| **A.8.3** | Information Access Restriction | Phase 2 | Need-to-know |
| **A.8.4** | Access to Source Code | Phase 8 | Code access control |
| **A.8.5** | Secure Authentication | Phase 1 | MFA, password policies |
| **A.8.9** | Configuration Management | Phase 7 | Baseline configs |
| **A.8.10** | Information Deletion | Phase 5 | Data disposal |
| **A.8.12** | Data Leakage Prevention | Phase 5 | DLP controls |
| **A.8.16** | Monitoring | Phase 9 | Activity monitoring |
| **A.8.24** | Use of Cryptography | Phases 5, 8 | Encryption |
| **A.8.25** | Secure Development | Phases 3, 4, 5, 6 | SDLC |
| **A.8.26** | Application Security | Phases 3, 4, 5, 6 | AppSec |
| **A.8.28** | Secure Coding | Phases 3, 6 | Coding standards |

### ISO 27001 Finding Tag Format
```markdown
**ISO 27001:2022:** A.8.5 - Secure Authentication
```

---

## Compliance Report Template

Use this template to generate compliance-specific reports:

```markdown
# [Compliance Framework] Audit Report

## Executive Summary
- **Audit Date:** [Date]
- **Scope:** [Application/System name]
- **Compliance Framework:** [SOC 2 / HIPAA / PCI-DSS / GDPR / ISO 27001]
- **Overall Compliance Status:** [Compliant / Partially Compliant / Non-Compliant]

## Compliance Summary

| Requirement | Status | Findings | Remediation Status |
|-------------|--------|----------|-------------------|
| [Requirement ID] | Pass/Fail/N/A | [Count] | [Pending/In Progress/Complete] |

## Detailed Findings by Compliance Requirement

### [Requirement ID]: [Requirement Name]

**Status:** Pass / Fail / Partial

**Related Security Findings:**
- [Finding ID]: [Brief description]

**Evidence:**
[Documentation or screenshots]

**Remediation Required:**
[Yes/No - if yes, describe]

## Remediation Roadmap

| Priority | Finding | Compliance Impact | Remediation | Due Date |
|----------|---------|-------------------|-------------|----------|
| Critical | [ID] | [Requirement] | [Action] | [Date] |

## Appendix

### A. Compliance Control Mapping
[Full mapping of audit findings to compliance controls]

### B. Supporting Evidence
[List of documentation and evidence collected]
```

---

## Quick Reference: Phase to Compliance Mapping

| Phase | SOC 2 | GDPR | PCI-DSS | HIPAA | ISO 27001 |
|-------|-------|------|---------|-------|-----------|
| 0 - Reconnaissance | CC6.8 | Art. 25 | 6.2 | 164.308(a)(1) | A.8.9 |
| 1 - Authentication | CC6.1, CC6.2 | Art. 32(1)(b) | 8.2, 8.3 | 164.312(d) | A.5.17, A.8.5 |
| 2 - Authorization | CC6.1, CC6.3 | Art. 32(1)(b) | 7.1, 7.2 | 164.308(a)(4) | A.5.15, A.5.18 |
| 3 - API Security | CC6.6, CC6.7 | Art. 32(1)(a) | 4.1, 6.5 | 164.312(e)(1) | A.8.26, A.8.28 |
| 4 - Business Logic | CC6.6 | Art. 25 | 6.3 | 164.308(a)(1) | A.8.25 |
| 5 - Data Layer | CC6.7, C1.1 | Art. 32(1)(a) | 3.1, 3.4 | 164.312(c)(1) | A.8.10, A.8.24 |
| 6 - Frontend | CC6.6 | Art. 32(1)(b) | 6.5 | 164.312(e)(1) | A.8.26 |
| 7 - Infrastructure | CC6.6, A1.1 | Art. 32(1)(b-d) | 1.2, 2.2 | 164.308(a)(7) | A.8.9 |
| 8 - Secrets | CC6.1 | Art. 32(1)(b) | 3.5 | 164.312(a)(1) | A.8.4, A.8.24 |
| 9 - Logging | CC7.1, CC7.2 | Art. 33 | 10.1-10.4 | 164.312(b) | A.8.16 |
| 10 - Error Handling | CC7.3, CC7.4 | Art. 34 | 10.4 | 164.308(a)(6) | A.8.16 |
| 11 - Cross-Cutting | CC6.6, CC6.7 | Art. 32 | 6.5 | All | All |
| 12 - Synthesis | All | All | All | All | All |

---

## Automated Compliance Tagging

The AI should automatically add compliance tags based on finding type:

| Finding Type | Auto-Tags |
|--------------|-----------|
| SQL Injection | OWASP A03, PCI 6.5, ISO A.8.28 |
| Broken Auth | OWASP A07, SOC2 CC6.1, HIPAA 164.312(d) |
| Sensitive Data Exposure | OWASP A02, PCI 3.4, GDPR Art.32(1)(a) |
| Missing Encryption | OWASP A02, PCI 4.1, HIPAA 164.312(e)(1) |
| Access Control Issues | OWASP A01, SOC2 CC6.1, PCI 7.1 |
| Security Misconfiguration | OWASP A05, PCI 2.2, ISO A.8.9 |
| Logging Failures | OWASP A09, SOC2 CC7.1, PCI 10.1 |
