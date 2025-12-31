---
name: security-audit
description: Comprehensive security audit for codebases. Use when asked to audit, review security, check for vulnerabilities, penetration test, or assess security posture. Supports web apps, mobile (iOS/Android/React Native/Flutter), APIs (REST/GraphQL), cloud (AWS), and Kubernetes deployments. Includes OWASP Top 10, SOC2, GDPR, PCI-DSS, and HIPAA compliance mapping.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Security Audit Skill

Autonomous security audit framework with 13 phases, specialized audits, and compliance mapping.

## Quick Start

When the user requests a security audit:

1. **Detect Technology Stack** - Run `python scripts/detect_stack.py <target_path>`
2. **Initialize Audit** - Run `python scripts/init_audit.py <target_path>`
3. **Execute Phases** - Run phases 0-12 sequentially
4. **Run Specialized Audits** - Based on detected technologies
5. **Generate Report** - Run `python scripts/generate_report.py <target_path>/.audit`

---

## Auto-Detection Workflow

### Step 1: Detect Technologies

```bash
python scripts/detect_stack.py /path/to/target
```

This outputs JSON with detected stack:
```json
{
  "app_type": "web|mobile|api|desktop|cli",
  "platforms": ["web", "ios", "android"],
  "frameworks": ["next.js", "react-native", "django"],
  "cloud": "aws|gcp|azure|self-hosted",
  "infrastructure": ["docker", "kubernetes"],
  "api_type": ["rest", "graphql"],
  "compliance_indicators": ["hipaa", "pci-dss"],
  "recommended_phases": ["0-12"],
  "recommended_specialized": ["mobile", "aws", "kubernetes"]
}
```

### Step 2: Present Audit Plan

Show the user what was detected and what audits will run:

```markdown
## Detected Technology Stack

**Application Type:** [From detection]
**Frameworks:** [List]
**Cloud Provider:** [Provider]
**Infrastructure:** [Docker/K8s/Serverless]
**API Type:** [REST/GraphQL/gRPC]
**Compliance Indicators:** [Any detected]

## Recommended Audit Path

### Core Security Audit (Phases 0-12)
[Always required - ~34 hours total]

### Specialized Audits
- [List based on detection]

Shall I proceed with this audit plan?
```

### Step 3: Initialize Audit Folder

After user confirms:

```bash
python scripts/init_audit.py /path/to/target
```

This creates:
```
target/.audit/
├── audit-context.md    # Session memory
├── findings/           # Individual findings
├── reports/            # Phase reports
└── carry-forward/      # Context summaries
```

**CRITICAL**: Before adding `.audit/` to `.gitignore`, you MUST:
1. Inform the user that audit artifacts exist in `.audit/`
2. Explain trade-offs (security vs. compliance history tracking)
3. Ask: "Would you like me to add `.audit/` to your `.gitignore`?"
4. Wait for explicit confirmation

---

## Phase Orchestration

### Core Phases (Run Sequentially)

| Phase | Name | Focus |
|-------|------|-------|
| 0 | [Reconnaissance](phases/phase-00.md) | Attack surface mapping |
| 1 | [Authentication](phases/phase-01.md) | Identity verification |
| 2 | [Authorization](phases/phase-02.md) | Access control |
| 3 | [API Security](phases/phase-03.md) | Endpoint security |
| 4 | [Business Logic](phases/phase-04.md) | Logic flaws |
| 5 | [Data Layer](phases/phase-05.md) | Database security |
| 6 | [Frontend](phases/phase-06.md) | Client-side security |
| 7 | [Infrastructure](phases/phase-07.md) | IaC & deployment |
| 8 | [Secrets Management](phases/phase-08.md) | Credential handling |
| 9 | [Logging & Monitoring](phases/phase-09.md) | Audit trails |
| 10 | [Error Handling](phases/phase-10.md) | Failure modes |
| 11 | [Cross-Cutting](phases/phase-11.md) | Integration review |
| 12 | [Synthesis](phases/phase-12.md) | Final report |

### Specialized Audits (Based on Detection)

