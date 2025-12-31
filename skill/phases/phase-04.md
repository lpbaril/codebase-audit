# Phase 4: Business Logic

**Purpose:** Identify logic flaws and business rule vulnerabilities.

## Objectives

1. Review state management and transitions
2. Check for race conditions
3. Validate business rule enforcement
4. Analyze workflow integrity

## Key Checks

### State Management
- [ ] Valid state transitions enforced
- [ ] State machine properly implemented
- [ ] Invalid transitions rejected
- [ ] State cannot be manipulated externally

### Race Conditions
- [ ] Concurrent operations handled safely
- [ ] Database transactions used properly
- [ ] Optimistic/pessimistic locking implemented
- [ ] Double-submit prevention

### Business Rules
- [ ] All business rules enforced server-side
- [ ] Rules cannot be bypassed via ordering
- [ ] Limits and quotas enforced
- [ ] Edge cases handled

### Workflow Integrity
- [ ] Workflow steps cannot be skipped
- [ ] Process cannot be restarted improperly
- [ ] Approval chains enforced
- [ ] Audit trail maintained

## Common Logic Flaws

1. **Price manipulation** - Modifying prices in requests
2. **Quantity abuse** - Negative quantities, overflow
3. **Coupon stacking** - Using multiple discounts
4. **Race conditions** - Double-spending, duplicate claims
5. **Workflow bypass** - Skipping required steps
6. **Time manipulation** - Expired offers, trial abuse

## Patterns to Search

```javascript
// Dangerous patterns
if (req.body.price)           // User-controlled price
amount = parseInt(quantity)   // No bounds checking
await Promise.all([debit, credit])  // Potential race

// Good patterns
price = getProductPrice(productId)  // Server-side lookup
if (quantity < 0 || quantity > MAX)
await transaction.serialize([debit, credit])
```

## Test Cases

1. Submit negative quantities or prices
2. Concurrent requests for same operation
3. Out-of-order workflow steps
4. Boundary value testing

## Output

### Finding Format
```markdown
### [LOGIC-###] Finding Title
**Severity:** Critical/High/Medium/Low
**OWASP:** A04:2021 - Insecure Design
**CWE:** CWE-XXX
**Location:** file:line
**Issue:** [Description]
**Attack Scenario:** [How to exploit]
**Recommendation:** [Fix]
```

### Carry-Forward Summary

Document for next phase:
1. **Critical Workflows:** [Payment, signup, etc.]
2. **Race Condition Risks:** [Areas identified]
3. **Business Rule Issues:** [Any bypasses found]
4. **State Management:** [How state is handled]

---

*For detailed guidance, see `../core-phases/phase-04-business-logic.md`*
