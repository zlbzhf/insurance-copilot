# Local Renewal Watcher Review

## What improved

- Added `scripts/renewal_watcher.py`, a deterministic internal-only watcher for renewal/lapse rows.
- Supports connector JSON and direct renewal-register CSV input.
- Adds TDD coverage for Markdown/JSON output, missing input, symlink/outside input, and output-inside-workspace rejection.
- Produces scheduled-agent-ready alerts without creating a live cron job.
- Documents no-customer-send, no-CRM-write, and carrier-status `[verify]` boundaries.
- Adds eval, examples, validator, and CI hooks so the watcher cannot disappear silently.

## Comparison to the managed-agent gap

This phase moves the project beyond static workflow templates and local connector bundles into a first scheduled-monitor-shaped module:

```text
renewal register / connector bundle
→ deterministic watcher
→ internal alert
→ optional future Hermes scheduled summary
```

It is still intentionally below production automation: it does not send messages, update systems, or verify carrier status.

## Remaining weaknesses

- No live Hermes cron job is created yet.
- No CRM/calendar/carrier connector exists.
- Alerts are deterministic but not yet enriched by a live model summary.
- No institution-specific AIA/友邦 public renewal process pack has been added.
- No audit log, retention policy implementation, or role-based access layer exists.

## Recommended next phase

Add a safe script-only cron wrapper template and optional Hermes cron creation guide for a synthetic/local private workspace. Keep `no_agent=True` for deterministic alerts first; only add LLM summarization after reviewer approval. If creating scheduled summaries, use per-job model override `custom:fufu` / `mimo-v2.5-pro` when desired, without changing global model configuration.
