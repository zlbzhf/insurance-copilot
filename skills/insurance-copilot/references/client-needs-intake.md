# Client Needs Intake

Use this workflow to turn messy notes, chat transcripts, call notes, or a conversation into a structured insurance fact-find. It is the default first substantive workflow before needs analysis or product review.

## Safety Rule

Do not recommend products from incomplete facts. If material facts are missing, produce questions first and label product discussion as premature.

## Required Inputs

Collect or mark unknown:

- Customer name/household or de-identified label.
- Jurisdiction/residency.
- Age/date of birth or age band where appropriate.
- Family status and dependents.
- Income and monthly obligations.
- Assets, debts, mortgage, business obligations.
- Existing insurance policies: type, carrier, coverage amount, premium, term, riders, exclusions if known.
- Employer/group benefits where relevant.
- Health disclosures and underwriting-sensitive facts, using only approved collection language.
- Budget and premium comfort range.
- Goals: protection, medical expense, family income replacement, education, retirement, estate, business continuity.
- Time horizon and liquidity needs.
- Risk tolerance where relevant.
- Preferred communication language and channel.

## Sensitive Data Collection Rules

Use minimum necessary data. Do not ask for government ID numbers, full medical records, payment details, or other unnecessary PII unless the user confirms it is required for a specific licensed workflow.

Safer phrasing:

- "Are there any health, occupation, travel, hobby, or financial facts the carrier/application would require us to disclose?"
- "Please use your approved application or fact-find form for exact health questions. I can help structure the notes, but I should not rewrite disclosures to make them look better."
- "If this is real customer data, redact identifiers that are not needed for the analysis."

Never suggest hiding, softening, or omitting disclosures.

## Intake Completeness Scoring

Use this scoring to decide whether analysis can proceed:

- **Complete enough for needs analysis:** jurisdiction, dependents/obligations, income/budget, goals, and existing coverage are known or explicitly not applicable.
- **Partial:** enough for preliminary gap questions, but not for product selection.
- **Insufficient:** missing core facts; ask questions only.

## Output Format

```markdown
## Intake Summary

### Completeness
- Complete enough for needs analysis / Partial / Insufficient
- Reason:

### Known Facts
- ...

### Missing / Must Ask Before Recommendation
- ...

### Preliminary Need Areas
- High priority:
- Medium priority:
- Low priority:
- Unknown pending facts:

### Existing Coverage Snapshot
- ...

### Compliance / Sensitivity Flags
- ...

### Suggested Next Questions
1. ...

### Do Not Recommend Yet If
- ...
```

## Guardrails

- Do not ask the agent to collect unnecessary sensitive data.
- Do not advise the client to hide or soften health, financial, claims, or lifestyle disclosures.
- Flag if the user is trying to jump to a product without adequate facts.
- Mark uncertain facts as `[verify]`.
- Do not store real customer PII unless the user explicitly requests and confirms the destination.
