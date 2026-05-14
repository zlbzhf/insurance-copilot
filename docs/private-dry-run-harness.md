# Private Dry-Run Deployment Harness

The Private Dry-Run Deployment Harness chains the local/private deployment gates before any live Hermes scheduled watcher is created.

```text
private workspace
  -> Private Workspace Readiness Gate
  -> Daily Agent Workbench connector bundle
  -> Internal Renewal Watcher
  -> script-only cron wrapper simulation
  -> manifest + deployment checklist
```

It is designed for the last local review step before a human decides whether to create a future Hermes `no_agent=True` watchdog.

## Run

```bash
python3 scripts/private_dry_run.py \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --out /tmp/insurance-copilot-dry-run
```

For a private workspace:

```bash
python3 scripts/private_dry_run.py \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --out /tmp/insurance-copilot-dry-run-$(date +%F)
```

Optional flags:

```text
--max-stale-days N
--synthetic-mode
--force
```

Use `--synthetic-mode` for committed examples/templates where PII-like fixture patterns should block readiness. Real private workspaces may contain customer data, so PII-like hits are warnings by default there.

## Artifacts

The output directory contains:

```text
readiness-report.md
readiness-report.json
workbench-bundle.json
workbench-bundle.md
renewal-alert.json
renewal-alert.md
cron-simulation.md
manifest.json
deployment-checklist.md
```

`manifest.json` records:

- workflow name;
- workspace and as-of date;
- `ready_for_scheduled_watcher`;
- `read_only: true`;
- `no_external_writes: true`;
- `live_cron_created: false`;
- stage statuses and exit codes;
- artifact paths, sizes, and SHA-256 checksums for all non-manifest artifacts.

Because `manifest.json` is self-referential, its own checksum is recorded as `self-referential-not-recorded` with `checksum_recorded: false`; all other artifact checksums are verifiable SHA-256 values.

## Exit Semantics

```text
exit 0 = dry run complete and readiness gate is ready
exit 1 = dry run complete, artifacts generated, but readiness blocks scheduled watcher deployment
exit 2 = CLI/config/child-command error; inspect stderr
```

A readiness blocker is not treated as a broken dry run. The harness still produces the connector bundle, watcher outputs, cron simulation, manifest, and checklist so the agent can diagnose blockers.

## Output Boundary

Generated artifacts must stay outside the private source workspace.

The harness rejects:

- symlinked workspace roots;
- `--out` inside the workspace;
- `--out` samefile/hardlink aliases to any workspace source file;
- symlinked output paths;
- existing non-empty output directories unless `--force` is supplied.

This prevents generated reports from being re-ingested as private source records or overwriting source files.

## Safety Boundary

The harness is read-only with respect to the private workspace and keeps the same action-safety posture as the underlying connector/watcher:

- no live Hermes cron job is created;
- no `cronjob(action='create')` is called;
- no customer message is sent;
- no CRM/calendar task is written;
- no carrier portal is contacted;
- no claim is filed;
- no application is submitted;
- no policy is changed, cancelled, surrendered, or replaced;
- No External Writes.

## Before Creating a Live Scheduled Watcher

Only proceed after:

1. `manifest.json` has `ready_for_scheduled_watcher: true`.
2. `deployment-checklist.md` is reviewed by the responsible agent/operations owner.
3. Schedule, timezone, delivery target, reviewer, and retention/audit owner are approved.
4. The future Hermes job is explicitly reviewed as script-only `no_agent=True`, or any LLM summary job is separately reviewed.
5. If a future LLM summary job is added, use the per-job model override `custom:fufu` / `mimo-v2.5-pro` instead of changing global Hermes model configuration.

## Example Output

See:

```text
examples/private-dry-run/synthetic-manifest.json
examples/private-dry-run/synthetic-deployment-checklist.md
```

The committed synthetic fixture is intentionally not ready because it lacks the full retention/audit readiness expected for scheduled deployment. That is useful: the dry run demonstrates complete diagnostics without falsely approving a watcher.
