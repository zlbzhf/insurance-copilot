# Policy Review

Use this workflow to review existing customer policies, especially before cross-sell, upsell, cancellation, surrender, replacement, reinstatement, or renewal discussions.

## Required Sources

Prefer primary policy sources. Mark missing items clearly.

- Policy contract or schedule.
- Riders/endorsements.
- Premium notice or payment history if available.
- In-force illustration where applicable.
- Current values, loan balance, surrender value, and charges where applicable.
- Customer goals and current needs.
- Proposed new product if replacement is being considered.

## Review Steps

1. Identify policy type, insured, owner, beneficiary, carrier, issue date, premium, coverage amount, term, riders, and renewal features.
2. Summarize benefits in plain language.
3. Extract exclusions, waiting periods, renewal terms, cash value/surrender terms, loan provisions, fees, and important limitations.
4. Compare the policy to current customer needs and known gaps.
5. Flag missing source pages or uncertainty with `[verify]`.
6. If replacement is contemplated, list replacement risks and require escalation.
7. Produce a review memo, not a cancellation/surrender recommendation.

## Replacement / Surrender Risk Checklist

Before any replacement, cancellation, or surrender suggestion, explicitly review:

- benefits, riders, guarantees, or grandfathered terms that may be lost;
- new underwriting and insurability risk;
- new waiting periods, exclusions, and contestability periods;
- surrender charges, market value adjustments, policy loans, tax assumptions, and liquidity impact;
- premium differences and whether they are guaranteed or projected;
- whether the existing policy can be adjusted instead of replaced;
- required forms, disclosures, supervisor/compliance review, and customer acknowledgements.

## Output Format

```markdown
## Existing Policy Review

### Scope
- Customer goal:
- Policy source(s):
- Jurisdiction/license context:
- Replacement/surrender/cancellation involved? Yes/No/Unknown

### Policy Snapshot
- Carrier:
- Policy type:
- Insured/owner/beneficiary:
- Coverage amount:
- Premium:
- Term/renewal:
- Riders:
- Issue date:
- Sources:

### What It Appears To Cover
- ...

### Important Limitations / Exclusions
- ...

### Values / Charges / Renewal Details
- Cash value/surrender value/loan balance if applicable:
- Fees/charges:
- Renewal or lapse considerations:

### Fit Against Current Needs
- Needs still addressed:
- Possible gaps:
- Duplicate or overlapping coverage:
- Facts requiring verification:

### Replacement / Surrender Cautions
- Benefits potentially lost:
- New underwriting/waiting/contestability risk:
- Charges/tax/liquidity assumptions:
- Required escalation:

### Questions / Missing Documents
1. ...

### Draft Customer-Friendly Summary
[plain-language draft; no final recommendation]
```

## Guardrails

- Do not recommend canceling, surrendering, or replacing coverage without complete comparison and escalation.
- Do not state coverage is active unless verified from carrier/current policy source.
- Do not interpret tax consequences as final advice; mark tax assumptions for qualified review.
- Do not minimize exclusions, waiting periods, contestability, or lost benefits.
