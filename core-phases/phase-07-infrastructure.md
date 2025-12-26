# Phase 7: Infrastructure as Code Security Audit

## Overview
**Purpose:** Validate infrastructure security configurations  
**Duration:** 1-2 hours  
**Criticality:** CRITICAL — Misconfigured infrastructure exposes everything  
**Output:** IaC vulnerabilities, container security, network security

## Files to Provide
- Terraform/CloudFormation/Pulumi files
- Kubernetes manifests (Deployments, Services, Ingress, RBAC)
- Dockerfiles and docker-compose files
- Ansible/Chef/Puppet scripts
- Network configuration (firewalls, security groups)
- Any Helm charts

---

## Prompt

```markdown
# Phase 7: Infrastructure as Code Security Audit

## Context
[PASTE: Previous Carry-Forward Summaries]

For air-gapped sensitive systems, infrastructure security is paramount. Misconfigurations can expose entire systems.

## Provided Materials
[PASTE YOUR INFRASTRUCTURE CODE FILES HERE]

---

## Audit Sections

### 7.1 Container Security (Docker)

**Dockerfile Analysis:**

For each Dockerfile:
| Check | Expected | Actual | File |
|-------|----------|--------|------|
| Base image official | Yes | | |
| Base image minimal (alpine/distroless) | Preferred | | |
| Base image version pinned | Yes (not :latest) | | |
| Non-root user | USER directive present | | |
| No secrets in build | No ENV with secrets | | |
| Multi-stage build | Preferred | | |
| .dockerignore exists | Yes | | |

**Dangerous Patterns:**
```dockerfile
# Bad practices:
FROM ubuntu:latest              # Unpinned, large
USER root                       # Running as root
ENV API_KEY=secret123           # Secrets in image
COPY . /app                     # May copy .git, secrets
RUN chmod 777 /app              # Overly permissive
```

**Runtime Security:**
| Check | Status |
|-------|--------|
| read-only filesystem possible | |
| capabilities dropped | |
| no privileged mode | |
| resource limits set | |
| health checks defined | |

### 7.2 Docker Compose Security

```yaml
# Check for these issues:
services:
  app:
    privileged: true           # ❌ Never in production
    network_mode: "host"       # ❌ Exposes all ports
    cap_add:
      - ALL                    # ❌ Excessive capabilities
    volumes:
      - /:/host                # ❌ Host filesystem access
    environment:
      - DATABASE_PASSWORD=xxx  # ❌ Secrets in compose
```

| Service | Privileged | Host Network | Caps | Volume Mounts | Secrets Exposed |
|---------|------------|--------------|------|---------------|-----------------|
| | | | | | |

### 7.3 Kubernetes Security

**Pod Security Analysis:**
```yaml
# For each deployment, check securityContext:
securityContext:
  runAsNonRoot: true            # ✅ Required
  runAsUser: 1000               # ✅ Specific user
  readOnlyRootFilesystem: true  # ✅ Recommended
  allowPrivilegeEscalation: false  # ✅ Required
  capabilities:
    drop: ["ALL"]               # ✅ Recommended
```

| Deployment | Non-Root | Read-Only FS | Caps Dropped | Privilege Escalation |
|------------|----------|--------------|--------------|---------------------|
| | | | | |

**RBAC Analysis:**
| Role/ClusterRole | Permissions | Too Broad? |
|------------------|-------------|------------|
| | | |

**Dangerous RBAC:**
```yaml
# Overly permissive:
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]           # ❌ God mode

# Dangerous permissions:
rules:
- resources: ["secrets"]
  verbs: ["get", "list"]  # Can read all secrets
- resources: ["pods/exec"]
  verbs: ["create"]       # Can exec into pods
