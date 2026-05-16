# Renewal Watcher Cron Recipe

Use Hermes cron to periodically review a renewal register exported by the agency. Start with the deterministic local watcher in `scripts/renewal_watcher.py`; only add an LLM summary layer after the internal alert format is accepted by the servicing agent and compliance reviewer.

## Purpose

Identify policies with due, grace-period, lapse, or review windows in the next 30 days. Produce internal draft actions only.

## Required Inputs

- Private workspace path or renewal register path.
- Practice profile path if available.
- Approved outreach template path if available.
- Named reviewer for lapse/grace/ambiguous-status escalation.

## Deterministic Command

```bash
python3 scripts/local_file_connectors.py daily-workbench \
  --workspace ~/.insurance_copilot/agents/<agent-id> \
  --format json \
  --output /tmp/insurance-workbench-bundle.json

python3 scripts/renewal_watcher.py \
  --bundle /tmp/insurance-workbench-bundle.json \
  --workspace ~/.insurance_copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --format markdown \
  --output /tmp/insurance-renewal-alert.md
```

## Recommended Prompt

```text
Load the insurance_copilot skill. Summarize the internal renewal watcher alert at <path>. Identify policies with due, grace-period, lapse, or review windows in the next 30 days. Produce internal draft outreach only. Mark all carrier status as [verify with carrier] unless the register includes a current carrier source timestamp. Do not send customer messages. Escalate lapse, reinstatement, complaint, vulnerable-customer, replacement, or status-ambiguity issues.
```

For scheduled update/check/report summaries, a per-job model override such as `custom:fufu` / `mimo-v2.5-pro` may be used without changing global Hermes model configuration.

## Required Toolsets

- `file` or `terminal` for deterministic script reads.
- optional `web` only for public regulator/carrier source checks when approved.

## Safety

- No automatic customer sending.
- No statement that coverage is active unless verified.
- No policy changes.
- No CRM/calendar writes in this watcher.
- Output must list human review owner.
