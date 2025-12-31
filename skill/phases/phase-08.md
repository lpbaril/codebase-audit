# Phase 8: Secrets Management

**Purpose:** Audit credential storage, access, and rotation practices.

## Objectives

1. Find hardcoded secrets
2. Review secret storage mechanisms
3. Check access controls on secrets
4. Verify rotation capabilities

## Key Checks

### Secret Detection
- [ ] No hardcoded API keys
- [ ] No hardcoded passwords
- [ ] No hardcoded tokens
- [ ] No secrets in git history
- [ ] No secrets in logs

### Secret Storage
- [ ] Secrets in vault/manager (not env vars)
- [ ] Encryption at rest
- [ ] Secrets not in source code
- [ ] .env files in .gitignore

### Access Control
- [ ] Least privilege access to secrets
- [ ] Secret access audited
- [ ] Scoped appropriately per environment
- [ ] Service accounts use unique secrets

### Rotation
- [ ] Rotation capability exists
- [ ] Rotation process documented
- [ ] Emergency rotation tested
- [ ] No long-lived credentials

## Patterns to Search

```bash
# High-entropy strings (potential secrets)
[A-Za-z0-9+/]{40,}
[a-f0-9]{32,64}

# Common secret patterns
api[_-]?key\s*[:=]
password\s*[:=]
secret\s*[:=]
token\s*[:=]
AWS_SECRET
PRIVATE_KEY
```

## Common Secret Locations

| Location | Risk | Check |
|----------|------|-------|
| Source code | High | Grep for patterns |
| .env files | Medium | Ensure in .gitignore |
| Config files | High | Review all config |
| Docker images | High | Check build history |
| Git history | High | git log -p |
| CI/CD configs | Medium | Review pipeline files |

## Secret Types to Find

- API keys (AWS, GCP, Azure, third-party)
- Database credentials
- JWT secrets
- OAuth client secrets
- SSH keys
- TLS private keys
- Encryption keys

## Output

### Finding Format
```markdown
### [SECRET-###] Finding Title
**Severity:** Critical/High
**OWASP:** A02:2021 - Cryptographic Failures
**CWE:** CWE-798 (Hardcoded Credentials)
**Location:** file:line
**Secret Type:** [API Key / Password / Token]
**Issue:** [Description - DO NOT include actual secret]
**Recommendation:** [Rotate immediately, use secret manager]
```

### Carry-Forward Summary

Document for next phase:
1. **Secret Manager:** [Vault/AWS SM/None]
2. **Secrets Found:** [Count by type]
3. **Rotation Status:** [Automated/Manual/None]
4. **Access Control:** [How secrets are accessed]
5. **Immediate Actions:** [Secrets requiring rotation]

---

*For detailed guidance, see `../core-phases/phase-08-secrets-management.md`*
