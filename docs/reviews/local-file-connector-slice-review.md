# Local File Connector Slice Review

## Purpose

Assess whether this phase improved Insurance Copilot's connector maturity while preserving privacy, review, and no-side-effect boundaries.

## What Improved vs claude-for-legal Connector Gap

- Added a deterministic read-only connector CLI: `scripts/local_file_connectors.py`.
- Added TDD coverage for Markdown output, JSON output, explicit output file behavior, missing workspace rejection, and non-mutation of source files.
- Symlink traversal was explicitly regression-tested and blocked by skipping symlinked/non-regular input files.
- Explicit output paths are rejected when they point inside the workspace, preventing generated bundles from becoming or overwriting input records.
- Added a synthetic private-workspace-shaped fixture under `examples/local-connectors/`.
- Added a generated Daily Agent Workbench connector bundle that can be pasted into Hermes.
- Added docs explaining how local file connectors bridge toward future MCP/data connectors.
- Added validator and CI coverage so the connector slice is not lost in future refactors.
- CI now installs developer pytest dependency from `requirements-dev.txt` before running validators/tests.

## Safety / Data Boundaries Preserved

- No real customer data.
- No real insurer or AIA data.
- No network calls.
- No CRM/calendar/customer-message writes.
- No carrier portal access.
- No claims filing, applications, or policy changes.
- All uncertain policy/payment/claim/referral facts remain `[verify]`.

## Remaining Gaps

- Still no real production connector to CRM, carrier portal, document store, calendar, or messaging.
- No deployed scheduled cron agent consumes the connector output yet.
- The connector is deterministic and useful for bundling context, but it does not perform live model evaluation.
- Public institution packs are still structurally ready but not content-rich with official public source records.

## Next Phase Recommendation

Build a reviewed cron/watchdog cookbook that consumes a local renewal-register connector bundle and emits internal alerts only. Keep it no-agent or agent-assisted with no external writes. After that, consider an official-public-source AIA minimal pack.
