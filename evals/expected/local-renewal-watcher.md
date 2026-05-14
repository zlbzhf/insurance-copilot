# Internal Renewal Watcher Alert

> Draft for licensed/compliance review; internal alert only. Do not send, schedule, or write externally.

## Scope
- As of: 2026-05-14
- Mode: internal-only renewal/lapse watcher
- Review owner: servicing agent; supervisor/compliance for lapse, grace-period, vulnerable-customer, complaint, or ambiguous-status items

## Summary Counts
- total: 1
- d_30: 0
- d_14: 0
- d_7: 0
- d_plus_1: 0
- grace_period_before_end: 0
- grace_ended: 0
- verify_status: 1

## Alerts
- Bucket: verify-status / Policy: SYN-POLICY-001 / Customer: SYN-CUSTOMER-001
  - Reason: status/review flags require verification
  - Premium due: 2026-05-20
  - Grace period end: 2026-06-20
  - Status source: [verify]
  - Status as of: [verify]
  - Next internal action: verify payment status before outreach
  - Review flags: possible lapse risk

## Draft Internal Follow-up Language
> Draft for licensed/compliance review; do not send automatically.

- Internal note: Verify official carrier/payment status before describing coverage, lapse, grace period, reinstatement, or claim implications to any customer.
- Customer-language placeholder: After verification and approval only, use a neutral reminder that payment/status should be checked with official carrier records; do not imply active, lapsed, or reinstated status.

## Verify Before Action
- [verify] carrier policy/payment status before any customer statement.
- [verify] grace period and lapse/reinstatement rules with official carrier source.
- [verify] approved script source and contact consent before outreach.

## No External Writes
- This watcher only reads local input and emits an internal alert.
- It does not send customer messages, update CRM/calendar, contact carriers, file claims, submit applications, or change policies.
