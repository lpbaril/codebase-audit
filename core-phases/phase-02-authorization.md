# Phase 2: Authorization & Access Control Deep Dive

## Overview
**Purpose:** Validate permission enforcement across all access levels  
**Duration:** 1-2 hours  
**Criticality:** CRITICAL — Authorization failures enable privilege escalation  
**Output:** Access control gaps, privilege escalation paths, permission matrix

## Files to Provide
- Role/permission definitions
- Authorization middleware/guards/decorators
- Policy files (ABAC/RBAC definitions)
- Resource ownership logic
- Admin/privileged function implementations
- API route definitions with auth requirements
- Database schemas for permissions

---

## Prompt

```markdown
# Phase 2: Authorization & Access Control Deep Dive

## Context
[PASTE: Phase 0 + Phase 1 Carry-Forward Summaries]

This system implements multiple access levels protecting sensitive corporate data. Authorization failures could allow privilege escalation or unauthorized data access.

## Access Level Documentation
Based on Phase 0 or provide here:
- Access levels: [Admin, Manager, User, Guest, Service Account, etc.]
- Protected resources: [Documents, Projects, Users, Settings, Audit Logs, etc.]
- Operations: [Create, Read, Update, Delete, Export, Share, etc.]

## Provided Materials
[PASTE YOUR AUTHORIZATION-RELATED CODE FILES HERE]

---

## Audit Sections

### 2.1 Access Control Model Analysis

**Model Identification:**
| Question | Answer |
|----------|--------|
| Primary model (RBAC/ABAC/ACL/Custom) | |
| Hybrid approaches used? | |
| Centralized or distributed enforcement? | |
| Policy stored where? (Code/Database/Config) | |

**Role Hierarchy:**
```
[Draw the role hierarchy]
Super Admin
    └── Admin
        └── Manager
            └── User
                └── Guest
```

- Is inheritance properly implemented?
- Can lower roles ever have permissions higher roles don't?
- Are service accounts properly scoped?

**Permission Granularity Assessment:**
| Resource | Create | Read | Update | Delete | Export | Share | Admin |
|----------|--------|------|--------|--------|--------|-------|-------|
| Own Profile | | | | | | | |
| Other Profiles | | | | | | | |
| Documents | | | | | | | |
| Projects | | | | | | | |
| Settings | | | | | | | |
| Audit Logs | | | | | | | |
| Users | | | | | | | |

Is granularity sufficient for least-privilege?

### 2.2 Enforcement Point Analysis

**Middleware/Guard Coverage:**

| Endpoint/Resource | Auth Check | Authz Check | Owner Check | Notes |
|-------------------|------------|-------------|-------------|-------|
| GET /api/users | ✅/❌ | ✅/❌ | N/A | |
| GET /api/users/:id | ✅/❌ | ✅/❌ | ✅/❌ | |
| POST /api/documents | ✅/❌ | ✅/❌ | N/A | |
| ... | | | | |

**Check Completeness:**
- [ ] ALL routes have authentication check?
- [ ] ALL routes have authorization check?
- [ ] Ownership verified for user-specific resources?
- [ ] Authorization checked on EVERY database query?
- [ ] Background jobs verify permissions?

### 2.3 IDOR (Insecure Direct Object Reference)

**Object Reference Analysis:**
| Object Type | ID Format | Predictable? | Access Check Exists? |
|-------------|-----------|--------------|---------------------|
| Users | UUID/Sequential | | |
| Documents | | | |
| Projects | | | |
| Files | | | |

**IDOR Test Cases:**
```
# Can User A access User B's resources?
GET /api/users/USER_B_ID/documents

# Can user access by guessing IDs?
GET /api/documents/1
GET /api/documents/2
GET /api/documents/3

