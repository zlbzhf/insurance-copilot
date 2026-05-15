# Private Dry-Run Deployment Harness

## Expected Result

The harness produces a complete local diagnostic bundle before any live Hermes scheduled watcher is created. Review it through the **Private Workspace Trace and Readiness Gate** before any future scheduling discussion.

## Required Artifacts

- readiness report
- Daily Agent Workbench connector bundle
- internal renewal watcher alert
- cron wrapper simulation
- Private Workspace Audit Trace (`audit-trace.json` and `audit-trace.md`)
- manifest with artifact checksums
- deployment checklist

## Private Workspace Audit Trace

- The trace is an **audit-style trace** for a **read-only local/private workspace connector** and **readiness gate dry-run**.
- The connector records `source_trace` as **metadata/checksums only**: relative path, operation, boundary, size, and SHA-256.
- Private source content is not copied into the trace.
- `read_only_verified` must be present and true before any readiness claim.
- `workspace_unchanged` must be present and true before any readiness claim.

## Safety Boundary

- `live_cron_created: false`.
- No live cron job is created.
- No live automation is authorized by this dry run.
- no live automation remains the default until separately approved.
- No customer message is sent.
- No CRM/calendar task is written.
- No carrier portal is contacted.
- No claim/application/policy-change action is performed.
- No External Writes.
- The checklist remains a draft for licensed/compliance/operations review before any scheduled watcher deployment.

## Readiness Gate

If readiness has blockers, the dry run should still generate diagnostics but must not mark `ready_for_scheduled_watcher` true.
