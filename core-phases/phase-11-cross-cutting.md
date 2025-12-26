# Phase 11: Cross-Cutting Concerns & Integration Review

## Overview
**Purpose:** Identify security issues that span multiple components and trust boundaries  
**Estimated Time:** 3-4 hours  
**Prerequisites:** Phases 0-10 completed (this phase synthesizes previous findings)

## Files to Provide

```
□ All findings from Phases 0-10 (Carry-Forward Summaries)
□ Integration code not yet reviewed
□ Middleware stacks
□ Cross-service communication code
□ Message queue configurations
□ API gateway configuration
□ Service mesh configuration (if applicable)
```

---

## Audit Prompt

```markdown
# Phase 11: Cross-Cutting Concerns & Integration Review

## Context
[PASTE: ALL Previous Carry-Forward Summaries from Phases 0-10]

This phase examines how components interact and identifies security issues that span boundaries. Individual components may be secure, but their integration can create vulnerabilities.

## Environment Details
- **Air-gapped:** Yes - all integration points internal
- **Sensitivity Level:** Corporate secrets
- **Architecture:** [Brief description of overall architecture]

## Provided Materials
[PASTE: Integration code, middleware, cross-service communication]

---

## Audit Checklist

### 11.1 Trust Boundary Analysis

**Map all trust boundaries:**

```
┌─────────────────────────────────────────────────────────┐
│                    EXTERNAL BOUNDARY                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Frontend   │───▶│   API GW    │───▶│  Backend    │ │
│  │  (Browser)  │    │             │    │  Services   │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                              │          │
│                                              ▼          │
│                           ┌─────────────────────────┐   │
│                           │      Data Layer         │   │
│                           │  (DB, Cache, Files)     │   │
│                           └─────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**For each trust boundary, verify:**

| Boundary | Auth Verified? | AuthZ Re-checked? | Input Validated? | Output Sanitized? |
|----------|---------------|-------------------|------------------|-------------------|
| User → Frontend | | | | |
| Frontend → API | | | | |
| API → Backend | | | | |
| Backend → Database | | | | |
| Service → Service | | | | |
| Admin → System | | | | |

### 11.2 Cross-Service Authentication

- [ ] **Service identity:** How do services prove identity to each other?
- [ ] **Mutual TLS:** mTLS between services?
- [ ] **Service tokens:** Service-to-service tokens properly scoped?
- [ ] **Token propagation:** User context properly propagated?
- [ ] **Service accounts:** Least privilege for service accounts?

**Service Authentication Matrix:**

| Caller | Callee | Auth Method | Token Type | Scope Validation |
|--------|--------|-------------|------------|------------------|
| | | | | |

### 11.3 Cross-Service Authorization

- [ ] **Consistent enforcement:** Same rules across all services?
- [ ] **No trusted caller bypass:** Internal calls still authorized?
- [ ] **Context propagation:** User permissions flow correctly?
- [ ] **Aggregate permissions:** Combined service calls don't exceed user's permissions?

### 11.4 Data Flow Security

**Trace sensitive data through the system:**

```
[Entry Point] → [Processing] → [Storage] → [Retrieval] → [Display/Export]
```

For each sensitive data type:
- [ ] **Entry validation:** Validated and sanitized at entry?
- [ ] **In-transit encryption:** Encrypted between all components?
- [ ] **At-rest encryption:** Encrypted in all storage locations?
- [ ] **Processing security:** Protected during processing?
- [ ] **Output filtering:** Properly filtered before display/export?
- [ ] **Unintended copies:** No copies in caches, logs, temp files?

**Sensitive Data Flow Map:**

| Data Type | Entry Point | Processing | Storage | Exit Points | Copies |
|-----------|-------------|------------|---------|-------------|--------|
| User credentials | | | | | |
| Session tokens | | | | | |
| Business secrets | | | | | |
| PII | | | | | |

### 11.5 Session Consistency

- [ ] **Session propagation:** Session context consistent across services?
- [ ] **Session invalidation:** Logout propagates to all services?
- [ ] **Session storage:** Same session accessible from all services?
- [ ] **Session timeout:** Consistent timeout across services?
- [ ] **Concurrent sessions:** Handled consistently?

### 11.6 Race Conditions Across Components

- [ ] **Distributed race conditions:** Cross-service timing issues?
- [ ] **Distributed locks:** Locks work correctly across services?
- [ ] **Eventual consistency:** Security implications of async updates?
- [ ] **Order dependencies:** Operations that must happen in order enforced?

**Race Condition Scenarios:**
```
1. Two services update same resource → Which wins? Is it secure?
2. Auth check in Service A, action in Service B → Gap exploitable?
3. Permission revoked while operation in progress → Completed or stopped?
```

### 11.7 Configuration Consistency

