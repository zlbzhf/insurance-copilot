# Script-only Cron Wrapper Review

## Scope Reviewed

This review covers the `Scheduled Managed Agents Layer v0.2` slice:

```text
cron/scripts/renewal_watcher.sh
scripts/local_file_connectors.py
scripts/renewal_watcher.py
tests/test_renewal_watcher_cron_wrapper.py
docs/script-only-cron-wrapper.md
examples/cron/renewal-watcher-no-agent.md
cron/renewal-watcher-cookbook.md
```

## What Improved

- Added a single checked wrapper command for future Hermes `no_agent=True` cron deployment.
- Preserved deterministic local execution: no LLM is required for the watchdog itself.
- Added silent/no-alert semantics for monitor-only rows: empty stdout and exit `0`.
- Added fail-loud behavior for broken configuration: non-zero exit with stderr.
- Kept generated connector/report artifacts in a temporary directory outside the workspace.
- Rejected explicit output paths inside the private workspace.
- Added tests for source workspace non-mutation.
- Added docs explaining `no_agent=True`: non-empty stdout delivers, empty stdout is silent, non-zero exit alerts.
- Documented optional LLM summary jobs with per-job `custom:fufu` / `mimo-v2.5-pro` override without changing global Hermes config.

## Safety Boundaries Confirmed

The wrapper does not:

- send customer messages;
- write CRM/calendar tasks;
- contact carriers or external portals;
- file claims;
- submit applications;
- alter policies;
- write outputs into the private workspace;
- create a live Hermes cron job.

## Remaining Weaknesses

- The wrapper is still local-file only; it does not connect to production CRM/carrier/calendar systems.
- It relies on CSV/source quality; carrier/payment status remains `[verify]` until an official source is checked.
- It does not include per-agent retention/audit policy enforcement.
- It does not implement a paired LLM summary job; that should remain a separately approved sidecar.
- It has no timezone-aware scheduler config because this phase deliberately avoids creating a live cron job.

## Next Phase Recommendation

Next useful large-module iteration:

```text
Private Workspace Validator + Retention/Audit Pack
```

That would add checks for required private workspace structure, stale source timestamps, synthetic-vs-private data separation, retention guidance, and a dry-run report before any live scheduled watcher is created.

## Verdict

This slice meets the plan: it upgrades the renewal watcher from a manual command to a script-only watchdog template suitable for later Hermes cron deployment while preserving read-only, internal-only, no-external-write boundaries.

## Independent review fix-ups

A pre-commit review identified three issues and they were fixed before commit:

- `TMPDIR` could have pointed inside the private workspace; the wrapper now resolves and rejects workspace-local `TMPDIR`, with regression coverage.
- Child command failures could have been silent because stdout was redirected; the wrapper now captures child output and emits a fail-loud stderr block, with invalid `--as-of` regression coverage.
- Docs previously suggested copying only the shell script to `~/.hermes/scripts/`; docs now require preserving repo-relative helper script access or using a project workdir.
