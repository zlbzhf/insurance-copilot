---
name: policy-review
description: Summarize an existing policy and flag replacement or coverage concerns.
---

# Policy Review

Use this skill to review existing customer policies, especially before cross-sell, upsell, cancellation, surrender, or replacement discussions.

## Required Sources

- Policy contract or schedule.
- Riders/endorsements.
- Premium notice if available.
- In-force illustration where applicable.
- Customer goals and current needs.

## Review Steps

1. Identify policy type, insured, owner, beneficiary, carrier, issue date, premium, coverage amount, term, riders.
2. Summarize benefits in plain language.
3. Extract exclusions, waiting periods, renewal terms, cash value/surrender terms if applicable.
4. Compare to current customer needs.
5. Flag missing source pages or uncertainty.
6. If replacement is contemplated, list replacement risks and escalation requirements.

## Output Format

```markdown
## Existing Policy Review

### Policy Snapshot
- Carrier:
- Policy type:
- Insured/owner:
- Coverage amount:
- Premium:
- Term/renewal:
- Riders:
- Sources:

### What It Appears To Cover
- ...

### Important Limitations / Exclusions
- ...

### Questions / Missing Documents
- ...

### Replacement Cautions
- Benefits that could be lost:
- New waiting/contestability periods:
- Surrender charges/tax issues:
- Underwriting risk:
- Escalation needed:

### Plain-Language Customer Draft
- ...
```

## Guardrails

- Never tell a customer to cancel/surrender based only on this review.
- Do not interpret ambiguous contract language as final; mark for licensed/compliance review.
- Do not provide tax or legal conclusions.
