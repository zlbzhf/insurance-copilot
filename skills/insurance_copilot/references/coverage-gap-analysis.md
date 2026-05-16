# Coverage Gap Analysis

Use after client-needs-intake or when sufficient client facts are available. This workflow maps responsibilities and risks to possible coverage gaps without prematurely pushing products.

## Objective

Separate needs analysis from product recommendation. Identify protection gaps, assumptions, and questions that must be resolved before recommending a product.

## Minimum Inputs

- Jurisdiction/residency and license/product scope.
- Household or business responsibilities.
- Dependents and income obligations.
- Existing insurance policies and employer/group benefits.
- Assets, debts, mortgage, business obligations.
- Goals and time horizon.
- Budget/premium comfort range.
- Health/underwriting-sensitive facts only if collected through approved language.

If these are missing, produce an intake gap list instead of a product recommendation.

## Analysis Dimensions

- Medical expense exposure.
- Income interruption / disability exposure if in scope.
- Critical illness / major disease expense and income impact.
- Life insurance / dependents / debt payoff / estate liquidity.
- Accident risk.
- Property/casualty exposure if in license scope.
- Long-term care / eldercare if relevant.
- Retirement or savings goals, clearly separated from protection needs.
- Business continuity / key-person / buy-sell funding if applicable.

## Prioritization Guidance

- **High priority:** risk could materially harm dependents, income continuity, home/business continuity, or required obligations; little or no known coverage.
- **Medium priority:** meaningful risk exists but severity, timing, or existing coverage is uncertain.
- **Low priority:** risk is less urgent, already partly addressed, or depends on future planning assumptions.
- **Unknown:** insufficient facts; ask questions before ranking.

## Output Format

```markdown
## Coverage Gap Analysis

### Scope
- Customer scenario:
- Jurisdiction/license context:
- Sources reviewed:
- Important unknowns:

### Executive Summary
- ...

### Gap Review

#### Gap 1: [name]
- Priority: High/Medium/Low/Unknown
- Facts supporting the gap:
- Assumptions to verify:
- Why it matters:
- Existing coverage that may address it:
- Possible solution categories, not products:
- Questions before recommendation:

### Existing Coverage Notes
- ...

### Not a Product Recommendation
- Explain what additional facts/source documents are needed before product selection.

### Compliance / Escalation Flags
- ...
```

## Guardrails

- Do not name a specific product unless the user asked for a separate product-fit review and sources are available.
- Do not quantify coverage amounts unless facts and methodology are provided; otherwise list data needed.
- Do not assume employer/group benefits are sufficient or active without verification.
- Do not use scare tactics.
- Mark all uncertain facts as `[verify]`.
