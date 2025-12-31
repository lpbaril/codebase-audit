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
├── audit-selector.md                  # Auto-detect tech stack & recommend audits
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
│   ├── mobile-security-audit.md       # iOS, Android, React Native, Flutter
│   ├── aws-security-audit.md          # AWS services security
│   ├── kubernetes-audit.md            # K8s-specific checks
│   ├── graphql-audit.md               # GraphQL API security
│   ├── api-penetration-testing.md     # Active testing guide
│   └── frontend-performance-audit.md  # Performance & SEO audit
├── skill/                             # Claude Code Skill (auto-triggered)
│   ├── SKILL.md                       # Main skill entry point
│   ├── phases/                        # Condensed phase instructions
│   ├── specialized/                   # Condensed specialized audits
│   ├── templates/                     # Finding & report templates
│   └── scripts/                       # Utility scripts (Python)
│       ├── detect_stack.py            # Auto-detect technologies
│       ├── init_audit.py              # Initialize .audit/ folder
│       ├── validate_finding.py        # Validate finding format
│       └── generate_report.py         # Compile final report
├── compliance/                        # Compliance framework mappings
│   └── compliance-mapping.md          # OWASP, SOC2, GDPR, PCI-DSS, HIPAA
├── templates/                         # Documentation templates
│   ├── finding-template.md            # Individual finding format
│   ├── audit-context-template.md      # AI session memory template
│   └── progress-tracker.md            # Audit progress tracking
├── checklists/                        # Quick-reference checklists
│   └── master-checklist.md            # Consolidated checklist
└── .github/
    └── ISSUE_TEMPLATE/                # GitHub issue templates
        └── security-finding.md        # Finding issue template
```

---

## 🎯 Two Ways to Use This Framework

This framework supports **two usage modes** to fit your workflow:

### Option 1: Claude Code Skill (Recommended)

If you use **Claude Code** (Anthropic's CLI), the skill provides **automated orchestration**:

**Installation:**
```bash
# Copy the skill to your Claude Code skills directory
cp -r skill ~/.claude/skills/security-audit

# Or for project-specific use:
cp -r skill .claude/skills/security-audit
```

**Usage:**
```
# Just ask Claude to audit your codebase:
"Run a security audit on this codebase"
"Check this app for vulnerabilities"
"Perform a security review"
```

**What happens automatically:**
1. Claude detects your technology stack (frameworks, cloud, infrastructure)
2. Recommends appropriate audit phases and specialized audits
3. Creates `.audit/` folder for findings and reports
4. Runs phases sequentially with context preservation
5. Generates final report with prioritized remediation

### Option 2: Standalone Markdown (Any AI Tool)

Works with **ChatGPT, Cursor, Aider, Windsurf**, or any AI assistant:

1. Start with `audit-selector.md` to determine your audit path
2. Run phases sequentially from `core-phases/`
3. Save carry-forward summaries between sessions
4. Use `templates/` for consistent documentation
5. Reference `compliance/` for regulatory mapping

See detailed workflow below.

---

## 🚀 Quick Start with Claude Code

This framework is designed to work with AI coding assistants. The recommended approach uses **Claude Code** (Anthropic's CLI tool), but it also works with other AI tools.

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed (`npm install -g @anthropic-ai/claude-code`)
- Access to the codebase you want to audit
- Terminal/command line access

### Step 1: Clone This Framework

Clone this repository to a **separate folder** (not inside your target codebase):

```bash
# Clone the audit framework
git clone https://github.com/your-username/codebase-audit.git
cd codebase-audit
```

### Step 2: Initialize Claude Code

Start Claude Code from the framework folder and let it understand the audit methodology:

```bash
# Start Claude Code
claude

