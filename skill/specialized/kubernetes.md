# Kubernetes Security Audit

**Focus:** RBAC, Network Policies, Pod Security, Secrets
**Use With:** Phase 7 (Infrastructure)

## Quick Checks

### RBAC
- [ ] Least privilege roles
- [ ] No cluster-admin for apps
- [ ] Service accounts scoped
- [ ] No default service account usage

### Pod Security
- [ ] runAsNonRoot: true
- [ ] readOnlyRootFilesystem: true
- [ ] allowPrivilegeEscalation: false
- [ ] No privileged containers
- [ ] Capabilities dropped

### Network Policies
- [ ] Default deny ingress
- [ ] Default deny egress
- [ ] Policies per namespace
- [ ] No allow-all rules

### Secrets
- [ ] Secrets encrypted at rest
- [ ] No secrets in ConfigMaps
- [ ] External secrets manager
- [ ] RBAC on secrets

### Resource Limits
- [ ] CPU/memory limits set
- [ ] Resource quotas per namespace
- [ ] LimitRange configured

## Patterns

```yaml
# BAD - Privileged container
securityContext:
  privileged: true
  runAsUser: 0

# GOOD
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

```yaml
# BAD - No network policy
# (All traffic allowed by default)

# GOOD - Default deny
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

```yaml
# BAD - Cluster-admin for app
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

# GOOD - Scoped permissions
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

## kubectl Verification

```bash
# Find privileged containers
kubectl get pods -A -o json | jq '.items[] |
  select(.spec.containers[].securityContext.privileged==true)'

# Find pods running as root
kubectl get pods -A -o json | jq '.items[] |
  select(.spec.securityContext.runAsNonRoot!=true)'

# Check RBAC
kubectl auth can-i --list --as=system:serviceaccount:default:default
```

## Finding Format
```markdown
### [K8S-###] Title
**Severity:** Critical/High/Medium/Low
**Resource:** [Deployment/Pod/ServiceAccount/etc.]
**Namespace:** [namespace]
**Location:** file:line
```

---

*Full guide: `../specialized/kubernetes-audit.md`*
