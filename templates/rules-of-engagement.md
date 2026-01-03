# Rules of Engagement (RoE) Template

## Pre-Engagement Questionnaire

Complete this document before beginning a security audit to establish scope, boundaries, and expectations.

---

## 1. Engagement Information

| Field | Value |
|-------|-------|
| **Project/Application Name** | |
| **Client/Stakeholder** | |
| **Audit Start Date** | |
| **Audit End Date** | |
| **Auditor(s)** | |
| **Emergency Contact** | |

---

## 2. Scope Definition

### 2.1 In-Scope Assets

| Asset Type | Asset Name/Path | Notes |
|------------|-----------------|-------|
| Repository | | |
| Application | | |
| API Endpoints | | |
| Infrastructure | | |
| Mobile Apps | | |

### 2.2 Out-of-Scope Assets

List any systems, components, or areas explicitly excluded from testing:

| Asset | Reason for Exclusion |
|-------|----------------------|
| | |
| | |

### 2.3 Testing Boundaries

**Code Branches:**
- [ ] Main/Master branch only
- [ ] Specific branch: ________________
- [ ] All branches

**Environments:**
- [ ] Development
- [ ] Staging
- [ ] Production (Caution required)
- [ ] Local only

---

## 3. Authorization & Permissions

### 3.1 Authorization Confirmation

- [ ] I have written authorization to perform this security audit
- [ ] The codebase owner is aware of this audit
- [ ] Relevant stakeholders have been notified

**Authorization Document Reference:** ________________

### 3.2 Access Levels Granted

| Access Type | Granted? | Account/Details |
|-------------|----------|-----------------|
| Source code read access | Yes/No | |
| Database read access | Yes/No | |
| Admin/elevated test account | Yes/No | |
| Infrastructure access | Yes/No | |
| CI/CD pipeline access | Yes/No | |

---

## 4. Testing Restrictions

### 4.1 Prohibited Activities

Check all that apply:

- [ ] **No destructive testing** (DoS, data deletion, resource exhaustion)
- [ ] **No production testing** without explicit approval
- [ ] **No social engineering** of employees
- [ ] **No physical security testing**
- [ ] **No testing outside business hours**
- [ ] **No automated scanning** against production
- [ ] **No exploitation of vulnerabilities** (detection only)

### 4.2 Conditional Activities

Activities requiring explicit approval before execution:

| Activity | Allowed? | Conditions |
|----------|----------|------------|
| Active exploitation testing | Yes/No | |
| Automated vulnerability scanning | Yes/No | |
| Credential testing | Yes/No | |
| Data exfiltration simulation | Yes/No | |
| API fuzzing | Yes/No | |

### 4.3 Data Handling

- [ ] **No real user data** should be accessed or extracted
- [ ] **Test data only** for any data manipulation
- [ ] **PII/PHI handling:** ________________
- [ ] **Secrets discovered:** Report immediately, do not store

---

## 5. Communication Protocol

### 5.1 Finding Disclosure

**Critical/High Severity Findings:**
- [ ] Immediate notification required
- [ ] Notification method: ________________
- [ ] Contact: ________________

**Standard Findings:**
- [ ] Include in final report
- [ ] Weekly summary updates
- [ ] Other: ________________

### 5.2 Escalation Path

| Severity | Response Time | Escalation Contact |
|----------|---------------|-------------------|
| Critical | Immediate | |
| High | Within 24 hours | |
| Medium | End of audit | |
| Low/Info | End of audit | |

### 5.3 Status Updates

- [ ] Daily standup
- [ ] Weekly summary
- [ ] Only on findings
- [ ] End of audit only

---

## 6. Technical Constraints

### 6.1 Environment Considerations

**Production Testing:**
- [ ] Production testing is NOT authorized
- [ ] Production testing authorized with restrictions: ________________
- [ ] Production is the only available environment

**Air-Gap Requirements:**
- [ ] System must remain air-gapped during audit
- [ ] No external tool downloads permitted
- [ ] All tools must be pre-approved

**Performance Constraints:**
- [ ] Avoid testing during peak hours: ________________
- [ ] Rate limiting requirements: ________________
- [ ] Resource usage limits: ________________

### 6.2 Tool Restrictions

**Approved Tools:**
| Tool | Purpose | Approved? |
|------|---------|-----------|
| Static analysis (manual) | Code review | Yes |
| grep/find utilities | Pattern searching | Yes |
| | | |

**Prohibited Tools:**
- [ ] Automated vulnerability scanners (e.g., Burp Suite, OWASP ZAP)
- [ ] Network scanners (e.g., Nmap)
- [ ] Exploitation frameworks (e.g., Metasploit)
- [ ] Custom exploit code

---

## 7. Deliverables

### 7.1 Expected Outputs

- [ ] Executive Summary
- [ ] Full Technical Report
- [ ] Finding Documents (per vulnerability)
- [ ] Remediation Roadmap
- [ ] Compliance Mapping (OWASP, CWE)
- [ ] Verification Retest (if applicable)

### 7.2 Report Delivery

- **Format:** Markdown / PDF / HTML
- **Encryption:** [ ] Required (GPG/PGP key: ________________)
- **Delivery Method:** ________________
- **Delivery Date:** ________________

### 7.3 Retention Policy

- [ ] Delete all audit artifacts after delivery
- [ ] Retain for _______ days/months
- [ ] Client-specified retention: ________________

---

## 8. File System Changes

### 8.1 Audit Directory

The audit will create a `.audit/` directory containing:
- Finding documents
- Context files
- Generated reports

**Handling:**
- [ ] Add `.audit/` to `.gitignore`
- [ ] Include in repository (private repo only)
- [ ] Store externally: ________________

### 8.2 Code Modifications

- [ ] **No code changes** permitted (audit only)
- [ ] **Hot-fix mode**: May propose immediate fixes for Critical findings
- [ ] **Fix-as-you-go**: Implement fixes during audit
- [ ] **Separate branch** for any changes: ________________

---

## 9. Legal & Compliance

### 9.1 Liability

- [ ] Auditor liability waiver signed
- [ ] Mutual NDA in place
- [ ] Terms of engagement documented

### 9.2 Compliance Requirements

Relevant compliance frameworks for this audit:

- [ ] OWASP Top 10
- [ ] PCI-DSS
- [ ] HIPAA
- [ ] SOC 2
- [ ] GDPR
- [ ] ISO 27001
- [ ] Other: ________________

---

## 10. Sign-Off

### Auditor Acknowledgment

I acknowledge that I have read and understood these Rules of Engagement and agree to conduct the security audit within the boundaries defined herein.

| | |
|---|---|
| **Auditor Name** | |
| **Signature** | |
| **Date** | |

### Client/Stakeholder Approval

I authorize the security audit to proceed under these Rules of Engagement.

| | |
|---|---|
| **Authorizer Name** | |
| **Title** | |
| **Signature** | |
| **Date** | |

---

## Quick Reference Checklist

Before starting the audit, confirm:

```
□ Written authorization obtained
□ Scope clearly defined
□ Out-of-scope items documented
□ Prohibited activities understood
□ Emergency contact information available
□ Communication protocol established
□ .audit/ directory handling decided
□ Code modification policy confirmed
□ Report format and delivery agreed
```

---

*Document Version: 1.0*
*Framework: Codebase Security Audit Framework*