```

**Network Policies:**
| Namespace | Ingress Policy | Egress Policy | Default Deny? |
|-----------|----------------|---------------|---------------|
| | | | |

**Secrets Management:**
| Check | Status |
|-------|--------|
| Secrets not in manifests | |
| External secrets operator or similar | |
| Secrets encrypted at rest (etcd) | |
| Secret access RBAC limited | |

### 7.4 Terraform/IaC Security

**Provider Configuration:**
```hcl
# Check for hardcoded credentials:
provider "aws" {
  access_key = "AKIA..."  # ❌ Hardcoded
  secret_key = "..."      # ❌ Hardcoded
}
```

**Resource Security:**
| Resource Type | Security Check | Status |
|---------------|----------------|--------|
| Security Groups | Ingress 0.0.0.0/0 for SSH/RDP | |
| S3 Buckets | Public access blocked | |
| RDS | Publicly accessible = false | |
| IAM | Least privilege | |
| EBS/Disks | Encrypted | |

**State Security:**
| Check | Status |
|-------|--------|
| Remote state backend | |
| State file encrypted | |
| State locking enabled | |
| State access controlled | |

### 7.5 Network Configuration

**Firewall/Security Group Analysis:**
| Rule | Source | Destination | Ports | Protocol | Justified? |
|------|--------|-------------|-------|----------|------------|
| | | | | | |

**Red Flags:**
- [ ] SSH (22) open to 0.0.0.0/0?
- [ ] RDP (3389) open to 0.0.0.0/0?
- [ ] Database ports externally accessible?
- [ ] All ports open between subnets?

**Network Segmentation:**
| Tier | Segment | Can Reach | Should Reach? |
|------|---------|-----------|---------------|
| Frontend | DMZ | Backend | Yes |
| Backend | Internal | Database | Yes |
| Database | Internal | Internet | ❌ No |

### 7.6 Host Security (if managing hosts)

**OS Configuration:**
| Check | Status |
|-------|--------|
| Minimal OS installation | |
| Automatic security updates | |
| SSH key-only auth | |
| Root SSH disabled | |
| Firewall enabled | |
| Unnecessary services disabled | |
| Audit logging enabled | |

### 7.7 Air-Gap Infrastructure Specifics

**Update Mechanisms:**
| Component | Update Method | Air-Gap Compatible? |
|-----------|---------------|---------------------|
| OS packages | | Internal mirror? |
| Container images | | Internal registry? |
| Application code | | Manual deploy? |
| Dependencies | | Vendored? |

**Internal Services Required:**
| Service | Purpose | Implemented? |
|---------|---------|--------------|
| NTP server | Time sync | |
| DNS server | Name resolution | |
| Package mirror | Updates | |
| Container registry | Images | |
| Certificate Authority | TLS | |
| Log aggregator | Logging | |

### 7.8 Secrets in IaC

**Secret Detection:**
```bash
# Search for patterns:
grep -r "password\|secret\|api_key\|token" *.tf *.yaml *.yml
```

| File | Line | Type of Secret | Secure? |
|------|------|----------------|---------|
| | | | |

**Recommended Pattern:**
```yaml
# Instead of:
password: "hardcoded123"

# Use:
password: ${SECRET_FROM_VAULT}
# or
password:
  secretKeyRef:
    name: db-secrets
    key: password
```

---

## Output Format

### Findings

```markdown
### [INFRA-001] Container Running as Root

**Severity:** High
**Component:** Docker/Kubernetes

**Location:**
- File: `docker/Dockerfile.app`
- Deployment: `app-deployment.yaml`

**Issue:**
Container runs as root user, increasing blast radius of any compromise.

**Current Configuration:**
```dockerfile
FROM node:16
# No USER directive - runs as root
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
```

**Recommendation:**
```dockerfile
FROM node:16-alpine
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -D appuser
WORKDIR /app
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```

And in Kubernetes:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  allowPrivilegeEscalation: false
```
```

---

### Phase 7 Summary

**Infrastructure Security Score:** [1-10]

| Category | Status |
|----------|--------|
| Container Security | ✅/⚠️/❌ |
| Kubernetes Security | ✅/⚠️/❌ |
| Network Security | ✅/⚠️/❌ |
| Secrets in IaC | ✅/⚠️/❌ |
| Host Security | ✅/⚠️/❌ |
| Air-Gap Compliance | ✅/⚠️/❌ |

---

### Phase 7 Carry-Forward Summary

```markdown
## Infrastructure Assessment
- Container security: [Good/Needs work]
- Network isolation: [Strong/Weak]
- Secrets management: [Secure/Exposed]

## For Secrets Phase
- [IaC secrets to address]
- [Key management needs]

## For Logging Phase
- [Infrastructure logging needs]
- [Audit requirements]

## Air-Gap Status
- [Compliant/Violations found]
- [Internal services needed]

## Immediate Action Items
1. [Critical infra fix]
2. [Network fix]
```
```

---

## Next Phase
→ **Phase 8: Secrets Management Audit**
