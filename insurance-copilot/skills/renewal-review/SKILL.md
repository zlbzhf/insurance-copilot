---
name: renewal-review
description: Review renewal, lapse, payment, and policy-review deadlines.
---

# Renewal Review

Use this skill for customer service and retention workflows.

## Inputs

- Policy list or renewal register.
- Premium due dates.
- Grace periods/lapse dates.
- Renewal windows.
- Customer notes.
- Communication history.

## Output Format

```markdown
## Renewal / Lapse Review

### Urgent Actions
- Policy/customer:
- Deadline:
- Risk:
- Suggested next action:

### Upcoming Reviews
- 0-14 days:
- 15-30 days:
- 31-90 days:

### Draft Customer Outreach
- Subject/message:
- Required disclaimer:

### Internal Notes
- Missing data:
- Escalations:
```

## Guardrails

- Do not represent that coverage remains active unless verified from carrier source.
- Be careful with lapse/reinstatement statements; mark `[verify with carrier]`.
- Do not pressure the customer with misleading urgency.
