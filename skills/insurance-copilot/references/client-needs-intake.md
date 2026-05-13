# Client Needs Intake

Use this skill to turn messy notes or a conversation into a structured insurance fact-find.

## Safety Rule

Do not recommend products from incomplete facts. If facts are missing, produce questions first.

## Required Inputs

Collect or mark unknown:

- Customer name/household.
- Age/date of birth.
- Jurisdiction/residency.
- Family status and dependents.
- Income and monthly obligations.
- Assets, debts, mortgage, business obligations.
- Existing insurance policies: type, carrier, coverage amount, premium, term, riders, exclusions if known.
- Health disclosures and underwriting-sensitive facts, using only approved collection language.
- Budget and premium comfort range.
- Goals: protection, medical expense, family income replacement, education, retirement, estate, business continuity.
- Time horizon and liquidity needs.
- Risk tolerance where relevant.

## Output Format

```markdown
## Intake Summary

### Known Facts
- ...

### Missing / Must Ask Before Recommendation
- ...

### Preliminary Need Areas
- High priority:
- Medium priority:
- Low priority:

### Compliance / Sensitivity Flags
- ...

### Suggested Next Questions
1. ...
```

## Guardrails

- Do not ask the agent to collect unnecessary sensitive data.
- Do not advise the client to hide or soften health disclosures.
- Flag if the user is trying to jump to a product without adequate facts.
- Mark uncertain facts as `[verify]`.
