# 🔒 Codebase Security Audit Framework

A comprehensive, structured security audit methodology for full-stack applications, specifically designed for:
- **Air-gapped environments**
- **Sensitive data handling**
- **Multi-tier access control systems**
- **Enterprise security requirements**

---

## 📋 Overview

This repository contains a complete security audit framework consisting of **12 sequential phases** that systematically examine every aspect of your application's security posture.

### Key Features

- ✅ **Sequential methodology** - Each phase builds on previous findings
- ✅ **LLM-optimized prompts** - Designed for use with Claude, GPT-4, or similar
- ✅ **Air-gap focused** - Special attention to offline/isolated environments
- ✅ **Comprehensive coverage** - Auth, APIs, infrastructure, secrets, and more
- ✅ **Actionable output** - Prioritized remediation roadmaps
- ✅ **Carry-forward system** - Context preserved across phases

---

## 📁 Repository Structure

```
codebase-audit/
├── README.md                          # This file
├── core-phases/                       # Main audit phases (run in order)
│   ├── phase-00-reconnaissance.md     # Attack surface mapping
│   ├── phase-01-authentication.md     # Identity verification
│   ├── phase-02-authorization.md      # Access control
│   ├── phase-03-api-security.md       # API endpoint security
│   ├── phase-04-business-logic.md     # Logic flaw detection
│   ├── phase-05-data-layer.md         # Database & storage
│   ├── phase-06-frontend.md           # Client-side security
│   ├── phase-07-infrastructure.md     # IaC & deployment
│   ├── phase-08-secrets-management.md # Credentials & keys
│   ├── phase-09-logging-monitoring.md # Audit trails
│   ├── phase-10-error-handling.md     # Failure modes
│   ├── phase-11-cross-cutting.md      # Integration review
│   └── phase-12-synthesis.md          # Final report
├── specialized/                       # Deep-dive audits
│   ├── kubernetes-audit.md            # K8s-specific checks
│   ├── graphql-audit.md               # GraphQL API security
│   └── api-penetration-testing.md     # Active testing guide
├── templates/                         # Documentation templates
│   ├── finding-template.md            # Individual finding format
│   └── progress-tracker.md            # Audit progress tracking
├── checklists/                        # Quick-reference checklists
│   └── master-checklist.md            # Consolidated checklist
└── .github/
    └── ISSUE_TEMPLATE/                # GitHub issue templates
        └── security-finding.md        # Finding issue template
```

---

## 🚀 Quick Start

### 1. Prepare Your Audit

1. Clone this repository
2. Create a secure workspace for audit materials
3. Gather access to all code repositories
4. Identify stakeholders and timeline

### 2. Run Phases Sequentially

```bash
# Start with Phase 0
1. Open core-phases/phase-00-reconnaissance.md
2. Provide the requested files to Claude/GPT-4
3. Run the audit prompt
4. Save the "Carry-Forward Summary"

# Continue to Phase 1
5. Open core-phases/phase-01-authentication.md
6. Paste previous Carry-Forward Summary
7. Provide authentication code
8. Run the audit prompt
9. Document findings
10. Save new Carry-Forward Summary

# Repeat for Phases 2-11...

# Finish with Phase 12
11. Compile all findings
12. Run synthesis prompt
13. Generate final report
```

### 3. Track Progress

Use `templates/progress-tracker.md` to monitor your audit status.

---

## 📖 Phase Descriptions

| Phase | Name | Purpose | Time Est. |
|-------|------|---------|-----------|
| 0 | Reconnaissance | Map attack surface, identify components | 2h |
| 1 | Authentication | Validate identity verification | 3h |
| 2 | Authorization | Check access control enforcement | 3h |
| 3 | API Security | Audit all API endpoints | 4h |
| 4 | Business Logic | Find logic flaws | 3h |
| 5 | Data Layer | Database & storage security | 3h |
| 6 | Frontend | Client-side vulnerabilities | 2h |
| 7 | Infrastructure | IaC & deployment security | 3h |
| 8 | Secrets | Credential management | 2h |
| 9 | Logging | Audit trail completeness | 2h |
| 10 | Error Handling | Secure failure modes | 2h |
| 11 | Cross-Cutting | Integration vulnerabilities | 3h |
| 12 | Synthesis | Final report & prioritization | 2h |

**Total Estimated Time:** 34 hours

---

## 🎯 Specialized Audits

For deeper analysis of specific technologies:

| Audit | Use When |
|-------|----------|
| `kubernetes-audit.md` | K8s/container deployments |
| `graphql-audit.md` | GraphQL APIs |
| `api-penetration-testing.md` | Active security testing |

---

## 📝 How to Use Prompts

### With Claude (Recommended)

1. Open the phase markdown file
2. Copy the prompt section (between triple backticks)
3. Paste into Claude conversation
4. Provide the requested code files
5. Review and document findings

### With Other LLMs

The prompts are designed for any capable LLM. Adjust context window usage as needed.

### Best Practices

- **Feed code in logical chunks** - Don't overwhelm the context window
- **Save carry-forward summaries** - These provide crucial context
- **Document as you go** - Don't wait until the end
- **Verify findings** - LLM analysis should be validated

---

## 🔐 Air-Gap Considerations

This framework includes special checks for air-gapped environments:

- ✅ External network dependency detection
- ✅ Offline certificate management
- ✅ Internal logging requirements
- ✅ Update mechanism review
- ✅ Telemetry/analytics detection

Look for "Air-Gap Specific" sections in each phase.

---

## 📊 Output Artifacts

After completing all phases, you'll have:

1. **Finding Database** - All security issues with severity ratings
2. **Attack Chain Analysis** - How vulnerabilities combine
3. **Prioritized Roadmap** - What to fix and when
4. **Executive Summary** - Leadership-ready overview
5. **Technical Recommendations** - Architecture improvements

---

## 🏷️ Finding Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Immediate compromise possible | Fix immediately |
| **High** | Significant security gap | Fix within 1-4 weeks |
| **Medium** | Defense-in-depth issue | Fix within 1-3 months |
| **Low** | Minor concern | Add to backlog |
| **Info** | Observation/improvement | Consider for future |

---

## 🤝 Contributing

Improvements welcome! Please submit issues or PRs for:
- Additional specialized audits
- Checklist improvements  
- New vulnerability patterns
- Better documentation

---

## 📄 License

MIT License - Use freely for your security audits.

---

## ⚠️ Disclaimer

This framework provides guidance for security audits but does not guarantee complete coverage. Always complement automated and LLM-assisted analysis with manual review and professional penetration testing for critical systems.

---

## 📞 Support

For questions about using this framework:
1. Check existing documentation
2. Open a GitHub issue
3. Consult security professionals for critical findings

---

**Happy Auditing! 🔍**
