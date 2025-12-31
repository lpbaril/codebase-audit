# Phase 11: Cross-Cutting Concerns

**Purpose:** Review integration points and service boundaries.

## Objectives

1. Analyze trust boundaries
2. Check service-to-service security
3. Review data flow across components
4. Identify attack chain possibilities

## Key Checks

### Trust Boundaries
- [ ] All boundaries identified
- [ ] Auth verified at each boundary
- [ ] Input validated at receiving side
- [ ] Output sanitized at sending side

### Service-to-Service Security
- [ ] mTLS or service mesh
- [ ] API keys/tokens for internal calls
- [ ] Least privilege between services
- [ ] Request signing where appropriate

### Context Propagation
- [ ] User context properly passed
- [ ] Tenant context maintained
- [ ] Audit context preserved
- [ ] No privilege escalation via context

### Data Flow Security
- [ ] Sensitive data encrypted in transit
- [ ] No unintended data copies
- [ ] Data minimization between services
- [ ] PII tracking across boundaries

## Integration Points to Review

| Integration | Security Check |
|-------------|----------------|
| API Gateway → Backend | Auth validation, rate limiting |
| Backend → Database | Connection security, least privilege |
| Backend → Cache | Data sensitivity, TTL |
| Backend → Queue | Message signing, encryption |
| Backend → External API | TLS, credential security |
| Microservice → Microservice | mTLS, service mesh |

## Attack Chain Analysis

Look for chains like:
1. XSS → Session theft → Account takeover
2. IDOR → Data leak → Privilege escalation
3. SSRF → Internal access → Credential theft
4. Injection → Data extraction → Lateral movement

## Patterns to Search

```javascript
// Service calls
fetch(internalService + req.params.path)  // SSRF risk
axios.get(url, { headers: req.headers })   // Header forwarding risk

// Context issues
db.query(sql, { userId: req.body.userId })  // User-controlled context
```

## Output

### Finding Format
```markdown
### [CROSS-###] Finding Title
**Severity:** High/Medium/Low
**OWASP:** Multiple
**CWE:** CWE-XXX
**Components:** [Service A → Service B]
**Issue:** [Description]
**Attack Chain:** [If applicable]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Service Architecture:** [Monolith/Microservices]
2. **Trust Boundaries:** [Identified locations]
3. **Service Auth:** [mTLS/API Key/None]
4. **Attack Chains:** [Potential combinations]
5. **Integration Risks:** [High-risk integrations]

---

*For detailed guidance, see `../core-phases/phase-11-cross-cutting.md`*
