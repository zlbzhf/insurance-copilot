# Client Plan Draft

Use this workflow to combine a client intake, coverage-gap analysis, current-policy notes, and source-backed product facts into a review-ready client plan draft. The output supports a licensed professional's review; it is not a final recommendation.

## Inputs

- Practice profile or provisional profile assumptions.
- Client needs intake and source date.
- Coverage gap analysis.
- Existing policy summaries, if any.
- Candidate solution categories and any source-backed product facts.
- Budget, affordability notes, goals, constraints, and exclusions.
- Jurisdiction/license scope.
- Source hierarchy: contract/rider first, then carrier official source, then approved brochure/script.

## Method

1. Start by listing confirmed facts, missing facts, and assumptions.
2. Summarize current coverage without implying status unless verified.
3. Convert needs into possible solution categories before product facts.
4. If candidate products are mentioned, cite source level and use `[verify]` where not contract/carrier-confirmed.
5. Separate internal agent notes from customer-safe language.
6. Include replacement/surrender/lapse flags if existing coverage could be affected.
7. End with next questions and review gates.

## Output Format

```markdown
## Scope
- Workflow:
- Jurisdiction/license context:
- Sources reviewed:
- Review owner:

## Customer Profile Snapshot
- ...

## Confirmed Needs
- ...

## Missing Facts / Must Ask
- ...

## Current Coverage Snapshot
- ... [verify]

## Gap Summary
- ...

## Candidate Solution Categories
- Category:
  - Why it may be relevant:
  - Facts needed before recommendation:

## Product / Source Caveats
- ... [verify against contract/carrier source]

## Compliance / Escalation Flags
- ...

## Customer-Safe Summary Draft
> Draft for licensed/compliance review.

...

## Internal Agent Notes
- ...

## Next Questions
1. ...
```

## Guardrails

- Do not say a product is best, guaranteed, risk-free, or certain to be approved/paid.
- Do not recommend cancellation, surrender, replacement, or reduction of existing coverage.
- Do not hide missing facts or internal risk flags from the agent copy.
- Do not rely on marketing material as if it were contract language.
- Do not produce customer-use copy without review-owner language.
