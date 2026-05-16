# Daily Agent Workbench

Use this workflow when an insurance professional wants a practical daily operating plan across meetings, open follow-ups, renewal/lapse windows, claim-support items, referrals, and customer-facing draft messages.

This workflow is intentionally operational, but it is still draft-only. It may prepare task lists and message drafts; it must not send messages, update CRM/calendar systems, change policy status, file claims, or represent carrier status without verification.

## Inputs

- Practice profile status and review owner.
- Today's date and working hours.
- Meetings or appointments.
- Open follow-ups and last contact notes.
- Renewal/lapse register or due-date notes.
- Claim/support items and document deadlines.
- Referral opportunities or thank-you follow-ups.
- Draft messages needing compliance review.
- Source timestamps for policy status, payment status, claim status, and product facts.

## Method

1. Confirm the practice profile exists. If not, use only generic prioritization and ask to run Agency Playbook Builder.
2. Normalize all items into: meeting, follow-up, renewal/lapse, claim, referral, compliance-copy, admin, or unknown.
3. Flag high-risk items first: lapse/grace-period, replacement/surrender, complaint, claim deadline, vulnerable customer, investment-linked/cash-value language, unverified policy status, or customer-facing guarantee language.
4. Draft internal next actions before customer messages.
5. Create customer-facing draft talk tracks only as licensed/compliance review drafts.
6. Mark all unverified policy/payment/claim/product facts as `[verify]`.
7. Produce a CRM/calendar task export draft without writing to any system.

## Output Format

```markdown
## Scope
- Date:
- Practice profile:
- Sources reviewed:
- Review owner:

## Today's Priorities
1. ...

## High-Risk Items
- ...

## Customer Follow-ups
- Customer/ref:
  - Reason:
  - Suggested next action:
  - Source status:

## Draft Talk Tracks
> Draft for licensed/compliance review; do not send automatically.

- ...

## Verify Before Action
- [verify] ...

## CRM/Calendar Task Export Draft
- Task:
  - Owner:
  - Due:
  - Notes:
  - No automatic write:

## Escalation / Review Gates
- ...
```

## Guardrails

- Do not automatically send, schedule, or write anything.
- Do not state coverage is active, paid, lapsed, reinstated, or claim-approved unless a current carrier source is supplied; even then cite the source and timestamp.
- Do not pressure vulnerable, distressed, grieving, or financially stressed customers.
- Do not draft replacement/surrender/cancellation language except as high-risk internal triage and compliance-review draft.
- Do not mix internal risk notes into a customer-safe message.
