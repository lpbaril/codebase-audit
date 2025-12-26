# Phase 5: Data Layer Security Audit

## Overview
**Purpose:** Validate database and storage security, encryption at rest  
**Duration:** 1-2 hours  
**Criticality:** CRITICAL — Data is the crown jewel  
**Output:** Data security assessment, encryption gaps, access patterns

## Files to Provide
- Database schemas/migrations
- ORM models and query patterns
- Data access layer (DAL/Repository) code
- Database configuration
- Encryption implementations
- Backup/restore procedures
- Any data masking code

---

## Prompt

```markdown
# Phase 5: Data Layer Security Audit

## Context
[PASTE: Previous Carry-Forward Summaries]

This system stores sensitive corporate secrets. Data layer security is critical—both data at rest and data in transit.

## Provided Materials
[PASTE YOUR DATA LAYER CODE FILES HERE]

---

## Audit Sections

### 5.1 Sensitive Data Inventory

**Classification Matrix:**
| Data Type | Classification | Storage | Encrypted? | Access Level | Retention |
|-----------|---------------|---------|------------|--------------|-----------|
| Passwords | Critical | users.password_hash | Hashed | System only | Permanent |
| API Keys | Critical | credentials | ? | Owner only | Until revoked |
| PII (names, emails) | High | users | ? | User+Admin | Account lifetime |
| Documents | High | documents | ? | Per doc | Policy |
| Audit logs | Medium | logs | ? | Admin only | 1 year |
| Session data | Medium | sessions | ? | System | Session lifetime |

**Questions:**
- [ ] Is all sensitive data identified?
- [ ] Is classification consistent across codebase?
- [ ] Are there any shadow data stores?

### 5.2 Schema Security Analysis

**Examine each table/collection:**

| Table | Sensitive Columns | Column Type Appropriate? | Constraints |
|-------|-------------------|-------------------------|-------------|
| users | password_hash | VARCHAR(255) ✅ | NOT NULL ✅ |
| users | email | VARCHAR(255) ✅ | UNIQUE ✅ |
| documents | content | TEXT - but encrypted? | |

**Schema Vulnerabilities:**
- [ ] Passwords stored as plain text?
- [ ] Sensitive fields have appropriate types?
- [ ] Primary keys predictable (sequential)?
- [ ] Foreign keys properly constrained?
- [ ] Indexes on sensitive columns? (information leakage via timing)
- [ ] Default values secure?

### 5.3 Query Security Analysis

**Query Pattern Review:**

| Location | Query Type | Parameterized? | Dynamic Parts | Risk |
|----------|------------|----------------|---------------|------|
| user_repo.py:45 | SELECT | Yes | None | Low |
| search.py:23 | SELECT | No | ORDER BY | High |
| admin.py:78 | DELETE | Yes | None | Low |

**Dangerous Patterns to Find:**
```python
# String interpolation
query = f"SELECT * FROM users WHERE id = {user_id}"

# String concatenation
query = "SELECT * FROM users WHERE name = '" + name + "'"

# Dynamic ORDER BY / GROUP BY (often overlooked)
query = f"SELECT * FROM users ORDER BY {sort_column}"

# ORM raw queries
Model.objects.raw(f"SELECT * FROM table WHERE {condition}")

# Unsafe ORM filters
User.objects.filter(**user_controlled_dict)  # NoSQL injection
```

### 5.4 Encryption at Rest

**Database-Level Encryption:**
| Feature | Status | Notes |
|---------|--------|-------|
| TDE (Transparent Data Encryption) | | |
| Encrypted storage volumes | | |
| Encrypted backups | | |

**Application-Level Encryption:**
| Field | Encrypted? | Algorithm | Key Location |
|-------|------------|-----------|--------------|
| document.content | | | |
| user.ssn | | | |
| credential.api_key | | | |

**Encryption Implementation Review:**
- [ ] Algorithm: AES-256-GCM or ChaCha20-Poly1305?
- [ ] Mode: GCM/CCM (authenticated) not ECB/CBC?
- [ ] IV/Nonce: Unique per encryption?
- [ ] Key derivation: PBKDF2/Argon2 for password-based?
- [ ] Key storage: Separate from data?
- [ ] Key rotation: Mechanism exists?

**Encryption Code Review:**
```python
# Look for patterns like:
from cryptography.fernet import Fernet  # ✅ Good
from Crypto.Cipher import DES  # ❌ Weak
import base64  # Is this "encryption"? ❌