# Can user access via different endpoints?
GET /api/documents/123
GET /api/projects/1/documents/123  # Same doc, different path
```

### 2.4 Horizontal Access Control

**Same-Level Access Boundaries:**
- [ ] User A cannot read User B's data?
- [ ] User A cannot modify User B's data?
- [ ] User A cannot delete User B's data?
- [ ] Shared resources properly isolated?
- [ ] Multi-tenant isolation verified? (if applicable)

**Sharing/Delegation Security:**
| Scenario | Expected Behavior | Actual |
|----------|------------------|--------|
| User shares document | Only specified users can access | |
| User removes share | Access immediately revoked | |
| User shares with "edit" | Cannot escalate to "admin" | |
| Shared user re-shares | Depends on policy | |

### 2.5 Vertical Access Control (Privilege Escalation)

**Privilege Escalation Vectors:**

| Vector | Test | Result |
|--------|------|--------|
| Self-role modification | Can user change their own role via API? | |
| Hidden admin endpoints | Are admin endpoints discoverable? | |
| Parameter pollution | Can role be injected in request body? | |
| Mass assignment | Are protected fields (role, isAdmin) assignable? | |
| JWT claim tampering | Can user modify role claim in token? | |
| API method bypass | If GET blocked, does POST work? | |
| Path manipulation | Does /admin work if /Admin blocked? | |
| HTTP verb tampering | Different behavior for OPTIONS/TRACE? | |

**Function-Level Authorization:**
```
# Test each privileged function
POST /api/admin/users          # Create user (admin only?)
PUT /api/admin/settings        # Change settings (admin only?)
DELETE /api/admin/audit-logs   # Clear logs (super admin only?)
POST /api/admin/impersonate    # Impersonate user (exists?)
```

### 2.6 Resource Ownership & Lifecycle

**Ownership Model:**
- How is ownership established?
- Can ownership be transferred?
- What happens when owner is deleted?

**Orphan Resource Analysis:**
| Event | Resource Behavior |
|-------|-------------------|
| User deleted | Owned documents... |
| Project deleted | Contained files... |
| Team disbanded | Shared resources... |

**Ownership Bypass:**
- [ ] Can admin bypass ownership for any resource?
- [ ] Can system/service accounts bypass ownership?
- [ ] Are bypasses logged?

### 2.7 Service Account & Internal Access

**Service Account Inventory:**
| Account | Purpose | Permissions | Credentials Location |
|---------|---------|-------------|---------------------|
| | | | |

**Internal API Security:**
- [ ] Internal APIs require authentication?
- [ ] Service-to-service auth mechanism?
- [ ] Internal APIs accessible from external network?
- [ ] Debug/admin endpoints protected?

**Scheduled Job Permissions:**
- What identity do background jobs run as?
- Are job permissions minimal?
- Can jobs be triggered by users?

### 2.8 Authorization Configuration Security

**Policy Management:**
- [ ] Permissions defined in code or configurable?
- [ ] Can permissions be modified at runtime?
- [ ] Who can modify permissions?
- [ ] Are permission changes audited?

**Fail-Secure Analysis:**
| Scenario | Expected Behavior | Actual |
|----------|-------------------|--------|
| Auth service unavailable | Deny all access | |
| Database unreachable | Deny all access | |
| Permission check throws error | Deny access | |
| Unknown role | Deny access | |
| Empty permission set | Deny access | |

**Caching Concerns:**
- Are permissions cached?
- How long is cache valid?
- Is cache invalidated on permission change?
- Could stale cache grant access?

### 2.9 Audit Trail for Authorization

**Access Logging:**
- [ ] Authorization decisions logged?
- [ ] Failed access attempts logged?
- [ ] Successful sensitive access logged?
- [ ] Logs include: who, what, when, outcome?

**Privileged Action Logging:**
- [ ] Admin actions logged with extra detail?
- [ ] Permission changes logged?
- [ ] User impersonation logged?
- [ ] Audit logs tamper-resistant?

---

## Permission Matrix Verification

Create and verify complete permission matrix:

### Expected Permissions Matrix
| Action | Guest | User | Manager | Admin | Super Admin | Service |
|--------|-------|------|---------|-------|-------------|---------|
| View own profile | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Edit own profile | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| View other profiles | ❌ | 👁️ | ✅ | ✅ | ✅ | 👁️ |
| Edit other profiles | ❌ | ❌ | 🔒 | ✅ | ✅ | ❌ |
| Delete users | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| View documents | ❌ | 👤 | 👤 | ✅ | ✅ | 🔒 |
| Create documents | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Delete any document | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Modify settings | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| View audit logs | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Clear audit logs | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

Legend: ✅ Full access, 👤 Own only, 👁️ Limited view, 🔒 Conditional, ❌ No access

### Actual Permissions (from code analysis)
[Fill in based on code review]

### Discrepancies Found
| Action | Expected | Actual | Severity |
|--------|----------|--------|----------|
| | | | |

---

## Attack Scenarios

### Scenario 1: Horizontal Privilege Escalation
User A attempts to access User B's resources through:
1. Direct ID manipulation
2. API parameter tampering
3. Relationship exploitation (shared resources)

### Scenario 2: Vertical Privilege Escalation
Regular user attempts to:
1. Access admin endpoints
2. Modify their own role
3. Escalate through mass assignment
4. Bypass UI restrictions via API

### Scenario 3: Privilege Confusion
Exploit transitions between:
1. Guest → Authenticated user
2. User → Manager
3. Manager → Admin
4. Any role → Service account permissions

### Scenario 4: Authorization Bypass
Attempt to bypass through:
1. HTTP method manipulation
2. Path traversal/normalization
3. Parameter pollution
4. Header manipulation

---

## Output Format

### Findings

```markdown
### [AUTHZ-001] Finding Title