| Audit | When to Use |
|-------|-------------|
| [Mobile Security](specialized/mobile.md) | iOS, Android, React Native, Flutter detected |
| [AWS Security](specialized/aws.md) | AWS cloud provider detected |
| [Kubernetes](specialized/kubernetes.md) | K8s manifests detected |
| [GraphQL](specialized/graphql.md) | GraphQL schema/queries detected |
| [Performance](specialized/performance.md) | Frontend performance requested |

---

## Session Persistence

### Reading Context

At the start of each session, check for existing audit:

```bash
# Check if audit exists
ls /path/to/target/.audit/audit-context.md
```

If exists, read it to understand:
- Current phase (where to resume)
- Completed phases
- Findings so far
- Carry-forward context

### Updating Context

After completing each phase:

1. Update `audit-context.md` with phase status
2. Save carry-forward summary to `carry-forward/phase-XX-summary.md`
3. Save any findings to `findings/`

---

## Finding Documentation

### Creating Findings

For each vulnerability discovered, create a finding file:

**Location:** `target/.audit/findings/{phase}-{number}.md`
**Example:** `target/.audit/findings/auth-001.md`

Use the template from [templates/finding.md](templates/finding.md)

### Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Immediate compromise possible | Fix immediately |
| High | Significant security gap | Fix within 1-4 weeks |
| Medium | Defense-in-depth issue | Fix within 1-3 months |
| Low | Minor concern | Add to backlog |
| Info | Observation | Consider for future |

### Validating Findings

```bash
python scripts/validate_finding.py /path/to/finding.md
```

---

## Report Generation

### Final Report

After completing all phases:

```bash
python scripts/generate_report.py /path/to/target/.audit
```

This generates `final-report.md` with:
- Executive Summary
- Findings by Severity
- Findings by Phase
- Attack Chain Analysis
- Prioritized Remediation Roadmap
- Compliance Mapping (if applicable)

---

## Compliance Tagging

Auto-tag findings with compliance frameworks:

| Finding Type | Auto-Tags |
|--------------|-----------|
| SQL Injection | OWASP A03, PCI 6.5, ISO A.8.28 |
| Broken Auth | OWASP A07, SOC2 CC6.1, HIPAA 164.312(d) |
| Sensitive Data Exposure | OWASP A02, PCI 3.4, GDPR Art.32(1)(a) |
| Missing Encryption | OWASP A02, PCI 4.1, HIPAA 164.312(e)(1) |
| Access Control Issues | OWASP A01, SOC2 CC6.1, PCI 7.1 |
| Security Misconfiguration | OWASP A05, PCI 2.2, ISO A.8.9 |
| Logging Failures | OWASP A09, SOC2 CC7.1, PCI 10.1 |

---

## Autonomous Execution Guidelines

### DO Automatically:
- Scan codebase to detect technologies
- Create `.audit/` folder structure
- Initialize `audit-context.md`
- Run phases sequentially
- Document findings as discovered
- Generate carry-forward summaries
- Proceed to specialized audits after core phases

### ASK User About:
- Adding `.audit/` to `.gitignore` (REQUIRED consent)
- Skipping phases that don't apply
- Prioritizing specific areas if time-constrained
- Clarifying business logic questions
- Access to external systems (databases, cloud consoles)

### ALWAYS Do at End:
- Generate final synthesis report
- Create prioritized remediation roadmap
- Update `audit-context.md` with completion status
- Offer to create GitHub issues for critical findings

---

## Air-Gap Considerations

Every phase includes air-gap specific checks:
- External network dependencies
- Telemetry/analytics detection
- Auto-update mechanisms
- License validation that phones home
- CDN references
- External resource loading

---

## Additional Resources

For full documentation, see the standalone markdown files:
- `../core-phases/` - Detailed phase prompts
- `../specialized/` - Full specialized audit guides
- `../compliance/compliance-mapping.md` - Complete compliance reference
- `../templates/` - Finding and report templates
- `../checklists/master-checklist.md` - Consolidated checklist
