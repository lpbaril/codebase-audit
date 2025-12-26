# Phase 3: API Security Deep Dive

## Overview
**Purpose:** Validate all API endpoints for input validation, injection, and abuse  
**Duration:** 2-3 hours  
**Criticality:** CRITICAL — APIs are primary attack surface  
**Output:** Endpoint inventory, vulnerability findings, injection vectors

## Files to Provide
- All API route definitions
- Controllers/handlers
- Request validation schemas
- API middleware stack
- Rate limiting configuration
- Error handling
- OpenAPI/Swagger specs (if available)

---

## Prompt

```markdown
# Phase 3: API Security Deep Dive

## Context
[PASTE: Previous Carry-Forward Summaries]

APIs are the primary attack surface. Every endpoint must be analyzed for input validation, authentication enforcement, and abuse potential.

## Provided Materials
[PASTE YOUR API CODE FILES HERE]

---

## Audit Sections

### 3.1 Complete API Inventory

Create exhaustive endpoint list:

| Endpoint | Method | Auth | Level | Content-Type | Description | Risk |
|----------|--------|------|-------|--------------|-------------|------|
| /api/auth/login | POST | No | Public | JSON | User login | Med |
| /api/users | GET | Yes | User | JSON | List users | High |
| /api/users/:id | GET | Yes | User | JSON | Get user | High |
| /api/admin/settings | PUT | Yes | Admin | JSON | Modify settings | Critical |
| ... | | | | | | |

**Flag these patterns:**
- Undocumented endpoints (in code but not docs)
- Debug/test endpoints
- Administrative endpoints
- Endpoints accepting file uploads
- Endpoints with user-controlled redirects

### 3.2 Input Validation Analysis

**For EACH endpoint, verify:**

#### Request Body Validation
| Field | Type Expected | Validated? | Max Length | Pattern | Sanitized |
|-------|---------------|------------|------------|---------|-----------|
| email | string/email | | | | |
| name | string | | | | |
| age | number | | | | |
| role | enum | | | | |

**Validation Concerns:**
- [ ] Schema validation enforced (Joi, Yup, Pydantic, etc.)?
- [ ] Type coercion safe or strict?
- [ ] Array size limits?
- [ ] Object depth limits?
- [ ] String length limits?
- [ ] Numeric bounds checked?
- [ ] Enum values restricted?
- [ ] Date/time formats validated?

#### URL Parameters
- Path parameters validated?
- Query string sanitized?
- Array query params bounded?

#### Headers
- Custom headers validated?
- Content-Type enforced?
- Authorization header properly parsed?

### 3.3 Injection Vulnerability Analysis

**SQL Injection:**
```
# Search for patterns like:
query = f"SELECT * FROM users WHERE id = {user_input}"
cursor.execute("SELECT * FROM users WHERE name = '" + name + "'")
```

| Location | Query Type | Parameterized? | Risk |
|----------|------------|----------------|------|
| | | | |

**NoSQL Injection (MongoDB, etc.):**
```
# Search for patterns like:
db.users.find({ name: req.body.name })  # $gt, $where injection
db.users.find({ $where: userInput })
```

| Location | Query | Operator Injection Possible? |
|----------|-------|------------------------------|
| | | |

**Command Injection:**
```
# Search for patterns like:
os.system(f"convert {filename}")
subprocess.run(cmd, shell=True)
exec(user_input)
```

| Location | Command | User Input Involved? | Risk |
|----------|---------|---------------------|------|
| | | | |

**LDAP Injection:**
```
# If LDAP used for auth
filter = f"(&(uid={username})(userPassword={password}))"
```

**XML/XXE:**
```
# If XML parsing used
xml.etree.ElementTree.fromstring(user_xml)  # External entity processing?
```

**Template Injection (SSTI):**
```
# User input in templates
template.render(name=user_input)  # Can inject {{ code }}?
```

**Path Traversal:**
```
# File operations with user input
open(f"uploads/{filename}")  # ../../etc/passwd?
```

| Endpoint | Input | Traversal Possible? |
|----------|-------|---------------------|
| | | |

### 3.4 Output Security

**Response Data Leakage:**
| Endpoint | Sensitive Fields in Response | Should Be Filtered? |
|----------|------------------------------|---------------------|
| GET /users/:id | password, passwordHash | Yes |
| GET /profile | internalId, roleFlags | Maybe |

**Error Response Analysis:**
| Error Type | Current Response | Information Leaked |
|------------|------------------|-------------------|
| 500 Internal Error | Stack trace? | Technology, paths |
| 404 Not Found | Detailed message? | Valid/invalid resource |
| 401 Unauthorized | Specific reason? | Authentication state |
| 403 Forbidden | Specific reason? | Authorization config |
| Validation Error | Field details? | Schema information |

**Security Headers Check:**
| Header | Expected | Actual |
|--------|----------|--------|
| Content-Type | Appropriate for response | |
| X-Content-Type-Options | nosniff | |
| Cache-Control | no-store for sensitive | |
| X-Frame-Options | DENY or SAMEORIGIN | |
| Content-Security-Policy | Restrictive | |

### 3.5 Rate Limiting & Abuse Prevention

**Rate Limit Configuration:**
| Scope | Limit | Window | Bypass Possible? |
|-------|-------|--------|------------------|
| Per IP | | | X-Forwarded-For spoofing? |
| Per User | | | Account switching? |
| Per Endpoint | | | Endpoint variations? |
| Global | | | |

**Abuse Scenarios:**
- [ ] Login endpoint rate limited?
- [ ] Password reset rate limited?
- [ ] Resource creation limited?
- [ ] Search/query endpoints limited?
- [ ] Export/download limited?
- [ ] Expensive operations limited?

**Resource Exhaustion:**
| Attack Vector | Protection |
|---------------|------------|
| Large request body | Body size limit? |
| Many concurrent requests | Connection limits? |
| Slow requests (Slowloris) | Timeout enforcement? |
| Large file uploads | Size and count limits? |
| Complex queries | Query complexity limits? |
| Paginated bulk fetch | Page size limits? |

### 3.6 CORS Configuration

**Current CORS Settings:**
```
Access-Control-Allow-Origin: [value]
Access-Control-Allow-Methods: [value]
Access-Control-Allow-Headers: [value]
Access-Control-Allow-Credentials: [value]
```

**CORS Vulnerabilities:**
| Check | Status |
|-------|--------|
| Origin: * with credentials | Critical if true |
| Reflected Origin | Dangerous |
| Null origin allowed | Risky |
| Overly permissive methods | Review needed |
| Preflight caching too long | Consider |

### 3.7 Request Integrity

**CSRF Protection:**
| Endpoint (state-changing) | CSRF Token Required? | SameSite Cookie? |
|---------------------------|---------------------|------------------|
| POST /api/settings | | |
| PUT /api/profile | | |
| DELETE /api/account | | |

**Request Validation:**
- [ ] Content-Type validated?
- [ ] Request signing for sensitive ops?
- [ ] Nonce/timestamp for replay prevention?
- [ ] Idempotency keys for duplicates?

### 3.8 File Upload Security

If file uploads exist:

| Check | Status | Notes |
|-------|--------|-------|
| File type validation (content-based) | | Extension only is insufficient |
| File size limits | | |
| Filename sanitization | | Path traversal? |
| Storage location (outside webroot) | | |
| Malware scanning | | |
| Image reprocessing | | Strip metadata |
| Upload rate limiting | | |

### 3.9 GraphQL Specific (if applicable)

| Check | Status |
|-------|--------|
| Introspection disabled in production | |
| Query depth limiting | |
| Query complexity limiting | |
| Field-level authorization | |
| Batching attack prevention | |
| Alias-based DoS prevention | |
| N+1 query prevention | |

### 3.10 API Documentation vs. Implementation

| Documented | Implemented | Match? | Security Concern |
|------------|-------------|--------|------------------|
| | | | |

**Undocumented endpoints found:**
1. ...

---

## Injection Testing Payloads

### SQL Injection
```
' OR '1'='1
'; DROP TABLE users;--
" OR ""="
1; WAITFOR DELAY '0:0:5'--
```

### NoSQL Injection
```json
{"$gt": ""}
{"$where": "sleep(5000)"}
{"$regex": "^a"}
```

### Command Injection
```
; ls -la
| cat /etc/passwd
`id`
$(whoami)
```

### XSS (for APIs returning HTML)
```
<script>alert(1)</script>
"><img src=x onerror=alert(1)>
javascript:alert(1)
```

### Path Traversal
```
../../../etc/passwd
....//....//....//etc/passwd
..%2f..%2f..%2fetc/passwd
```

---

## Output Format

### Findings

```markdown
### [API-001] SQL Injection in User Search

