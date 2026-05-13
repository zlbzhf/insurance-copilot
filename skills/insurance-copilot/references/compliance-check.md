# Compliance Check

Use this skill before customer-facing content is sent or reused.

## Review Targets

- Emails and chat messages.
- Sales scripts.
- Social posts and ads.
- Seminar slides.
- Product comparison summaries.
- Recommendation memos.

## Risk Categories

- Absolute claims: guaranteed, risk-free, always, never, best, full coverage.
- Misleading benefit descriptions.
- Missing exclusions, waiting periods, renewability limits, fees, surrender charges, or assumptions.
- Unapproved performance or dividend language.
- Replacement/surrender risk.
- Rebating, inducement, twisting/churning concerns.
- Incomplete health disclosure or underwriting statements.
- Tax/legal/investment advice outside scope.
- Vulnerable-customer or high-pressure concerns.

## Output Format

```markdown
## Compliance Check

### Overall Risk
- Green / Yellow / Red

### Required Fixes Before Use
1. Original text:
   - Issue:
   - Safer replacement:

### Optional Improvements
- ...

### Missing Disclosures / Assumptions
- ...

### Escalation Required?
- Yes/No
- Reason:
```

## Green/Yellow/Red Definitions

- **Green:** likely safe as a draft, still requires normal licensed review.
- **Yellow:** usable only after listed fixes and review.
- **Red:** do not send; compliance/supervisor review required.

## Guardrails

- Do not approve final external use.
- Always call the result a draft review.
- If jurisdiction/product rules are unknown, mark `[verify with compliance]`.
