# Claims Triage

Use this workflow when the user asks about a possible claim, claim status, claim documentation, denial, appeal, or coverage question. This workflow helps organize information; it does not decide claims.

## Boundary

Do not state that a claim is covered, payable, denied correctly, or guaranteed. Claims decisions belong to the carrier/claims administrator and applicable review/appeal process.

## Required Inputs

- Policy source and relevant coverage section if available.
- Loss/event date and high-level event description.
- Claim status, if any.
- Carrier claim instructions or correspondence.
- Deadlines and required documents.
- Jurisdiction if relevant.

## Review Procedure

1. Identify the type of claim or question.
2. Extract known facts and documents received.
3. Identify missing documents and deadlines.
4. Separate policy-language facts from assumptions.
5. Draft a neutral checklist or customer service script.
6. Escalate complaints, denials, deadlines, vulnerable customers, or legal threats.

## Output Format

```markdown
## Claims Triage

### Scope
- Claim/question type:
- Policy/source(s):
- Status:

### Known Facts
- ...

### Missing Documents / Deadlines
- ...

### Policy / Carrier Source Points To Verify
- ...

### Draft Customer Service Language
[neutral draft; no coverage or payout guarantee]

### Escalation Flags
- ...
```

## Guardrails

- Do not guarantee claims payout or coverage.
- Do not advise customer to alter facts or documentation.
- Do not provide legal advice about disputes or appeals.
- Mark coverage interpretations `[verify with carrier/claims specialist]` unless authoritative source and licensed review are provided.
- Escalate denials, complaints, deadlines, suspected fraud, or legal threats.
