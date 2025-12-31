# GraphQL Security Audit

**Focus:** Introspection, Query Complexity, Authorization, Injection
**Use With:** Phase 3 (API Security)

## Quick Checks

### Introspection
- [ ] Disabled in production
- [ ] Or restricted to authorized users

### Query Limits
- [ ] Depth limiting implemented
- [ ] Complexity analysis
- [ ] Timeout configured
- [ ] Rate limiting per query

### Authorization
- [ ] Field-level authorization
- [ ] Type-level authorization
- [ ] Resolver-level checks
- [ ] No over-fetching

### Input Validation
- [ ] Arguments validated
- [ ] Custom scalars validated
- [ ] No injection in resolvers

### Batching
- [ ] Batching attacks prevented
- [ ] Alias limit configured
- [ ] Array size limits

## Patterns

```graphql
# BAD - Unlimited depth
query DeepNested {
  user {
    friends {
      friends {
        friends {
          friends { ... }
        }
      }
    }
  }
}

# BAD - Alias attack
query AliasAttack {
  a1: user(id: 1) { name }
  a2: user(id: 2) { name }
  # ... 1000 more aliases
}
```

```javascript
// BAD - No auth check in resolver
const resolvers = {
  Query: {
    users: () => db.users.findAll()  // Anyone can query!
  }
}

// GOOD - Auth check
const resolvers = {
  Query: {
    users: (_, __, context) => {
      if (!context.user?.isAdmin) throw new ForbiddenError()
      return db.users.findAll()
    }
  }
}
```

```javascript
// Depth limiting
import depthLimit from 'graphql-depth-limit'

const server = new ApolloServer({
  validationRules: [depthLimit(5)]
})

// Complexity limiting
import { createComplexityLimitRule } from 'graphql-validation-complexity'

const server = new ApolloServer({
  validationRules: [createComplexityLimitRule(1000)]
})
```

## Test Queries

```graphql
# Test introspection
query {
  __schema {
    types { name }
  }
}

# Test depth
query {
  user { friends { friends { friends { id } } } }
}

# Test authorization
query {
  allUsers { sensitiveField }
}
```

## Finding Format
```markdown
### [GQL-###] Title
**Severity:** Critical/High/Medium/Low
**Query/Mutation:** [Name]
**Resolver:** file:line
**Issue:** [Description]
```

---

*Full guide: `../specialized/graphql-audit.md`*
