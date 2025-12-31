# Phase 2: Authorization

**Purpose:** Verify access control mechanisms and privilege management.

## Objectives

1. Review access control model (RBAC, ABAC, ACL)
2. Test for IDOR vulnerabilities
3. Check horizontal and vertical privilege escalation
4. Verify service account permissions

## Key Checks

### Access Control Model
- [ ] Consistent authorization model across application
- [ ] Authorization checks on all protected routes
- [ ] Default deny behavior
- [ ] Fail-secure on authorization errors

### IDOR Prevention
- [ ] Object references validated against user permissions
- [ ] No sequential/predictable IDs exposed
- [ ] Indirect references used where appropriate

### Privilege Management
- [ ] Users cannot self-escalate privileges
- [ ] Role changes require proper authorization
- [ ] Admin functions properly protected
- [ ] Service accounts follow least privilege

### Multi-Tenancy
- [ ] Tenant isolation enforced
- [ ] Cross-tenant access prevented
- [ ] Tenant ID validated on all operations

## Patterns to Search

```javascript
// Dangerous patterns
if (user.isAdmin)        // Client-side role check only
params.id                // Direct use of user-supplied ID
req.body.role            // User-controlled role assignment

// Good patterns
authorize(user, resource, action)
checkPermission(userId, resourceId)
tenantId === user.tenantId
```

## Test Cases

1. Access resources with different user IDs
2. Modify role/permission parameters in requests
3. Access admin endpoints as regular user
4. Cross-tenant resource access attempts

## Output

### Finding Format
```markdown
### [AUTHZ-###] Finding Title
**Severity:** Critical/High/Medium/Low
**OWASP:** A01:2021 - Broken Access Control
**CWE:** CWE-XXX
**Location:** file:line
**Issue:** [Description]
**Recommendation:** [Fix with code example]
```

### Carry-Forward Summary

Document for next phase:
1. **AuthZ Model:** [RBAC/ABAC/ACL/Custom]
2. **Protected Resources:** [List critical resources]
3. **IDOR Findings:** [Any direct object reference issues]
4. **Privilege Escalation:** [Any escalation paths found]
5. **Multi-Tenancy:** [Isolation status]

---

*For detailed guidance, see `../core-phases/phase-02-authorization.md`*
