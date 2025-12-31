# Phase 0: Reconnaissance

**Purpose:** Map the attack surface and understand the application architecture.

## Objectives

1. Identify all components, services, and entry points
2. Map data flows and trust boundaries
3. Inventory dependencies and check for known CVEs
4. Understand deployment architecture

## Key Checks

### Architecture Mapping
- [ ] All components identified (frontend, backend, databases, caches, queues)
- [ ] Data flows documented
- [ ] Entry points inventoried (APIs, webhooks, file uploads, etc.)
- [ ] Trust boundaries identified
- [ ] Third-party integrations listed

### Dependency Analysis
- [ ] All dependencies listed (package.json, requirements.txt, etc.)
- [ ] Known CVEs checked (`npm audit`, `pip-audit`, `trivy`)
- [ ] Outdated packages identified
- [ ] License compliance verified

### Air-Gap Considerations
- [ ] External network dependencies identified
- [ ] CDN usage detected
- [ ] Telemetry/analytics code found
- [ ] Auto-update mechanisms present

## Files to Examine

```
package.json, package-lock.json, yarn.lock
requirements.txt, Pipfile, pyproject.toml
Gemfile, Gemfile.lock
pom.xml, build.gradle
Dockerfile, docker-compose.yml
*.tf (Terraform), *.yaml (K8s manifests)
```

## Output

### Finding Format
```markdown
### [RECON-###] Finding Title
**Severity:** Critical/High/Medium/Low/Info
**Category:** Dependency / Architecture / Configuration
**Component:** [Affected component]
**Issue:** [Description]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Technology Stack:** [Frontend, Backend, Database, etc.]
2. **Entry Points:** [List all API endpoints, webhooks, etc.]
3. **Critical Dependencies:** [High-risk or outdated packages]
4. **Trust Boundaries:** [Where auth/authz is enforced]
5. **Architecture Diagram:** [Text description or link]
6. **Air-Gap Issues:** [Any external dependencies]

---

*For detailed guidance, see `../core-phases/phase-00-reconnaissance.md`*
