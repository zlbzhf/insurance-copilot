# Private Workspace Audit Trace Template

Use with `references/private-workspace-trace-readiness.md` and this runtime template path `templates/private-workspace-audit-trace.md` when reviewing a read-only local/private workspace connector, private dry-run output, or readiness gate dry-run. This is a manual-first safeguard for private workspace review, not a live automation template.

## Private Workspace Trace and Readiness Gate

- Workflow:
- Intended use:
- Workspace classification: synthetic / de-identified / real private / unknown
- Review owner:
- Output directory reviewed:
- no live automation decision: no live automation is authorized by this trace
- No External Writes status:
- `live_cron_created: false` status:

## Private Workspace Audit Trace

- Audit artifact reviewed: `audit-trace.json` / `audit-trace.md` / other
- Trace type: audit-style trace
- Connector type: read-only local/private workspace connector
- Readiness mode: readiness gate dry-run
- `source_trace` reviewed:
- `read_only_verified`:
- `workspace_unchanged`:
- `ready_for_scheduled_watcher`: true only after audit trace review confirms `read_only_verified: true` and `workspace_unchanged: true`; otherwise false
- Stage ledger reviewed:
- Boundary ledger reviewed:

## source_trace / Source Inventory Review

For each source or source group, record metadata/checksums only:

- Path or group:
  - Operation: read
  - Boundary: regular in-workspace file / skipped symlink / output artifact / other
  - SHA-256 or inventory status:
  - Private source content copied into trace? No
  - Needs `[verify]` or reviewer follow-up?

## Read-Only Verification

- Before/after workspace inventory matched?
- `read_only_verified` source:
- `workspace_unchanged` source:
- Output path outside workspace?
- Hardlink/symlink/output boundary checked?
- Private source content excluded from public repo/evals/examples?

## Readiness Gate Dry-Run

- Readiness verdict:
- Readiness blockers:
- Freshness/status issues:
- Retention/audit owner status:
- Internal watcher simulation reviewed:
- Minimum safe next step:

## No External Writes / Live Automation Boundary

- No External Writes: no customer sending, CRM/calendar writes, carrier contact, claims filing, application submission, policy change, quote generation, or publication.
- `live_cron_created: false`.
- no live automation: this output does not authorize `cronjob(action='create')`, scheduled watcher deployment, customer messaging, or external writes.
- Any future scheduled watcher requires explicit separate approval of schedule, timezone, delivery target, reviewer, retention/audit owner, and script-only `no_agent=True` posture.

## Professional Review Gate Handoff

Use `templates/professional-review-gate.md` before customer-facing, regulated, external-use, public-pack canonicalization, or side-effect-adjacent use.

- Action class: private workspace diagnostic / connector audit / readiness review
- Review owner:
- Source verification status:
- Customer-facing approval status: draft for licensed/compliance review; not approved to send
- Side-effect status: no external action is authorized
- Minimum safe next step:

## Forbidden Output States

Do not:

- create live automation or a live Hermes cron job;
- write CRM/calendar tasks or send customer messages;
- contact carriers, file claims, submit applications, change policies, or generate quotes;
- copy private source content into audit traces, public packs, examples, evals, or docs;
- treat a readiness dry-run as deployment approval;
- omit `read_only_verified`, `workspace_unchanged`, `source_trace`, `No External Writes`, or `live_cron_created: false` from the review.
