# Phase 4: Backend Business Logic Security Audit

## Overview
**Purpose:** Find logical flaws that bypass security through valid operations  
**Duration:** 1-2 hours  
**Criticality:** HIGH — Logic flaws often bypass technical controls  
**Output:** Logic vulnerability findings, workflow security issues

## Files to Provide
- Core business logic modules
- Workflow/state machine implementations
- Transaction handling code
- Business rules and validation
- Integration with internal systems
- Order processing, approvals, or multi-step flows

---

## Prompt

```markdown
# Phase 4: Backend Business Logic Security Audit

## Context
[PASTE: Previous Carry-Forward Summaries]

Business logic vulnerabilities are often missed by automated tools. These are flaws where the code "works correctly" but the logic can be abused to achieve unintended outcomes.

## Provided Materials
[PASTE YOUR BUSINESS LOGIC CODE FILES HERE]

---

## Audit Sections

### 4.1 State Machine & Workflow Security

**Identify all state machines/workflows:**

| Workflow | States | Transitions | Critical? |
|----------|--------|-------------|-----------|
| Document approval | Draft→Review→Approved | 3 | Yes |
| User onboarding | Invited→Active→Verified | 3 | Yes |
| Order processing | ... | ... | ... |

**For each workflow, analyze:**

**Valid State Transitions:**
```
Draw the expected state machine:

[Draft] → [Submitted] → [Under Review] → [Approved]
              ↓               ↓              ↓
          [Rejected]     [Rejected]      [Revoked]
```

**State Transition Attacks:**
| Attack | Description | Test |
|--------|-------------|------|
| Skip states | Jump from Draft→Approved | Can API set state directly? |
| Reverse transitions | Go from Approved→Draft | Is this blocked? |
| Invalid states | Set state to "SuperApproved" | Is enum enforced? |
| Concurrent transitions | Two users approve simultaneously | Race condition? |
| Stuck states | Trigger state with no valid exit | Orphan handling? |

**Questions to answer:**
- [ ] Are ALL valid transitions explicitly defined?
- [ ] Are invalid transitions explicitly rejected?
- [ ] Can state be set directly via API?
- [ ] Are state changes logged?
- [ ] Are state changes reversible when they shouldn't be?
- [ ] What happens to in-progress workflows on system restart?

### 4.2 Race Conditions & Concurrency

**Critical sections to analyze:**

| Operation | Concurrent Risk | Protection |
|-----------|-----------------|------------|
| Balance/credit operations | Double-spend | Transaction lock? |
| Resource allocation | Over-allocation | Mutex? |
| Sequence number generation | Duplicates | Atomic increment? |
| Inventory operations | Oversell | Optimistic/pessimistic lock? |

**Race Condition Patterns:**
```
# Time-of-check to time-of-use (TOCTOU)
if has_permission(user):    # Check
    time.sleep(0.1)         # Window
    perform_action(user)    # Use

# Double-spend pattern
if balance >= amount:       # Check
    time.sleep(0.1)         # Window
    deduct(amount)          # Use - can run twice!
