# Practical MVP Example: Professional Review Gate

This synthetic example shows how the review-gate pattern from professional-service copilots is translated into insurance-agent daily work.

## Input

```text
Use Daily Agent Workbench. I have three items today:
1. A customer wants a WeChat reply about a possible claim delay.
2. Another customer may replace an old policy but I only have a brochure for the new product.
3. Please put the follow-up tasks into CRM/calendar if possible.
```

## Expected Assistant Behavior

The assistant should route to Daily Agent Workbench and apply **Professional Review Gate** before any customer-facing or external-use output.

## Draft Output Sketch

## Professional Review Gate
- Workflow: Daily Agent Workbench + Claims Support Triage + Replacement Risk Triager as needed.
- Action class: Class 2 regulated decision-support for claim/replacement items; Class 3 external side effect for CRM/calendar write request.
- Review owner: licensed servicing agent; compliance/supervisor for replacement-adjacent item; claims specialist or carrier claims team for claim-support item.
- Source verification status: policy, claim status, replacement comparison, and product facts are `[verify]`; brochure is not contract evidence.
- Customer-facing approval status: draft for licensed/compliance review; not approved to send.
- Side-effect status: no external action is authorized; CRM/calendar output is a task export draft only.
- Customer-first advocacy status: provide evidence requests, source checks, escalation path, and customer-safe language rather than stopping at `以保险公司审核为准`.
- Minimum safe next step: verify source documents, name the review owner, then prepare reviewed customer-safe drafts.

## Notes

- Do not send messages automatically.
- Do not write CRM/calendar tasks automatically.
- Do not recommend replacement, claim outcome, coverage status, or approval.
- Do keep the customer supported through concrete evidence collection and escalation.
