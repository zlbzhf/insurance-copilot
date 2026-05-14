# Renewal Review

Use this workflow for customer service and retention reviews involving renewals, premium due dates, grace periods, lapse risk, reinstatement windows, and scheduled policy reviews.

## Inputs

- Policy list or renewal register.
- Premium due dates.
- Grace periods/lapse dates.
- Renewal windows.
- Carrier status source and timestamp.
- Customer notes.
- Communication history.
- Approved outreach templates.

## Required Register Fields

At minimum, a renewal/lapse register should include:

- customer or de-identified customer ID;
- policy number or masked policy reference;
- carrier;
- policy type;
- premium due date;
- grace period end date if applicable;
- renewal/review date;
- current status source;
- last contact date;
- assigned agent/owner.

If carrier status is missing, mark status `[verify with carrier]`.

## Review Procedure

1. Sort by earliest deadline: lapse/grace period, premium due date, renewal date, review date.
2. Separate urgent service risks from routine review opportunities.
3. Confirm whether status is verified or needs carrier confirmation.
4. Draft internal next actions first.
5. Draft customer outreach only as reviewable language, not as a sent message.
6. Escalate lapses, reinstatements, complaints, vulnerable customers, and coverage-status ambiguity.

## Output Format

```markdown
## Renewal / Lapse Review

### Scope
- Register/source:
- Review date:
- Status verification level:

### Urgent Actions
- Policy/customer:
- Deadline:
- Risk:
- Status verified? Yes/No/[verify with carrier]
- Suggested internal next action:

### Upcoming Reviews
- 0-14 days:
- 15-30 days:
- 31-90 days:

### Draft Customer Outreach
- Subject/message:
- Required disclaimer:
- Do not send until reviewed by:

### Internal Notes
- Missing data:
- Escalations:
```

## Safe Outreach Sequencing

1. Verify status with carrier/source.
2. Confirm the assigned agent and approved channel.
3. Draft customer message with no guarantee that coverage is active.
4. Obtain licensed/compliance review if required.
5. Only send after explicit human approval.

## Guardrails

- Do not represent that coverage remains active unless verified from carrier source.
- Be careful with lapse/reinstatement statements; mark `[verify with carrier]`.
- Do not pressure the customer with misleading urgency.
- Do not automatically send outreach.
- Escalate if lapse, reinstatement, cancellation deadline, complaint, or vulnerable-customer concern appears.


## Operational Cadence

Use these stages when dates are available. If dates or carrier status are missing, mark them `[verify]` and do not make coverage-status statements.

- **D-30:** prepare service review, verify contact details, confirm official due date and amount.
- **D-14:** remind internally, verify payment method/status, prepare low-pressure customer draft if approved.
- **D-7:** escalate unresolved payment/status uncertainty; use only source-verified wording.
- **D+1:** verify whether payment posted before any lapse/grace-period statement.
- **Grace-period-before-end:** high-risk escalation to servicing agent/supervisor; no promise of reinstatement, claim validity, or continued coverage.

## Operational Output Add-on

```markdown
## Renewal/Lapse Timeline
- D-30:
- D-14:
- D-7:
- D+1:
- Grace-period-before-end:

## Carrier Status Verification
- [verify] source:
- [verify] timestamp:

## Internal Task List
- ...

## Customer Draft Language
> Draft for licensed/compliance review; do not send automatically.

...
```