```

**Test scenarios:**
- [ ] Simultaneous requests to same endpoint
- [ ] Rapid repeated submissions
- [ ] Concurrent approval workflows
- [ ] Simultaneous resource claims

### 4.3 Transaction & Consistency

**Multi-step operations:**

| Operation | Steps | Atomic? | Rollback? |
|-----------|-------|---------|-----------|
| User registration | Create user + Send email | | |
| Document creation | Save doc + Set permissions | | |
| Payment processing | Validate + Charge + Update | | |

**Partial Failure Analysis:**
| Operation | If Step 2 Fails | Current Behavior | Secure? |
|-----------|-----------------|------------------|---------|
| | | | |

**Questions:**
- [ ] Are multi-step operations wrapped in transactions?
- [ ] What happens on partial failure?
- [ ] Can partial state be exploited?
- [ ] Are retries idempotent?
- [ ] Is there a compensation mechanism?

### 4.4 Numeric & Financial Logic

If handling numbers, currency, or quantities:

**Precision Issues:**
| Value Type | Storage Type | Precision Risk |
|------------|--------------|----------------|
| Currency | Float? Decimal? Integer (cents)? | Rounding errors |
| Percentages | | Division precision |
| Quantities | | Negative values? |

**Boundary Conditions:**
| Scenario | Test | Expected | Actual |
|----------|------|----------|--------|
| Zero amount | Transfer $0 | Reject | |
| Negative amount | Transfer -$100 | Reject | |
| Very large amount | Transfer $999999999999 | Handle | |
| Fractional amounts | Transfer $1.999 | Round correctly | |

**Calculation Vulnerabilities:**
- [ ] Order of operations correct?
- [ ] Integer overflow possible?
- [ ] Division by zero handled?
- [ ] Rounding manipulation possible?

### 4.5 Business Rule Bypass

**Identify business rules:**
| Rule | Enforcement Point | Bypassable? |
|------|-------------------|-------------|
| Max 5 projects per user | Project creation | Check at API? |
| Document size < 10MB | Upload handler | Client + server? |
| Approval requires 2 reviewers | Approval logic | Hardcoded? |

**Bypass Techniques:**
- [ ] Can limits be bypassed by splitting operations?
- [ ] Are limits checked on every relevant operation?
- [ ] Can limits be modified by users?
- [ ] Are limits enforced server-side (not just client)?
- [ ] Can timing attacks bypass limits?

### 4.6 Default Values & Empty States

**Default value analysis:**
| Field | Default Value | Exploitable? |
|-------|---------------|--------------|
| role | "user" | What if not set? |
| isActive | true | Default active? |
| permissions | [] | Empty = deny? |

**Empty/Null handling:**
| Operation | Empty Input | Null Input | Missing Input |
|-----------|-------------|------------|---------------|
| Search | | | |
| Filter | | | |
| Update | | | |

### 4.7 Time-Based Logic

**Time-dependent operations:**
| Operation | Time Dependency | Clock Skew Risk? |
|-----------|-----------------|------------------|
| Token expiration | Current time comparison | |
| Scheduled jobs | Trigger time | |
| Trial periods | Start/end dates | |
| Audit timestamps | Event time | |

**Timezone issues:**
- [ ] All times stored as UTC?
- [ ] Timezone conversions correct?
- [ ] User timezone handling secure?

**Air-gap time concerns:**
- [ ] How is time synchronized?
- [ ] What if system clock is wrong?
- [ ] Can users manipulate time-based features?

### 4.8 Integration Points

**Internal system integrations:**
| System | Integration Type | Trust Level | Data Validated? |
|--------|------------------|-------------|-----------------|
| | | | |

**Integration security:**
- [ ] Is data from internal systems validated?
- [ ] What happens if internal system unavailable?
- [ ] Are responses from internal systems trusted blindly?
- [ ] Are there circuit breakers?

---

## Logic Flaw Scenarios

### Scenario 1: Get Something for Nothing
- Can user gain access/resources without proper payment/approval?
- Can free tier users access paid features?
- Can trial be extended indefinitely?

### Scenario 2: Skip Required Steps
- Can approval be bypassed?
- Can required fields be omitted?
- Can verification be skipped?

### Scenario 3: Repeat Benefits
- Can discounts be applied multiple times?
- Can referral bonuses be claimed repeatedly?
- Can trial periods be reset?

### Scenario 4: Manipulate Outcomes
- Can voting/ratings be manipulated?
- Can order totals be modified?
- Can priorities be changed?

### Scenario 5: Affect Other Users
- Can User A's actions impact User B negatively?
- Can shared resources be monopolized?
- Can queues be jumped?

---

## Output Format

### Findings

```markdown
### [LOGIC-001] Double-Spend in Credit System

**Severity:** Critical
**Business Impact:** Users can claim credits multiple times

**Location:**
- File: `src/services/credits.py`
- Function: `claim_credit()`

**Vulnerable Logic:**
```python
def claim_credit(user_id, promo_code):
    if not already_claimed(user_id, promo_code):  # Check
        # No lock between check and use
        credit = get_promo_credit(promo_code)
        add_credit(user_id, credit)  # Use
        mark_claimed(user_id, promo_code)
```

**Exploit Scenario:**
1. Attacker sends 10 simultaneous requests
2. All pass the already_claimed check
3. User receives 10x the intended credit

**Proof of Concept:**
```bash
# Send concurrent requests
for i in {1..10}; do
  curl -X POST /api/claim-promo -d '{"code":"FREE50"}' &
done
```

**Business Impact:**
- Direct financial loss
- Unfair advantage
- System abuse

**Recommendation:**
```python
def claim_credit(user_id, promo_code):
    with database.transaction():
        # SELECT FOR UPDATE to lock row
        if not already_claimed_locked(user_id, promo_code):
            credit = get_promo_credit(promo_code)
            add_credit(user_id, credit)
            mark_claimed(user_id, promo_code)
```
```

---

### Phase 4 Summary

**Business Logic Security Score:** [1-10]

| Category | Status |
|----------|--------|
| State Machine Security | ✅/⚠️/❌ |
| Race Condition Protection | ✅/⚠️/❌ |
| Transaction Integrity | ✅/⚠️/❌ |
| Numeric Safety | ✅/⚠️/❌ |
| Business Rule Enforcement | ✅/⚠️/❌ |
| Time-Based Logic | ✅/⚠️/❌ |

---

### Phase 4 Carry-Forward Summary

```markdown
## Business Logic Assessment
- Critical workflows: [List]
- Race condition risks: [Yes/No] - [Where]
- Transaction gaps: [List]

## For Data Layer Phase
- [Database operations needing locks]
- [Consistency requirements]

## For Logging Phase
- [Business events that need audit trails]
- [Critical state changes]

## Immediate Action Items
1. [Critical logic fix]
2. [Race condition fix]
```
```

---

## Next Phase
→ **Phase 5: Data Layer Security Audit**
