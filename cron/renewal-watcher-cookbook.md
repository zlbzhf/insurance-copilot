# Renewal Watcher Cookbook

Use this cookbook to convert the renewal/lapse workflow into a reviewed Hermes cron job. This is a planning artifact; do not deploy against production data without compliance approval.

## Scope

- **Input:** private renewal register CSV or read-only connector output with policy ref, due date, grace period end, carrier status source, status timestamp, last contact, and review flags.
- **Cadence:** daily on business mornings, or more frequently only with supervisor approval.
- **Output:** internal alert with urgent renewals/lapse risks, `[verify]` status notes, draft customer outreach language, and task export draft.
- **Review owner:** servicing agent; supervisor/compliance for grace-period, lapse, vulnerable customer, complaint, or ambiguous status.

## Forbidden Actions

- No automatic customer messages.
- No CRM/calendar writes unless a separate reviewed side-effect job is approved.
- No statements that coverage is active/lapsed/reinstated without current carrier verification.
- No promises of reinstatement, claim validity, premium savings, or policy continuation.

## Prompt Skeleton

```text
Load insurance-copilot. Use Renewal/Lapse Follow-up Planner on the private renewal register supplied by the script output. Prioritize D-30, D-14, D-7, D+1, and grace-period-before-end items. Mark carrier status [verify] unless source and timestamp are current. Produce internal tasks and draft customer language only; do not send or write anything automatically.
```

## Handoff Gate

Before any external use, the servicing agent must verify carrier status, payment status, contact consent, approved script source, and whether compliance/supervisor escalation is required.