- [ ] **Security settings:** Same across all environments?
- [ ] **Feature flags:** Security features can't be disabled?
- [ ] **Environment parity:** Dev/staging match prod security?
- [ ] **Config drift:** Detection for configuration changes?

### 11.8 Dependency Coordination

- [ ] **Version compatibility:** All services on compatible versions?
- [ ] **Security patches:** Patches coordinated across services?
- [ ] **API versioning:** Old insecure API versions disabled?
- [ ] **Deprecation:** Deprecated insecure features removed everywhere?

### 11.9 Message Queue Security (if applicable)

- [ ] **Message authentication:** Messages from legitimate senders?
- [ ] **Message encryption:** Sensitive messages encrypted?
- [ ] **Message integrity:** Tampering detected?
- [ ] **Poison messages:** Malformed messages handled safely?
- [ ] **Dead letter security:** Dead letter queues secured?

### 11.10 API Gateway Security (if applicable)

- [ ] **Central authentication:** Enforced at gateway?
- [ ] **Rate limiting:** Applied before backend processing?
- [ ] **Input validation:** Basic validation at gateway?
- [ ] **Request routing:** Can't bypass to internal services?
- [ ] **Header security:** Proper headers added/stripped?

---

## End-to-End Attack Scenarios

Walk through complete attack scenarios across components:

### Scenario 1: External Attacker → Admin Compromise
```
Starting point: No credentials
Goal: Administrative access
Path analysis: [Trace possible attack paths]
```

### Scenario 2: Low-Privilege User → Data Exfiltration
```
Starting point: Basic user credentials
Goal: Access to unauthorized data
Path analysis: [Trace possible attack paths]
```

### Scenario 3: Compromised Service → Lateral Movement
```
Starting point: One compromised service
Goal: Access to other services/data
Path analysis: [Trace possible attack paths]
```

### Scenario 4: Malicious Insider → Covering Tracks
```
Starting point: Legitimate privileged access
Goal: Exfiltrate data without detection
Path analysis: [Trace possible attack paths]
```

### Scenario 5: Physical Access → Data Extraction (Air-Gap Specific)
```
Starting point: Physical access to server
Goal: Extract sensitive data
Path analysis: [Trace possible attack paths]
```

---

## Integration Vulnerability Patterns

Check for these common integration issues:

| Pattern | Description | Check |
|---------|-------------|-------|
| Confused Deputy | Service acts on behalf of user without proper authorization | [ ] |
| TOCTOU | Time-of-check vs time-of-use across services | [ ] |
| Trust Escalation | Internal service calls bypass user restrictions | [ ] |
| Data Mixing | Multi-tenant data leaking across boundaries | [ ] |
| Session Riding | Actions performed in wrong user context | [ ] |
| Replay Attacks | Messages/tokens replayable across services | [ ] |

---

## Output Format

For each finding:
```
### [XCUT-###] Finding Title
**Severity:** Critical/High/Medium/Low
**Components Affected:** [List all components involved]
**Trust Boundary:** [Which boundary is affected]
**Issue:** Description of the cross-cutting vulnerability
**Attack Chain:** How this fits into a larger attack
**Recommendation:** Cross-component fix
**Coordination Required:** [Which teams need to coordinate]
**Effort:** Quick fix / Moderate / Significant
```

---

## Phase 11 Deliverables

1. **Trust Boundary Map** - Visual representation of all boundaries
2. **Data Flow Diagrams** - Sensitive data paths through system
3. **Attack Path Analysis** - Documented attack scenarios
4. **Integration Weakness Summary** - Cross-cutting vulnerabilities
5. **Service Dependency Map** - How services depend on each other
6. **Phase 11 Carry-Forward Summary** - Final summary for synthesis
```

---

## Carry-Forward Template

```markdown
## Phase 11 Carry-Forward Summary

### Trust Boundary Assessment
- [Summary of trust boundary security]

### Cross-Service Security
- [Authentication and authorization across services]

### Data Flow Risks
- [Sensitive data handling across components]

### Attack Paths Identified
- [Summary of viable attack scenarios]

### Critical Findings
- [List any Critical/High severity cross-cutting issues]

### Integration Gaps
- [Where component integration creates vulnerabilities]

### Coordination Requirements
- [Fixes that require multi-team coordination]
```

---

## Common Findings Reference

| Finding | Severity | Description |
|---------|----------|-------------|
| Service bypass | Critical | Can call internal service directly, bypassing auth |
| Session not propagated | High | User context lost between services |
| Trust escalation | High | Internal calls have elevated privileges |
| Missing boundary validation | High | Input not validated at trust boundary |
| Inconsistent authorization | Medium | Different auth rules in different services |
| Data flow through logs | Medium | Sensitive data logged between services |
| Async security gap | Medium | Security state changes during async operations |
| Config inconsistency | Medium | Security settings differ between services |
