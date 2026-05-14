# Private Dry-Run Deployment Harness

## Expected Result

The harness produces a complete local diagnostic bundle before any live Hermes scheduled watcher is created.

## Required Artifacts

- readiness report
- Daily Agent Workbench connector bundle
- internal renewal watcher alert
- cron wrapper simulation
- manifest with artifact checksums
- deployment checklist

## Safety Boundary

- `live_cron_created: false`.
- No live cron job is created.
- No customer message is sent.
- No CRM/calendar task is written.
- No carrier portal is contacted.
- No claim/application/policy-change action is performed.
- No External Writes.
- The checklist remains a draft for licensed/compliance/operations review before any scheduled watcher deployment.

## Readiness Gate

If readiness has blockers, the dry run should still generate diagnostics but must not mark `ready_for_scheduled_watcher` true.
