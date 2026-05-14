# Renewal Watcher Cron Recipe

Use Hermes cron to periodically review a renewal register exported by the agency.

## Purpose

Identify policies with due, grace-period, lapse, or review windows in the next 30 days. Produce internal draft actions only.

## Required Inputs

- Renewal register path.
- Practice profile path if available.
- Approved outreach template path if available.

## Recommended Prompt

```text
Load the insurance-copilot skill. Review the renewal register at <path>. Identify policies with due, grace-period, lapse, or review windows in the next 30 days. Produce internal draft outreach only. Mark all carrier status as [verify with carrier] unless the register includes a current carrier source timestamp. Do not send customer messages. Escalate lapse, reinstatement, complaint, vulnerable-customer, or status-ambiguity issues.
```

## Required Toolsets

- `file`
- optional `web` only for public regulator/carrier source checks when approved

## Safety

- No automatic customer sending.
- No statement that coverage is active unless verified.
- No policy changes.
- Output must list human review owner.
