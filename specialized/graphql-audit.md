# Specialized: GraphQL Security Audit

## Overview
**Use Case:** Deep-dive audit for GraphQL APIs  
**Use With:** Phase 3 (API Security) or standalone  
**Estimated Time:** 2-3 hours

---

## Files to Provide

```
□ GraphQL schema files (.graphql, .gql)
□ Resolver implementations
□ Authentication/authorization middleware
□ Query complexity/depth configuration
□ Rate limiting configuration
□ Persisted queries configuration (if used)
□ Subscription implementations (if used)
□ Custom directives
□ GraphQL server configuration
```

---

## Audit Prompt

```markdown
# GraphQL Security Deep Dive

## Context
[PASTE: Previous phase summaries if running as part of full audit]

This GraphQL API handles sensitive corporate data in an air-gapped environment with multi-tier access control.

## Environment Details
- **GraphQL Framework:** [Apollo/Yoga/graphql-js/etc.]
- **Schema Approach:** [Code-first/Schema-first]
- **Auth Mechanism:** [JWT/Session/etc.]

## Provided Materials
[PASTE: Schema, resolvers, middleware, configuration]

---

## Audit Checklist

### GQL-1: Introspection Control

- [ ] Introspection disabled in production?
- [ ] `__schema` and `__type` queries blocked?
- [ ] Schema not publicly discoverable?

```graphql
# This should fail in production:
query {
  __schema {
    types { name }
  }
}
```

### GQL-2: Query Complexity & Depth

- [ ] **Query depth limiting:** Maximum depth enforced?
- [ ] **Query complexity analysis:** Complexity scoring implemented?
- [ ] **Field-level cost:** Expensive fields have higher cost?
- [ ] **Timeout:** Query execution timeout configured?
- [ ] **Batch limiting:** Maximum operations per request?

**Test Queries:**
```graphql
# Deep nesting attack
query {
  user {
    friends {
      friends {
        friends {
          friends { # ... continues
            name
          }
        }
      }
    }
  }
}

# Wide query attack
query {
  users(first: 10000) {
    posts(first: 10000) {
      comments(first: 10000) {
        text
      }
    }
  }
}
```

### GQL-3: Authentication

- [ ] All queries require authentication (except public ones)?
- [ ] Authentication checked before resolver execution?
- [ ] Token validation happens on every request?
- [ ] Anonymous access explicitly defined (not default)?

### GQL-4: Authorization

#### Field-Level Authorization
- [ ] Sensitive fields protected at resolver level?
- [ ] User can only access their own data?
- [ ] Admin fields restricted to admin users?
- [ ] Nested object permissions enforced?

**Authorization Matrix:**
| Type.Field | Public | User | Admin | Notes |
|------------|--------|------|-------|-------|
| Query.me | ❌ | ✅ | ✅ | |
| Query.users | ❌ | ❌ | ✅ | |
| User.email | ❌ | Own only | ✅ | |
| User.ssn | ❌ | ❌ | ❌ | PII |

#### Object-Level Authorization
- [ ] Resolver checks ownership before returning data?
- [ ] Cannot access other users' objects by ID?
- [ ] Nested objects checked independently?

### GQL-5: Input Validation

- [ ] All arguments validated?
- [ ] Custom scalars validate format?
- [ ] Enum values enforced?
- [ ] String length limits?
- [ ] Numeric bounds checked?
- [ ] Array size limits?

**Test Inputs:**
```graphql
mutation {
  createUser(input: {
    email: "not-an-email",
    name: "A".repeat(100000),
    age: -1
  }) { id }
}
```

### GQL-6: Injection Vulnerabilities

- [ ] **SQL Injection:** Arguments used safely in queries?
- [ ] **NoSQL Injection:** Object arguments sanitized?
- [ ] **LDAP Injection:** If LDAP used?
- [ ] **Command Injection:** Arguments not passed to shell?

```graphql
# Test for injection in search
query {
  search(query: "'; DROP TABLE users; --") { id }
}

# Test for NoSQL injection
query {
  user(where: { id: { "$gt": "" } }) { id }
}
```

### GQL-7: Batching & Aliasing Attacks

- [ ] **Alias limit:** Maximum aliases per query?
- [ ] **Batch mutation limit:** Cannot batch-create unlimited records?
- [ ] **Brute force via aliases:** Cannot test many passwords in one query?

```graphql
# Alias attack (auth brute force)
query {
  a1: login(password: "pass1") { token }
  a2: login(password: "pass2") { token }
  a3: login(password: "pass3") { token }
  # ... hundreds more
}
```

### GQL-8: Information Disclosure

- [ ] Error messages don't reveal implementation details?
- [ ] Stack traces not returned to clients?
- [ ] Field suggestions disabled (don't reveal schema)?
- [ ] Debug mode disabled in production?

### GQL-9: Rate Limiting

- [ ] Per-user/per-IP rate limiting?
- [ ] Complexity-based rate limiting?
- [ ] Different limits for mutations vs queries?
- [ ] Rate limit headers returned?

### GQL-10: Subscriptions Security (if applicable)

- [ ] Subscription authentication required?
- [ ] Subscription authorization enforced?
- [ ] Cannot subscribe to other users' events?
- [ ] Connection limits enforced?
- [ ] Subscription complexity limited?

### GQL-11: Persisted Queries (if applicable)

- [ ] Only persisted queries allowed in production?
- [ ] Arbitrary queries blocked?
- [ ] Persisted query IDs not guessable?

### GQL-12: N+1 and DoS Concerns

- [ ] DataLoader or equivalent used?
- [ ] Cannot trigger expensive database operations?
- [ ] Cannot cause memory exhaustion via large results?

### GQL-13: File Uploads (if applicable)

- [ ] File type validation?
- [ ] File size limits?
- [ ] Malware scanning?
- [ ] Secure storage location?

---

## Attack Scenarios

### Scenario 1: Schema Discovery
```
1. Try introspection query
2. Try field suggestion via typos
3. Analyze error messages for hints
```

### Scenario 2: Authorization Bypass
```
1. Query another user's object by ID
2. Query sensitive fields with different user contexts
3. Batch queries to bypass per-request auth checks
```

### Scenario 3: DoS Attack
```
1. Deep nested query
2. Wide query with large pagination
3. Aliased repeated expensive operations
4. Complex query that times out database
```

---

## Output Format

For each finding:
```
### [GQL-###] Finding Title
**Severity:** Critical/High/Medium/Low
**Type/Field:** Affected type.field or query/mutation
**Issue:** Description
**Exploit Query:** GraphQL query demonstrating issue
**Recommendation:** Specific fix with code example
```

---

## Deliverables

1. **Schema Authorization Matrix** - Permissions per field
2. **Complexity Analysis** - Expensive queries identified
3. **Input Validation Gaps** - Missing validation
4. **DoS Vulnerability Assessment** - Resource exhaustion risks
```

---

## Quick Reference: Secure Patterns

```typescript
// Field-level authorization
const resolvers = {
  User: {
    email: (parent, args, context) => {
      // Only return email if user is viewing their own profile or is admin
      if (context.user.id !== parent.id && !context.user.isAdmin) {
        return null; // or throw new ForbiddenError()
      }
      return parent.email;
    },
    
    // Sensitive field with directive
    ssn: () => {
      throw new ForbiddenError('SSN is not accessible via API');
    }
  }
};

// Query complexity configuration
const complexityConfig = {
  maximumComplexity: 1000,
  scalarCost: 1,
  objectCost: 10,
  listFactor: 10,
  
  // Custom field costs
  fieldCost: {
    'Query.expensiveReport': 100,
    'User.friends': 20
  }
};
```
