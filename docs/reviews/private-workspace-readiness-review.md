# Private Workspace Readiness Review

## Scope Reviewed

This review covers the `Private Workspace Readiness Gate` slice:

```text
scripts/private_workspace_readiness.py
tests/test_private_workspace_readiness.py
docs/private-workspace-readiness.md
examples/private-workspace-readiness/*
evals/cases/private-workspace-readiness.json
evals/expected/private-workspace-readiness.md
```

## What Improved

- Added a deterministic readiness report before scheduled watcher deployment.
- Added read-only checks for workspace structure, renewal register freshness, privacy/PII-like patterns, output boundaries, and retention/audit policy presence.
- Added both Markdown and JSON output for human review and deterministic automation.
- Added explicit exit semantics: ready `0`, generated report with blockers `1`, CLI/config error `2`.
- Added tests proving source workspace hashes are unchanged.
- Added tests rejecting explicit report output inside the workspace.
- Added synthetic-mode PII blocking for demo/template workspaces.

## Safety Boundaries Confirmed

The readiness gate does not:

- create live Hermes cron jobs;
- send customer messages;
- write CRM/calendar tasks;
- contact carriers or external portals;
- file claims;
- submit applications;
- change policies;
- delete or mutate private workspace files;
- approve production deployment by itself.

## Known Limitations

- PII scanning is basic deterministic pattern matching, not full DLP.
- Freshness is based on renewal register `status_as_of` fields, not live carrier verification.
- Real private workspaces may intentionally contain customer data; outside `--synthetic-mode`, PII-like hits are warnings, not blockers.
- Retention/audit policy quality is checked by presence/keywords, not legal sufficiency.
- The tool does not enforce deletion or retention automatically.

## Independent Review Findings and Fixes

Independent pre-commit review found blockers that were fixed before commit:

- Symlinked required paths and renewal-register directories could be followed outside the workspace. Fixed by rejecting symlinked required paths and only reading regular in-workspace renewal registers/text files.
- Freshness used only the latest `status_as_of`, so a fresh row could mask stale or blank rows. Fixed by validating every row and blocking blank/stale/future-dated rows.
- Explicit output outside the workspace could still be a hardlink to a workspace source file. Fixed by same-file checks against workspace files.

Regression tests were added for all three classes.

## Verdict

This slice adds a useful readiness gate before a private workspace is connected to the script-only renewal watcher cron wrapper. It improves deployment safety while preserving the project's read-only, internal-only, no-external-write posture.
