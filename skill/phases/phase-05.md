# Phase 5: Data Layer

**Purpose:** Audit database security and data protection mechanisms.

## Objectives

1. Review query security and ORM usage
2. Check encryption at rest
3. Analyze data access controls
4. Verify data lifecycle management

## Key Checks

### Query Security
- [ ] All queries parameterized
- [ ] ORM used safely (no raw queries with user input)
- [ ] Query limits enforced (pagination)
- [ ] No mass assignment vulnerabilities

### Encryption at Rest
- [ ] Sensitive data encrypted
- [ ] Strong encryption algorithm (AES-256)
- [ ] Proper key management
- [ ] PII/PHI properly protected

### Database Access
- [ ] Database credentials secured
- [ ] Minimal privilege DB accounts
- [ ] No shared database credentials
- [ ] Connection strings not hardcoded

### Multi-Tenancy
- [ ] Data isolation enforced
- [ ] Row-level security implemented
- [ ] Cross-tenant queries prevented

### Data Lifecycle
- [ ] Retention policies implemented
- [ ] Secure deletion (not soft-delete only)
- [ ] Backups encrypted
- [ ] Data minimization practiced

## Patterns to Search

```javascript
// Dangerous patterns
.query(`SELECT * FROM users WHERE name = '${name}'`)
Model.findByIdAndUpdate(id, req.body)  // Mass assignment
db.connection(process.env.DB_URL)       // Check if hardcoded

// Good patterns
.query("SELECT * FROM users WHERE name = $1", [name])
Model.findByIdAndUpdate(id, { $set: { name: req.body.name } })
```

## Sensitive Data Categories

| Category | Examples | Protection Required |
|----------|----------|---------------------|
| PII | Name, email, address | Encryption, access control |
| PHI | Medical records | HIPAA compliance, encryption |
| Financial | Credit cards, bank | PCI-DSS, tokenization |
| Credentials | Passwords, tokens | Hashing, secure storage |

## Output

### Finding Format
```markdown
### [DATA-###] Finding Title
**Severity:** Critical/High/Medium/Low
**OWASP:** A02:2021 - Cryptographic Failures
**CWE:** CWE-XXX
**Location:** file:line
**Issue:** [Description]
**Data Affected:** [Type of data]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Databases Used:** [PostgreSQL, MongoDB, etc.]
2. **ORM/Driver:** [Prisma, Sequelize, etc.]
3. **Encryption Status:** [At rest, in transit]
4. **Sensitive Data:** [Types found]
5. **Access Control:** [Row-level, column-level]

---

*For detailed guidance, see `../core-phases/phase-05-data-layer.md`*
