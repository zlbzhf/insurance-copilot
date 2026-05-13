# Product-Fit Review

Use this workflow when the user provides a product brochure, policy wording, rate sheet, illustration, or product notes and asks whether it appears to fit known customer needs.

## Source Hierarchy

Prefer policy contract/riders over brochure summaries. If only marketing material is provided, mark all product details `[verify against contract/carrier source]`.

## Required Inputs

Do not produce a positive fit assessment until these are known or explicitly marked unknown:

- Customer intake or coverage-gap analysis.
- Product source documents or structured product facts.
- Jurisdiction and license/product scope.
- Carrier and product version/date.
- Whether this is new coverage, replacement, upsell, renewal, cross-sell, or reinstatement.
- Budget/premium comfort range.
- Existing policies that might be affected.
- Customer goals and constraints.

## Review Steps

1. Identify product category and intended use.
2. Extract key features: covered risks, exclusions, waiting periods, benefit triggers, renewal terms, premium structure, surrender charges, liquidity limits, underwriting requirements, and optional riders.
3. Map each feature to a documented customer need or gap.
4. Separate confirmed facts, assumptions, and missing facts.
5. Identify mismatches: budget, liquidity, time horizon, underwriting risk, exclusions, duplicate coverage, or unsuitable complexity.
6. If replacement/surrender/cancellation is involved, stop and require policy review plus escalation.
7. Produce a draft explanation, not a final recommendation.

## Fit Rating Rules

- **Strong candidate:** known customer need, verified product source, material caveats disclosed, no unresolved high-risk flags.
- **Possible candidate:** plausible match but missing facts or source verification remain.
- **Weak fit:** product features do not map well to stated goals, budget, time horizon, or risk profile.
- **Insufficient information:** client facts or product sources are inadequate.

Never use "best" or "guaranteed" language.

## Output Format

```markdown
## Product-Fit Review: [Product Name]

### Scope
- Customer scenario:
- Product source(s):
- Jurisdiction/license context:
- Transaction type: new / replacement / upsell / renewal / cross-sell / reinstatement

### Bottom Line
- Fit rating: Strong candidate / Possible candidate / Weak fit / Insufficient information
- Reason:
- Human review required before presentation: Yes

### Customer Need Match
| Need | Product feature | Source/citation | Caveat |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

### Key Cautions
- Exclusions/waiting periods:
- Premium/budget considerations:
- Underwriting assumptions:
- Liquidity/surrender/fee considerations:
- Tax/legal/investment assumptions, if any:

### Unsuitable / Not Yet Supported Uses
- ...

### Replacement or Existing Policy Issues
- Is replacement/surrender/cancellation involved? Yes/No/Unknown
- Benefits potentially lost:
- New waiting periods/contestability:
- Surrender charges/tax assumptions:
- Required escalation:

### Questions Before Presenting
1. ...

### Draft Agent Explanation
[plain-language script labeled as draft]

### Compliance Flags
- ...
```

## Guardrails

- Do not call a product "best".
- Do not guarantee approval, benefits, renewability, claims outcome, savings, or returns.
- Do not rely on illustrations without stating assumptions and source limitations.
- Do not present marketing facts as contract facts.
- For replacement, require `policy-review` and escalation before any customer recommendation.
- If the user asks for a final recommendation, respond with a draft support memo and list the licensed/compliance review required.
