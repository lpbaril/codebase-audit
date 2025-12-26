# Phase 0: Codebase Reconnaissance & Attack Surface Mapping

## Overview
**Purpose:** Establish baseline understanding before diving into code  
**Duration:** 30-60 minutes  
**Output:** Architecture map, attack surface inventory, initial red flags

## Files to Provide
- README, ARCHITECTURE.md, or any design docs
- Directory tree structure (`tree -L 3` output)
- Package manifests (package.json, requirements.txt, go.mod, Cargo.toml)
- Docker/container configurations
- CI/CD pipeline definitions
- Any infrastructure diagrams

---

## Prompt

```markdown
# Phase 0: Codebase Reconnaissance & Attack Surface Mapping

## Context
You are beginning a comprehensive security audit of a full-stack application that:
- Handles sensitive corporate data and secrets
- Operates on air-gapped servers with no external network access
- Implements multi-tier access control (different user privilege levels)
- Must enforce local-only usage

Your goal is to map the system before deep analysis begins.

## Provided Materials
[PASTE YOUR FILES HERE]

---

## Tasks

### 1. Architecture Mapping
Analyze the codebase structure and create:

**Component Inventory:**
| Component | Type | Language/Framework | Purpose | Criticality |
|-----------|------|-------------------|---------|-------------|

**Data Flow Diagram (Text-based):**
```
[User] → [Frontend] → [API Gateway] → [Backend Services] → [Database]
                   ↓
              [Auth Service]
```

Identify:
- All major components and their responsibilities
- Data flow between components
- All entry points (APIs, CLI, scheduled jobs, message queues, webhooks)
- All exit points (responses, exports, logs, notifications)
- Shared resources (databases, caches, queues)

### 2. Attack Surface Inventory

Create comprehensive entry point analysis:

| Entry Point | Type | Auth Required? | Auth Level | Input Type | Data Sensitivity | Notes |
|-------------|------|----------------|------------|------------|------------------|-------|
| /api/login | REST | No | N/A | JSON | High (credentials) | |
| /api/users | REST | Yes | User+ | JSON | High (PII) | |
| ... | ... | ... | ... | ... | ... | |

Categorize by:
- **Public endpoints** (no auth)
- **Authenticated endpoints** (logged-in users)
- **Privileged endpoints** (admin/elevated)
- **Internal endpoints** (service-to-service)
- **Scheduled/Background** (cron jobs, workers)

### 3. Dependency Risk Assessment

**Direct Dependencies Analysis:**
| Package | Version | Purpose | Last Updated | Known CVEs | Risk Level |
|---------|---------|---------|--------------|------------|------------|

**Transitive Dependency Concerns:**
- Total dependency count
- Any dependencies with concerning history
- Dependencies that seem excessive for their purpose
- Outdated packages

**Air-Gap Compatibility Check:**
Flag any dependencies that:
- [ ] Require network access at runtime (telemetry, updates)
- [ ] Have license validation that phones home
- [ ] Load resources from CDNs
- [ ] Have auto-update mechanisms

### 4. Technology Stack Assessment

| Layer | Technology | Version | Security Considerations |
|-------|------------|---------|------------------------|
| Frontend | | | |
| API | | | |
| Backend | | | |
| Database | | | |
| Cache | | | |
| Queue | | | |
| Container | | | |
| Orchestration | | | |

### 5. Air-Gap Violation Scan

Search for patterns that violate air-gap requirements:

**Code Patterns to Flag:**
- External URLs (http://, https://, cdn., etc.)
- API calls to external services
- Telemetry/analytics code
- Update checkers
- License validation endpoints
- External font/script loading
- External image URLs

**Configuration Patterns to Flag:**
- External DNS references
- Cloud service configurations
- Third-party integrations
- External logging services

### 6. Initial Red Flags

Document immediate security concerns:

**Critical Concerns (Investigate First):**
1. ...

**Configuration Concerns:**
1. ...

**Code Quality Concerns:**
1. ...

**TODO/FIXME Security Items:**
Search for comments containing: TODO, FIXME, HACK, XXX, SECURITY, VULNERABLE, UNSAFE

### 7. Access Level Mapping

Document the access control structure:

| Role | Description | Approximate Permissions | User Count (if known) |
|------|-------------|------------------------|----------------------|
| Super Admin | | Full system access | |
| Admin | | | |
| Manager | | | |
| User | | | |
| Guest | | | |
| Service Account | | | |

### 8. Sensitive Data Inventory

| Data Type | Classification | Storage Location | Encryption Status | Access Control |
|-----------|---------------|------------------|-------------------|----------------|
| User credentials | Critical | | | |
| PII | High | | | |
| Business data | | | | |
| Audit logs | | | | |

---

## Output Format

### Architecture Summary
[Provide text-based architecture diagram and component relationships]

### Attack Surface Matrix
[Complete entry point table]

### Risk Heatmap
| Area | Risk Level | Reasoning |
|------|------------|-----------|
| Authentication | | |
| Authorization | | |
| Data Storage | | |
| API Endpoints | | |
| Infrastructure | | |

### Priority Investigation Areas
1. [Highest priority area for Phase 1+]
2. ...
3. ...

### Air-Gap Compliance Status
- ✅ Compliant areas
- ⚠️ Potential issues
- ❌ Violations found

### Phase 0 Carry-Forward Summary
```markdown
## Key Observations
- Application type: [Web app/API/Microservices/etc.]
- Primary language(s): [...]
- Critical components: [...]
- User roles identified: [...]

## Attack Surface Summary
- Total API endpoints: X
- Public endpoints: X
- Authenticated endpoints: X
- Admin endpoints: X

## Initial Concerns (for subsequent phases)
1. [Concern for Auth phase]
2. [Concern for API phase]
3. [Concern for Data phase]

## Air-Gap Status
[Compliant/Issues Found/Violations]

## Dependency Risk
[Low/Medium/High] - [Brief reasoning]
```
```

---

## Checklist Before Moving to Phase 1

- [ ] Architecture diagram created
- [ ] All entry points documented
- [ ] Dependency audit complete
- [ ] Air-gap violations identified
- [ ] Initial red flags documented
- [ ] Carry-forward summary prepared
- [ ] Access levels mapped
- [ ] Sensitive data inventory started

---

## Next Phase
→ **Phase 1: Authentication System Audit**

Files needed for Phase 1:
- All auth-related modules (login, registration, password reset)
- Session/token configuration
- OAuth/SSO integration code
- User model/schema definitions
- Auth middleware