**Severity:** Critical/High/Medium/Low
**Attack Type:** IDOR/Privilege Escalation/Broken Access Control
**CWE:** CWE-XXX

**Location:**
- File: `path/to/file.py`
- Line: XX-XX
- Function/Route: `GET /api/resource/:id`

**Description:**
[Clear explanation]

**Proof of Concept:**
```http
# HTTP request demonstrating the issue
GET /api/users/OTHER_USER_ID/secrets HTTP/1.1
Authorization: Bearer LOW_PRIV_TOKEN
```

**Impact:**
- Can access: [What unauthorized data/actions]
- Affected users: [Who is impacted]

**Recommendation:**
[Specific fix with code]

**References:**
- OWASP: Broken Access Control
```

---

### Phase 2 Summary

**Authorization Security Score:** [1-10]

| Category | Status | Issues |
|----------|--------|--------|
| Horizontal Access Control | ✅/⚠️/❌ | |
| Vertical Access Control | ✅/⚠️/❌ | |
| Object-Level Authorization | ✅/⚠️/❌ | |
| Function-Level Authorization | ✅/⚠️/❌ | |
| Ownership Enforcement | ✅/⚠️/❌ | |
| Service Account Security | ✅/⚠️/❌ | |

---

### Phase 2 Carry-Forward Summary

```markdown
## Authorization Assessment
- Model type: [RBAC/ABAC/Custom]
- Enforcement: [Centralized/Distributed]
- Overall security: [Strong/Moderate/Weak]

## Privilege Escalation Paths
- [Any confirmed escalation paths]
- [Potential escalation concerns]

## Access Control Gaps
- [Missing checks identified]
- [Inconsistent enforcement areas]

## For API Phase (Phase 3)
- [Endpoints needing deeper review]
- [Authorization bypasses to verify]

## For Data Phase (Phase 5)
- [Data access patterns to verify]
- [Row-level security needs]

## Immediate Action Items
1. [Critical fix]
2. [High priority fix]
```
```

---

## Checklist Before Moving to Phase 3

- [ ] Permission matrix created and verified
- [ ] All access control models documented
- [ ] IDOR vulnerabilities tested
- [ ] Privilege escalation vectors checked
- [ ] Service account permissions reviewed
- [ ] Fail-secure behavior verified
- [ ] Findings documented
- [ ] Carry-forward summary prepared

---

## Next Phase
→ **Phase 3: API Security Audit**

Files needed for Phase 3:
- All API route definitions
- Request validation/schemas
- API middleware
- Rate limiting configuration
- API documentation (OpenAPI/Swagger)
