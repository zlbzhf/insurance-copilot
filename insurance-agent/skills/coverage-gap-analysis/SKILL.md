---
name: coverage-gap-analysis
description: Identify insurance coverage gaps without premature product pushing.
---

# Coverage Gap Analysis

Use after client-needs-intake or when sufficient client facts are available.

## Objective

Map client responsibilities and risks to possible coverage gaps. Keep needs analysis separate from product recommendation.

## Analysis Dimensions

- Medical expense exposure.
- Income interruption / disability exposure if in scope for the jurisdiction/product line.
- Critical illness / major disease expense and income impact.
- Life insurance / dependents / debt payoff / estate liquidity.
- Accident risk.
- Property/casualty exposure if in license scope.
- Long-term care / eldercare if relevant.
- Retirement or savings goals, clearly separated from protection needs.
- Business continuity / key-person / buy-sell funding if applicable.

## Output Format

```markdown
## Coverage Gap Analysis

### Executive Summary
- ...

### Gap Table

#### Gap 1: [name]
- Priority: High/Medium/Low
- Facts supporting the gap:
- Assumptions to verify:
- Why it matters:
- Possible solution categories, not products:
- Questions before recommendation:

### Existing Coverage Review
- What appears covered:
- What may be underinsured:
- What requires policy-source verification:

### Compliance Notes
- ...
```

## Guardrails

- Do not say the client is definitely underinsured without source verification.
- Do not calculate exact coverage needs unless assumptions are stated.
- Do not recommend replacement; if existing policy weakness appears, trigger policy-review.
- Cite sources or mark `[verify]`.
