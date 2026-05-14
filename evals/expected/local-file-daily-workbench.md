# Daily Agent Workbench Connector Bundle

> Draft for licensed/compliance review; do not send, schedule, or write externally.

## Scope
- Workspace: `synthetic-agent-workspace`
- Connector mode: read-only local files
- Review owner: licensed agent; compliance reviewer for customer-facing/high-risk items

## Today's Priorities
1. Review high-risk renewal/lapse, claim, policy-status, or replacement-sensitive items first.
2. Prepare for 1 meeting(s) using missing-fact questions before product discussion.
3. Verify 1 renewal/payment item(s) against carrier source before outreach.
4. Review 1 referral item(s) for consent, incentive, and channel restrictions.
5. Convert 1 private task list(s) into reviewed CRM/calendar draft tasks only.

## High-Risk Items
- Renewal/lapse: SYN-POLICY-001 for SYN-CUSTOMER-001 — status [verify]; possible lapse risk
- Claim support: SYN-CLAIM-001 — do not promise coverage or payout; verify carrier instructions.
- Policy review: SYN-POLICY-001 — source/status needs verification before customer statements.

## Renewal / Lapse Items
- Policy: SYN-POLICY-001 / Customer: SYN-CUSTOMER-001
  - Premium due: 2026-05-20
  - Grace period end: 2026-06-20
  - Status source: [verify]
  - Next action: verify payment status before outreach

## Customer / Meeting / Policy Inputs
### Customers
- SYN-CUSTOMER-001 (`clients/SYN-CUSTOMER-001.md`) — type: customer
### Meetings
- SYN-MEETING-001 (`meetings/SYN-MEETING-001.md`) — type: meeting-note
### Policies
- SYN-POLICY-001 (`policies/SYN-POLICY-001.md`) — type: policy-summary
### Claims
- SYN-CLAIM-001 (`claims/SYN-CLAIM-001.md`) — type: claim-tracker
### Referrals
- SYN-REFERRAL-001 (`referrals/SYN-REFERRAL-001.md`) — type: referral-tracker
### Tasks
- SYN-TASKS (`tasks/SYN-TASKS.md`) — type: task-list

## Draft Talk Tracks
> Draft for licensed/compliance review; do not send automatically.

- Renewal reminder draft: Please verify the official carrier/payment status before telling the customer anything about coverage, grace period, or lapse.
- Claim support draft: I can help organize documents and carrier instructions, but final coverage or payout depends on carrier claim review.
- Referral draft: Use only low-pressure opt-out language after consent and incentive rules are verified.

## Verify Before Action
- [verify] carrier policy/payment/claim status before any customer statement.
- [verify] approved script or practice profile before sending customer-facing copy.
- [verify] referral consent and incentive/anti-rebating rules before referral outreach.

## CRM/Calendar Task Export Draft
- Task:
  - Owner: assigned agent
  - Due: [verify]
  - Notes: Review high-risk renewal/lapse, claim, policy-status, or replacement-sensitive items first.
  - External write allowed: no, draft only.
- Task:
  - Owner: assigned agent
  - Due: [verify]
  - Notes: Prepare for 1 meeting(s) using missing-fact questions before product discussion.
  - External write allowed: no, draft only.
- Task:
  - Owner: assigned agent
  - Due: [verify]
  - Notes: Verify 1 renewal/payment item(s) against carrier source before outreach.
  - External write allowed: no, draft only.
- Task:
  - Owner: assigned agent
  - Due: [verify]
  - Notes: Review 1 referral item(s) for consent, incentive, and channel restrictions.
  - External write allowed: no, draft only.
- Task:
  - Owner: assigned agent
  - Due: [verify]
  - Notes: Convert 1 private task list(s) into reviewed CRM/calendar draft tasks only.
  - External write allowed: no, draft only.

## No External Writes
- This connector only reads local files and emits a bundle.
- It does not send messages, update CRM/calendar, contact carriers, file claims, submit applications, or change policies.
