# Replacement Risk Monitor Cron Recipe

Use Hermes cron or a manual workflow to scan internal notes for cancellation, surrender, replacement, exchange, rebating, twisting/churning, or high-pressure indicators.

## Recommended Prompt

```text
Load the insurance_copilot skill. Review notes under <path> for replacement/surrender/cancellation risk indicators. Produce an internal escalation candidate list with source file, quoted phrase, risk category, and recommended next review step. Do not make compliance findings or contact customers.
```

## Safety

- Findings are candidates, not final compliance determinations.
- No customer contact.
- No policy changes.
- Escalate all confirmed replacement/surrender/cancellation scenarios.