# Once inside Claude Code, initialize the framework context
/init
```

The `/init` command helps Claude understand the complete audit framework, including all phases, templates, and guidelines.

### Step 3: Start Your Audit

Tell Claude the path to your target codebase and ask it to begin the audit:

**Example prompts to start:**

```
Following this audit framework, please audit my codebase located at "../my-project/"
```

```
I want to run a security audit on my application at "C:/Projects/my-app/".
Please follow the phases in this framework, starting with Phase 0 Reconnaissance.
```

```
Audit the codebase at "../my-saas-app/" using this security framework.
Focus on authentication and API security first.
```

**For performance audits:**

```
Run a frontend performance audit on "../my-website/" using the
specialized/frontend-performance-audit.md guide.
```

### Step 4: Follow the Phases

Claude will automatically:

1. **Create the `.audit/` folder** in your target project for all findings
2. **Initialize `audit-context.md`** to track progress and enable resumption
3. **Run phases sequentially** (0 through 12), building on previous findings
4. **Document findings** using the templates in this framework
5. **Ask about `.gitignore`** before adding sensitive audit files

You can guide the process with prompts like:

```
Continue to the next phase
```

```
Focus more on the API endpoints in /src/api/
```

```
Skip Phase 7 (Infrastructure) - we don't use Kubernetes
```

```
Run the specialized GraphQL audit on our API
```

### Step 5: Resume an Audit

If you need to stop and resume later, Claude will read the `audit-context.md` file:

```
Resume the security audit on "../my-project/"
```

```
Continue the audit from where we left off
```

### Step 6: Generate Final Report

After completing all phases:

```
Generate the final synthesis report for this audit
```

```
Create an executive summary of all findings
```

---

## 🔧 Using with Other AI Tools

### ChatGPT / GPT-4 (Web Interface)

1. Open the phase markdown file (e.g., `core-phases/phase-00-reconnaissance.md`)
2. Copy the prompt section (between triple backticks)
3. Paste into ChatGPT along with your code files
4. Manually save the "Carry-Forward Summary" for the next phase
5. Repeat for each phase, pasting the previous summary

### Cursor / VS Code AI Extensions

1. Open your target codebase in Cursor
2. Reference this framework in your prompts:
   ```
   Using the audit methodology from @codebase-audit/core-phases/phase-00-reconnaissance.md,
   analyze this codebase for security vulnerabilities
   ```
3. Use `@file` references to include phase prompts

### Aider / Other CLI Tools

1. Start your AI tool in the framework directory
2. Provide the target codebase path
3. Reference phase files as context

### Best Practices for All Tools

- **Feed code in logical chunks** - Don't overwhelm the context window
- **Save carry-forward summaries** - These provide crucial context between sessions
- **Document as you go** - Don't wait until the end
- **Verify findings** - AI analysis should be validated by security professionals

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
| `mobile-security-audit.md` | iOS, Android, React Native, Flutter apps |
| `aws-security-audit.md` | AWS-deployed applications |
| `kubernetes-audit.md` | K8s/container deployments |
| `graphql-audit.md` | GraphQL APIs |
| `api-penetration-testing.md` | Active security testing |
| `frontend-performance-audit.md` | Frontend performance, Core Web Vitals, SEO |

### Compliance Mapping

Use `compliance/compliance-mapping.md` to map findings to:
- **OWASP Top 10 (2021)** - Web application security
- **SOC 2** - Trust service criteria
- **GDPR** - EU data protection
- **PCI-DSS v4.0** - Payment card security
- **HIPAA** - Healthcare data protection
- **ISO 27001:2022** - Information security management

---

## 🤖 AI Agent Guidelines

When using AI assistants (Claude, GPT-4, etc.) to conduct audits with this framework:

### Audit Artifact Storage

All AI-generated documents MUST be saved to a `.audit/` folder in the **project being audited**:

```
target-project/
├── .audit/                    # AI-generated audit artifacts
│   ├── audit-context.md       # Session memory (AI resumes from here)
│   ├── findings/              # Individual finding documents
│   ├── reports/               # Phase reports and summaries
│   ├── carry-forward/         # Carry-forward summaries
│   └── final-report.md        # Synthesized final report
├── src/
└── ...
```

**What goes in `.audit/`:**
- `audit-context.md` - Session memory for AI to resume audits
- Finding documents (from `templates/finding-template.md`)
- Progress tracker instances
- Carry-forward summaries
- Phase reports and final synthesis

### Audit Context File (Session Memory)

The AI MUST create and maintain `.audit/audit-context.md` using the template in `templates/audit-context-template.md`. This file enables:
- **Resuming audits** after breaks or codebase changes
- **Tracking remediation** status of findings (open/fixed/in-progress)
- **Preserving context** (carry-forward summaries, notes)

**AI Behavior:**
1. At audit start: Check if `.audit/audit-context.md` exists
2. If exists: Read it to understand previous state and resume
3. If not: Create it using the template
4. After each phase: Update the context file with current state

### Git Ignore Consent Rule

**CRITICAL:** Before adding `.audit/` to `.gitignore`, the AI MUST:

1. Inform the user that audit artifacts exist in `.audit/`
2. Explain trade-offs:
   - **Add to .gitignore:** Keeps sensitive findings out of version control (recommended)
   - **Do NOT add:** Allows audit history tracking (useful for compliance)
3. Explicitly ask: *"Would you like me to add `.audit/` to your `.gitignore`?"*
4. Wait for user confirmation before making changes

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
2. Consult security professionals for critical findings

---

**Happy Auditing! 🔍**
