# Private Dry-Run Deployment Checklist

Draft for licensed/compliance/operations review.

## Verdict
- Blocked before scheduled watcher deployment
- As of: `2026-05-14`
- Workspace: `/root/insurance-agent-assistant/examples/local-connectors/synthetic-agent-workspace`
- Read-only: true
- No External Writes: true
- Live Hermes cron created: false

## Artifacts to Review
- `readiness-report.md`
- `readiness-report.json`
- `workbench-bundle.json`
- `workbench-bundle.md`
- `renewal-alert.json`
- `renewal-alert.md`
- `cron-simulation.md`
- `manifest.json`
- `deployment-checklist.md`

## Gate Checks
- Readiness: blocked (exit 1)
- Connector bundle: ok (exit 0)
- Renewal watcher: ok (exit 0)
- Cron wrapper simulation: ok (exit 0)

## Before Any Live Scheduled Job
- Resolve all readiness blockers.
- Confirm schedule, timezone, delivery target, reviewer, and retention/audit owner.
- Keep any future Hermes job `no_agent=True` unless an explicitly reviewed summary job is added.
- If an LLM summary job is later added, use per-job model override `custom:fufu` / `mimo-v2.5-pro` instead of changing global model config.
- Preserve `[verify]` markers and internal-only wording.

## Safety Boundary
- This dry run did not create a live Hermes cron job.
- It did not send customer messages, write CRM/calendar tasks, contact carriers, file claims, submit applications, or change policies.
- No External Writes.

## Readiness Risks
- blocker / missing-renewal-status-date: renewal-registers/synthetic-renewal-register.csv row 2 policy SYN-POLICY-001 has blank status_as_of
- blocker / missing-retention-audit-policy: missing regular in-workspace RETENTION.md/AUDIT.md with retention and audit guidance, or missing regular in-workspace log.md
