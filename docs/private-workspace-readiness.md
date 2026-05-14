# Private Workspace Readiness Gate

The Private Workspace Readiness Gate is a deterministic, read-only preflight check before a private agent workspace is connected to the local connector, renewal watcher, or script-only Hermes cron wrapper.

It answers:

```text
Is this workspace structurally ready, fresh enough, privacy-safe enough, and retention/audit-aware enough for a scheduled watcher dry run?
```

It does **not** approve production use by itself.

## Command

```bash
python3 scripts/private_workspace_readiness.py \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --format markdown
```

JSON form:

```bash
python3 scripts/private_workspace_readiness.py \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --format json
```

Use `--synthetic-mode` for template/demo workspaces where any PII-like pattern should be a blocker.

## Output Shape

Markdown reports include:

- `Private Workspace Readiness Report`
- `Readiness Verdict`
- `Workspace Structure`
- `Renewal Register Freshness`
- `Privacy / PII Scan`
- `Output Boundary`
- `Retention / Audit Checklist`
- `Scheduled Watcher Deployment Gate`
- `Recommended Next Actions`
- `No External Writes`

JSON reports include:

```json
{
  "ready_for_cron": false,
  "internal_only": true,
  "no_external_writes": true,
  "summary": {},
  "checks": [],
  "risks": [],
  "recommended_next_actions": []
}
```

The script exits:

- `0` when there are no blocker risks;
- `1` when a report was generated but the workspace is not ready;
- `2` for CLI/config errors such as missing workspace or unsafe output path.

## Checks

### Workspace structure

Required directories:

```text
clients/
meetings/
policies/
claims/
referrals/
tasks/
renewal-registers/
```

Required file:

```text
README.md
```

### Renewal register freshness

The readiness gate scans regular in-workspace `renewal-registers/*.csv` files and checks required renewal fields, row presence, parseable `status_as_of` dates, and freshness for every row against:

```text
--as-of YYYY-MM-DD
--max-stale-days 7
```

Any stale, blank, invalid, or future-dated row blocks scheduled watcher readiness because renewal/lapse alerts depend on current carrier/payment status for each monitored policy. This does not mean coverage is active or lapsed; it means the source is not ready for automated monitoring.

### Privacy / PII scan

The script performs a basic deterministic scan for high-risk PII-like patterns such as SSN-like, credit-card-like, and email-like strings in text files. This is a guardrail, not a complete DLP system.

In `--synthetic-mode`, PII-like hits are blockers. Outside synthetic mode, they are warnings because real private workspaces may intentionally contain customer data under approved private controls.

### Retention / audit checklist

Before scheduled monitoring, the private workspace should contain retention/audit guidance such as:

```text
RETENTION.md
AUDIT.md
log.md
```

The readiness gate expects a retention/audit policy plus `log.md` before a workspace is considered ready for cron deployment.

### Symlink and path boundary

Required directories/files, renewal registers, retention/audit files, and scanned text files must be regular in-workspace paths. Symlinked required paths are rejected or skipped so the validator does not read private data outside the declared workspace.

### Output boundary

The readiness script writes to stdout by default. If `--output` is provided, the output path must be outside the workspace and must not be the same file/hardlink as any workspace source file, to avoid contaminating or overwriting private source records with generated reports.

## Safety Boundary

The readiness gate is read-only. It does not:

- create a live Hermes cron job;
- send customer messages;
- write CRM/calendar tasks;
- contact carriers or portals;
- file claims;
- submit applications;
- change policies;
- delete or mutate private workspace files.

## Relationship to Script-only Cron Wrapper

Run this readiness gate before using:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --mode alert-only
```

A future deployment sequence should be:

```text
private workspace readiness report
→ fix blockers
→ private dry-run deployment harness
→ review manifest and deployment checklist
→ script-only cron wrapper dry run with no delivery if needed
→ reviewed Hermes no_agent=True scheduled job
```

Do not create a live job until reviewer, schedule, timezone, retention/audit policy, and data boundary are approved.

For the one-command deployment preflight, see `docs/private-dry-run-harness.md`.
