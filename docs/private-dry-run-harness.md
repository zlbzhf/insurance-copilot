# Private Dry-Run Deployment Harness

Runtime gate: **Private Workspace Trace and Readiness Gate** for the **Private Workspace Audit Trace**. It reviews the **read-only local/private workspace connector**, **readiness gate dry-run**, **audit-style trace**, `source_trace`, `read_only_verified`, `workspace_unchanged`, **metadata/checksums only**, **No External Writes**, `live_cron_created: false`, and **no live automation**.

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
audit-trace.json
audit-trace.md
manifest.json
deployment-checklist.md
```

The audit trace artifacts are runtime-effective safeguards for the read-only/private boundary:

- `audit-trace.json`: Machine-readable audit-style trace with `read_only_verified`, `workspace_unchanged`, stage ledger, readiness gate dry-run summary, source inventory before/after checksums, connector `source_trace`, and boundary ledger.
- `audit-trace.md`: Human-readable trace summary for licensed/compliance/operations review before any live scheduled watcher decision.
- `manifest.json` / `deployment-checklist.md`: Final readiness verdict, artifact checksums, review steps, and deployment boundary.

`manifest.json` records:

- workflow name;
- workspace and as-of date;
- `ready_for_scheduled_watcher` must be computed after audit trace review and requires `read_only_verified: true` plus `workspace_unchanged: true`; otherwise the gate remains blocked.
- `read_only: true`;
- `read_only_verified` from the audit trace;
- `workspace_unchanged` from the audit trace;
- `no_external_writes: true`;
- `live_cron_created: false`;
- stage statuses and exit codes;
- artifact paths, sizes, and SHA-256 checksums for all non-manifest artifacts.

Because `manifest.json` is self-referential, its own checksum and final byte size are recorded as unstable/not recorded: `sha256: self-referential-not-recorded`, `checksum_recorded: false`, `size_bytes: null`, and `size_recorded: false`; all other artifact sizes and checksums are verifiable SHA-256 values.

## Exit Semantics

```text
exit 0 = dry run complete and readiness gate is ready
exit 1 = dry run complete, artifacts generated, but readiness blocks scheduled watcher deployment
exit 2 = CLI/config/child-command error; inspect stderr
```

A readiness blocker is not treated as a broken dry run. The harness still produces the connector bundle, watcher outputs, cron simulation, audit trace, manifest, and checklist so the agent can diagnose blockers.

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

- `audit-trace.json` records `read_only_verified`, `workspace_unchanged`, `source_inventory`, and `connector_source_trace` as metadata/checksums only;
- private source content is not copied into the audit trace;
- before/after workspace checksums must match before the manifest reports `read_only_verified: true`;
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

1. `manifest.json` has `ready_for_scheduled_watcher: true`, computed only after `audit-trace.json` is generated.
2. `manifest.json` has `read_only_verified: true` and `workspace_unchanged: true` from the audit trace; if either is false, `ready_for_scheduled_watcher` must remain false even when child stages exit `0`.
3. `audit-trace.json` / `audit-trace.md` have been reviewed for source inventory, stage ledger, boundary ledger, and metadata-only private source handling.
4. `deployment-checklist.md` is reviewed by the responsible agent/operations owner.
5. Schedule, timezone, delivery target, reviewer, and retention/audit owner are approved.
6. The future Hermes job is explicitly reviewed as script-only `no_agent=True`, or any LLM summary job is separately reviewed.
7. If a future LLM summary job is added, use the per-job model override `custom:fufu` / `mimo-v2.5-pro` instead of changing global Hermes model configuration.

## Example Output

See:

```text
examples/private-dry-run/synthetic-manifest.json
examples/private-dry-run/synthetic-deployment-checklist.md
```

The committed synthetic fixture is intentionally not ready because it lacks the full retention/audit readiness expected for scheduled deployment. That is useful: the dry run demonstrates complete diagnostics without falsely approving a watcher.