# Check IV handling:
cipher = AES.new(key, AES.MODE_GCM)  # Good - random IV
cipher = AES.new(key, AES.MODE_ECB)  # Bad - no IV, pattern leakage
cipher = AES.new(key, AES.MODE_CBC, iv=b'\x00'*16)  # Bad - static IV
```

### 5.5 Data Access Patterns

**Data Access Layer Analysis:**
| Function | Data Accessed | Row-Level Filter? | Tenant Filter? |
|----------|---------------|-------------------|----------------|
| get_user() | users | By ID | N/A |
| list_documents() | documents | By owner | ? |
| search_all() | multiple | ??? | ??? |

**Access Control at Query Level:**
- [ ] All queries include ownership/tenant filter?
- [ ] No "SELECT *" without restrictions?
- [ ] Bulk operations properly restricted?
- [ ] Export functions filter appropriately?

### 5.6 Connection Security

**Database Connection Analysis:**
| Setting | Expected | Actual |
|---------|----------|--------|
| TLS/SSL enabled | Yes | |
| Certificate validation | Yes | |
| Minimum TLS version | 1.2+ | |
| Connection pooling | Yes | |
| Credential source | Vault/Env | |

**Connection String Security:**
- [ ] Not hardcoded in source?
- [ ] Not logged?
- [ ] Credentials from secure source?
- [ ] Different credentials per environment?

### 5.7 Data Lifecycle

**Retention & Deletion:**
| Data Type | Retention Policy | Actual Implementation |
|-----------|------------------|----------------------|
| User data | Until account deleted | Hard delete? Soft delete? |
| Audit logs | 1 year | Automatic purge? |
| Temp files | Session | Cleaned up? |

**Deletion Security:**
- [ ] Is deletion actually deletion (not soft delete for sensitive)?
- [ ] Are backups considered for deletion?
- [ ] Is cascade deletion correct?
- [ ] Are related records cleaned up?

**Data Export Security:**
- [ ] Export functions require authorization?
- [ ] Export is logged?
- [ ] Export respects data classification?
- [ ] Bulk export rate limited?

### 5.8 Backup Security

**Backup Analysis:**
| Question | Answer |
|----------|--------|
| Backups encrypted? | |
| Backup key management | |
| Backup access control | |
| Backup testing frequency | |
| Backup location | |
| Backup retention | |

**Air-Gap Backup Considerations:**
- [ ] Backups stored on air-gapped media?
- [ ] Backup transfer mechanism secure?
- [ ] Offline backup storage location secure?

### 5.9 File/Blob Storage

If storing files:

| Check | Status |
|-------|--------|
| Files stored outside webroot | |
| File paths sanitized (no traversal) | |
| File type validated by content | |
| File permissions set correctly | |
| Large file handling (chunked) | |
| Cleanup of orphan files | |

---

## Output Format

### Findings

```markdown
### [DATA-001] Unencrypted PII Storage

**Severity:** High
**Data at Risk:** User SSN, addresses stored in plaintext

**Location:**
- Table: `users`
- Columns: `ssn`, `address`

**Issue:**
Sensitive PII stored without encryption, visible to anyone with database access.

**Impact:**
- Data breach exposes all user PII
- Regulatory compliance violations (GDPR, etc.)
- Backup exposure risk

**Recommendation:**
```python
from cryptography.fernet import Fernet

# Encrypt before storage
encrypted_ssn = fernet.encrypt(ssn.encode())

# Decrypt on retrieval
ssn = fernet.decrypt(encrypted_ssn).decode()
```

Consider: Application-level encryption with proper key management.
```

---

### Phase 5 Summary

**Data Layer Security Score:** [1-10]

| Category | Status |
|----------|--------|
| Sensitive Data Identification | ✅/⚠️/❌ |
| Query Security (SQLi prevention) | ✅/⚠️/❌ |
| Encryption at Rest | ✅/⚠️/❌ |
| Access Pattern Security | ✅/⚠️/❌ |
| Connection Security | ✅/⚠️/❌ |
| Backup Security | ✅/⚠️/❌ |

---

### Phase 5 Carry-Forward Summary

```markdown
## Data Security Assessment
- Sensitive data identified: [Yes/Partially/No]
- Encryption status: [Full/Partial/None]
- Query security: [Parameterized/Gaps found]

## Encryption Gaps
- [Unencrypted sensitive fields]
- [Weak algorithms found]

## For Infrastructure Phase
- [Database config needs]
- [Backup concerns]

## For Logging Phase
- [Data access that should be logged]
- [Audit trail requirements]

## Immediate Action Items
1. [Encryption priority]
2. [Query security fix]
```
```

---

## Next Phase
→ **Phase 6: Frontend Security Audit**