**Severity:** Critical
**Endpoint:** GET /api/users/search
**CWE:** CWE-89

**Location:**
- File: `src/controllers/users.py`
- Line: 45

**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
cursor.execute(query)
```

**Proof of Concept:**
```http
GET /api/users/search?q=' OR '1'='1 HTTP/1.1
```

**Impact:**
- Full database read access
- Potential data exfiltration
- Possible command execution via SQL

**Recommendation:**
```python
query = "SELECT * FROM users WHERE name LIKE %s"
cursor.execute(query, (f'%{search_term}%',))
```
```

---

### Phase 3 Summary

**API Security Score:** [1-10]

| Category | Status | Issues |
|----------|--------|--------|
| Input Validation | ✅/⚠️/❌ | |
| SQL Injection | ✅/⚠️/❌ | |
| NoSQL Injection | ✅/⚠️/❌ | |
| Command Injection | ✅/⚠️/❌ | |
| XSS | ✅/⚠️/❌ | |
| Rate Limiting | ✅/⚠️/❌ | |
| CORS | ✅/⚠️/❌ | |
| Error Handling | ✅/⚠️/❌ | |

**Endpoint Risk Matrix:**
| Risk Level | Count | Examples |
|------------|-------|----------|
| Critical | | |
| High | | |
| Medium | | |
| Low | | |

---

### Phase 3 Carry-Forward Summary

```markdown
## API Security Assessment
- Total endpoints: X
- Validated endpoints: X
- Rate-limited endpoints: X
- Overall security: [Strong/Moderate/Weak]

## Injection Findings
- SQL Injection: [Yes/No] - [locations]
- NoSQL Injection: [Yes/No] - [locations]
- Command Injection: [Yes/No] - [locations]

## For Business Logic Phase
- [Endpoints with complex logic]
- [State-changing operations]
- [Multi-step workflows via API]

## For Data Layer Phase
- [Database query patterns to verify]
- [Data exposure concerns]

## Immediate Action Items
1. [Critical injection fix]
2. [Rate limiting needs]
```
```

---

## Next Phase
→ **Phase 4: Backend Business Logic Audit**
