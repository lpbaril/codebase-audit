# Phase 7: Infrastructure

**Purpose:** Audit deployment configuration and infrastructure security.

## Objectives

1. Review container security
2. Check Kubernetes configuration (if applicable)
3. Analyze network segmentation
4. Verify IaC security

## Key Checks

### Container Security
- [ ] Minimal base images used
- [ ] Non-root user configured
- [ ] Capabilities dropped
- [ ] Read-only filesystem where possible
- [ ] Resource limits set
- [ ] No secrets in image layers

### Kubernetes (if applicable)
- [ ] RBAC configured with least privilege
- [ ] Network policies enforced
- [ ] Pod security standards applied
- [ ] Secrets encrypted at rest
- [ ] No privileged containers
- [ ] Resource quotas set

### Network Security
- [ ] Proper network segmentation
- [ ] Internal TLS configured
- [ ] No unnecessary ports exposed
- [ ] Ingress/egress rules defined

### IaC Security
- [ ] No hardcoded secrets in Terraform/CloudFormation
- [ ] State files secured
- [ ] Least privilege IAM roles
- [ ] Encryption enabled on resources

## Patterns to Search

```dockerfile
# Dockerfile issues
FROM ubuntu:latest      # Use specific versions
USER root               # Should be non-root
COPY . .                # May include secrets

# Good patterns
FROM node:20-alpine
USER node
COPY --chown=node:node package*.json ./
```

```yaml
# Kubernetes issues
securityContext:
  privileged: true      # DANGEROUS
  runAsRoot: true       # Avoid

# Good patterns
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

## Infrastructure Files to Review

```
Dockerfile, docker-compose.yml
*.yaml (K8s manifests)
*.tf (Terraform)
*.template (CloudFormation)
helmfile.yaml, values.yaml
.github/workflows/*.yml
```

## Output

### Finding Format
```markdown
### [INFRA-###] Finding Title
**Severity:** Critical/High/Medium/Low
**OWASP:** A05:2021 - Security Misconfiguration
**CWE:** CWE-XXX
**Location:** file:line
**Issue:** [Description]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Container Runtime:** [Docker/Podman/etc.]
2. **Orchestration:** [K8s/ECS/None]
3. **IaC Tool:** [Terraform/CloudFormation/etc.]
4. **Network Config:** [Segmentation status]
5. **Security Posture:** [Overall assessment]

---

*For detailed guidance, see `../core-phases/phase-07-infrastructure.md`*
