# Specialized: Kubernetes Security Audit

## Overview
**Use Case:** Deep-dive audit for Kubernetes-based deployments  
**Use With:** Phase 7 (Infrastructure) or standalone  
**Estimated Time:** 3-4 hours

---

## Files to Provide

```
□ All Kubernetes manifests (deployments, services, configmaps, secrets)
□ Helm charts (if used)
□ Kustomize overlays (if used)
□ Network policies
□ RBAC configurations (roles, rolebindings, serviceaccounts)
□ Pod security policies / Pod security standards
□ Ingress configurations
□ Admission controller configurations
□ Operator configurations (if any)
□ kubectl get all -A output
```

---

## Audit Prompt

```markdown
# Kubernetes Security Deep Dive

## Context
[PASTE: Previous phase summaries if running as part of full audit]

This is an air-gapped Kubernetes deployment handling sensitive corporate data. All workloads must be secured and isolated appropriately.

## Environment Details
- **Kubernetes Version:** [Version]
- **Distribution:** [EKS/GKE/AKS/OpenShift/Vanilla/RKE/k3s]
- **Air-gapped:** Yes - no external registry access, no internet
- **Namespaces:** [List critical namespaces]

## Provided Materials
[PASTE: K8s manifests, RBAC configs, network policies]

---

## Audit Checklist

### K8S-1: Pod Security

#### Container Security Context
For each deployment/pod, verify:
- [ ] `runAsNonRoot: true` - Containers don't run as root
- [ ] `readOnlyRootFilesystem: true` - Filesystem is read-only where possible
- [ ] `allowPrivilegeEscalation: false` - No privilege escalation
- [ ] `capabilities.drop: ["ALL"]` - All capabilities dropped
- [ ] `capabilities.add` - Only necessary capabilities added
- [ ] `privileged: false` - No privileged containers
- [ ] `runAsUser/runAsGroup` - Specific non-root UID/GID set
- [ ] `seccompProfile` - Seccomp profile applied

**Pod Security Standards/Policies:**
- [ ] Pod Security Admission configured?
- [ ] Appropriate level (restricted/baseline/privileged) per namespace?
- [ ] Legacy PSP migrated if applicable?

### K8S-2: RBAC Configuration

#### Service Accounts
- [ ] Default service account not used for workloads?
- [ ] `automountServiceAccountToken: false` where not needed?
- [ ] Custom service accounts with minimal permissions?

#### Roles and ClusterRoles
- [ ] No overly permissive roles (*, verbs: ["*"])?
- [ ] No cluster-admin bindings to non-admin users/SAs?
- [ ] Roles scoped to specific resources?
- [ ] Secret access restricted?

**RBAC Audit Table:**
| ServiceAccount | Namespace | Roles/ClusterRoles | Concerning Permissions |
|----------------|-----------|--------------------|-----------------------|
| | | | |

#### Common RBAC Issues
- [ ] Can any SA list secrets cluster-wide?
- [ ] Can any SA create/modify RBAC resources?
- [ ] Can any SA exec into pods?
- [ ] Can any SA access the Kubernetes API extensively?

### K8S-3: Network Policies

- [ ] Default deny policy in all namespaces?
- [ ] Ingress rules specific (not allow-all)?
- [ ] Egress rules restrict outbound (critical for air-gap)?
- [ ] Database pods only accessible from app pods?
- [ ] Management interfaces isolated?

**Network Policy Coverage:**
| Namespace | Default Deny? | Ingress Policies | Egress Policies |
|-----------|---------------|------------------|-----------------|
| | | | |

### K8S-4: Secrets Management

- [ ] Secrets not in plain manifests (use sealed-secrets, external-secrets, vault)?
- [ ] Secrets encrypted at rest (etcd encryption)?
- [ ] Secret access logged?
- [ ] Secrets mounted as files, not env vars where possible?
- [ ] Secret rotation capability?

### K8S-5: Image Security

- [ ] Images from trusted internal registry only?
- [ ] Image pull policy set appropriately?
- [ ] Image tags are immutable (SHA digests preferred)?
- [ ] ImagePullSecrets configured for private registry?
- [ ] Image scanning in CI/CD?
- [ ] No `latest` tags in production?

**Air-Gap Image Management:**
- [ ] Internal registry properly secured?
- [ ] Image provenance tracked?
- [ ] Vulnerable images identified and tracked?

### K8S-6: Resource Limits

- [ ] CPU/memory requests set for all containers?
- [ ] CPU/memory limits set for all containers?
- [ ] ResourceQuotas per namespace?
- [ ] LimitRanges configured?

### K8S-7: Ingress Security

- [ ] TLS termination configured?
- [ ] Certificates valid and managed?
- [ ] Rate limiting at ingress?
- [ ] WAF rules (if applicable)?
- [ ] No sensitive paths exposed?

### K8S-8: etcd Security

- [ ] etcd encrypted at rest?
- [ ] etcd communication encrypted?
- [ ] etcd access restricted?
- [ ] etcd backup encrypted?

### K8S-9: API Server Security

- [ ] Anonymous auth disabled?
- [ ] Insecure port disabled?
- [ ] Audit logging enabled?
- [ ] Admission controllers configured (OPA/Kyverno)?
- [ ] API access restricted to necessary clients?

### K8S-10: Node Security

- [ ] Node access restricted?
- [ ] Kubelet authentication required?
- [ ] Kubelet authorization mode set (not AlwaysAllow)?
- [ ] Node SSH access controlled?

### K8S-11: Air-Gap Specific

- [ ] No external registry references?
- [ ] No internet-dependent init containers?
- [ ] No webhooks calling external services?
- [ ] No telemetry sending data externally?
- [ ] Certificate management works offline?
- [ ] DNS resolution internal only?

---

## Security Benchmark Checks

**CIS Kubernetes Benchmark Categories:**

| Category | Status | Notes |
|----------|--------|-------|
| Control Plane Components | | |
| etcd | | |
| Control Plane Configuration | | |
| Worker Nodes | | |
| Policies | | |

---

## Output Format

For each finding:
```
### [K8S-###] Finding Title
**Severity:** Critical/High/Medium/Low
**Resource:** deployment/namespace/name or cluster-wide
**Manifest:** filename:line
**Issue:** Description
**Exploit Scenario:** How this could be exploited
**Recommendation:** Specific fix with YAML example
**CIS Benchmark:** Reference if applicable
```

---

## Deliverables

1. **RBAC Audit Report** - All service accounts and their permissions
2. **Network Policy Gap Analysis** - Missing network isolation
3. **Pod Security Assessment** - Security context analysis
4. **Image Inventory** - All images and their sources
5. **Air-Gap Compliance** - External dependency check
```

---

## Quick Reference: Secure Defaults

```yaml
# Secure container template
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      serviceAccountName: secure-app-sa
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 10000
        runAsGroup: 10000
        fsGroup: 10000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        image: internal-registry.local/app@sha256:...
        imagePullPolicy: Always
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```
