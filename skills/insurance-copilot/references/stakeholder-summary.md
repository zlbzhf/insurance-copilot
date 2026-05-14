# Stakeholder Summary

Use this workflow after intake, coverage analysis, product review, policy review, renewal review, or compliance check to translate detailed work into the right level of detail for a specific audience.

## Audience Modes

- **Customer:** plain language, no jargon, no pressure, no internal notes, no unsupported recommendation.
- **Agent:** action-oriented, includes missing facts and next questions.
- **Manager:** risk, operational priority, staffing/approval needs.
- **Compliance:** flags, source gaps, approval needs, risky phrases, escalation rationale.

## Redaction and Audience Rules

- Customer versions must remove internal-only notes, risk scoring labels that could confuse, and compliance deliberation language.
- Compliance versions must preserve exact risky phrases and source gaps.
- Manager versions should summarize urgency and business risk without unnecessary PII.
- Agent versions may include next questions and workflow steps, but should still minimize sensitive data.

## Output Format

```markdown
## Stakeholder Summary

### Audience
- Customer / Agent / Manager / Compliance

### 3-Sentence Summary
1. ...
2. ...
3. ...

### Key Takeaways
- ...

### Open Questions
- ...

### Required Review / Approval
- ...

### Audience-Specific Draft
[only include if requested]
```

## Transformation Rules

- Preserve caveats from the source analysis.
- Do not simplify away exclusions, assumptions, or compliance flags.
- If customer-facing, use softer language and label as draft.
- If internal, mark customer-sensitive content and avoid unnecessary PII.
- If compliance-facing, include exact source/citation references where available.

## Guardrails

- Do not convert a cautious analysis into a confident recommendation.
- Do not remove `[verify]` markers unless the source was actually verified.
- Do not include internal-only notes in customer copy.
- Do not imply approval by compliance unless the user provides that approval.
