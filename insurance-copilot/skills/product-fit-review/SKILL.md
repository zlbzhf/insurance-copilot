---
name: product-fit-review
description: Review whether a specific insurance product appears suitable for known customer needs.
---

# Product-Fit Review

Use this skill when the user provides a product brochure, policy wording, rate sheet, illustration, or product notes and asks whether it fits a customer's needs.

## Source Hierarchy

Prefer policy contract/riders over brochure summaries. If only marketing material is provided, mark all product details `[verify against contract]`.

## Required Inputs

- Customer intake or coverage-gap analysis.
- Product source documents or structured product facts.
- Jurisdiction and carrier.
- Whether this is new coverage, replacement, upsell, renewal, or cross-sell.

## Review Steps

1. Identify product category and intended use.
2. Extract key features: covered risks, exclusions, waiting periods, benefit triggers, renewal terms, premium structure, surrender charges, liquidity limits, underwriting requirements.
3. Match product features to customer goals and gaps.
4. Identify mismatches, assumptions, and facts requiring verification.
5. Flag replacement/suitability/compliance issues.
6. Produce a draft explanation, not a final recommendation.

## Output Format

```markdown
## Product-Fit Review: [Product Name]

### Bottom Line
- Fit rating: Strong / Possible / Weak / Insufficient information
- Reason:

### Customer Need Match
- Need:
- Relevant product feature:
- Source/citation:
- Caveat:

### Key Cautions
- ...

### Unsuitable / Not Yet Supported Uses
- ...

### Replacement or Existing Policy Issues
- ...

### Questions Before Presenting
1. ...

### Draft Agent Explanation
[plain-language script]

### Compliance Flags
- ...
```

## Guardrails

- Do not call a product "best".
- Do not guarantee approval, benefits, renewability, or returns.
- Do not rely on illustrations without stating assumptions.
- For replacement, require policy-review and escalation.
