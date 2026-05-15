# Private Dry-Run Deployment Harness Plan

> **For Hermes:** This plan is the durable handoff artifact. If context is compressed or the session is interrupted, resume by reading this file first, then run the state/validation commands below. Do not rely on prior chat history.

## Goal

Add a deterministic, read-only private dry-run harness that chains the current private-workspace deployment gates before any live Hermes scheduled watcher is created:

```text
private workspace
  -> Private Workspace Readiness Gate
  -> Daily Agent Workbench connector bundle
  -> Internal Renewal Watcher
  -> script-only cron wrapper simulation
  -> manifest + deployment checklist
```

The harness should make it easy for an agent to run one local/private dry run and inspect all generated artifacts before deciding whether to create a live Hermes `no_agent=True` scheduled job.

## Resume Instructions

After a fresh session or context compression:

1. Read this file first.
2. Run:

```bash
git status --short
git log --oneline -5
python3 scripts/validate_repo.py
```

3. Inspect current implementation files:

```text
scripts/private_dry_run.py
tests/test_private_dry_run.py
docs/private-dry-run-harness.md
examples/private-dry-run/
docs/reviews/private-dry-run-harness-review.md
```

4. Resume from the next unchecked task below. Trust repo state and this plan over prior chat memory.

## Non-goals

This phase must not:

- create or schedule a real Hermes cron job;
- use `cronjob(action='create')` or configure Hermes automatically;
- send customer messages;
- write CRM/calendar tasks;
- contact carrier portals;
- file claims;
- submit applications;
- change, cancel, surrender, or replace policies;
- write generated artifacts inside the private source workspace;
- commit real customer data, secrets, production policy records, or non-public institution materials;
- build a web app or production connector.

## Gate Model

### Pre-flight gate

- Working tree state is known.
- Existing repo validator passes before implementation.
- Plan exists before production code.

### TDD gate

- Write failing tests for harness behavior first.
- Watch tests fail because `scripts/private_dry_run.py` is missing or behavior is missing.
- Implement the smallest script that passes tests.

### Revision gate

Before marking done, compare implementation against acceptance criteria:

- readiness stage captured;
- connector bundle generated outside workspace;
- renewal watcher output generated;
- cron wrapper simulation generated;
- manifest/checklist generated;
- source workspace not mutated;
- output path/hardlink/symlink boundaries covered;
- no live cron or external side effects.

### Escalation gate

Stop and ask before adding any side-effecting action, remote integration, live scheduled job creation, customer-send flow, CRM/calendar write, or production-data handling.

### Abort gate

If tool calls/context are running out, update this plan progress log with the next exact command/file to inspect.

## Acceptance Criteria

### Code

Create:

```text
scripts/private_dry_run.py
```

Required CLI:

```bash
python3 scripts/private_dry_run.py   --workspace examples/local-connectors/synthetic-agent-workspace   --as-of 2026-05-14   --out /tmp/insurance-copilot-dry-run
```

Optional flags:

```text
--max-stale-days N
--synthetic-mode
--force
```

Required behavior:

- Reject missing workspace.
- Reject symlinked workspace root.
- Reject `--out` inside workspace.
- Reject `--out` samefile/hardlink alias to any workspace source file if it already exists.
- If out dir exists and is non-empty, require `--force`.
- Default output is an explicit out directory, not stdout-only.
- Generated artifacts must be outside the workspace.
- Readiness can return not-ready (`exit 1`) and still be captured as an artifact; dry-run script should continue to produce a complete diagnostic bundle, then return non-zero because deployment is blocked.
- Child command configuration errors should fail loud with useful stderr.
- Do not mutate source workspace.

Required artifacts:

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

`manifest.json` should include:

- `workflow: Private Dry-Run Deployment Harness`
- `workspace`
- `as_of`
- `ready_for_scheduled_watcher`
- `read_only: true`
- `no_external_writes: true`
- artifact paths/checksums/sizes
- stage statuses and exit codes
- explicit note that no live Hermes cron job was created.

### Tests

Create:

```text
tests/test_private_dry_run.py
```

Tests should cover:

1. synthetic workspace generates all expected artifacts and manifest shape;
2. not-ready readiness is captured and dry-run returns non-zero, while artifacts are still produced;
3. ready synthetic temp workspace returns `0`;
4. source workspace hashes are unchanged;
5. `--out` inside workspace is rejected;
6. `--out` hardlink/samefile alias to workspace source file is rejected;
7. existing non-empty out dir requires `--force`;
8. symlinked workspace root is rejected;
9. cron simulation artifact contains `Internal Renewal Watcher Alert`, `[verify]`, and `No External Writes`.

### Docs and CI

Create/update:

```text
docs/private-dry-run-harness.md
examples/private-dry-run/synthetic-manifest.json
examples/private-dry-run/synthetic-deployment-checklist.md
evals/cases/private-dry-run-harness.json
evals/expected/private-dry-run-harness.md
docs/reviews/private-dry-run-harness-review.md
README.md
docs/quickstart.md
docs/quality-gates.md
ROADMAP.md
scripts/validate_repo.py
.github/workflows/validate.yml
```

CI should run:

```bash
python3 -m pytest tests/test_private_dry_run.py -q
```

Validator should require the new script/docs/examples/eval/test and smoke-run the synthetic dry-run with `|| test $? -eq 1` where appropriate because synthetic fixture may be intentionally not ready.

## Validation Commands

Run before commit:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_all_knowledge_packs.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help >/tmp/ingest_help.txt
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py tests/test_renewal_watcher_cron_wrapper.py tests/test_private_workspace_readiness.py tests/test_private_dry_run.py -q
```

Also run a static scan over the staged diff for obvious secrets/PII patterns.

## Review Task

Before commit, run independent blocker-focused review on staged changes. Ask reviewer to focus on:

- symlink/path traversal;
- source workspace mutation;
- output contamination/hardlink aliases;
- child-command failure handling;
- no live cron creation;
- fixture privacy;
- documentation mismatch.

Record results in:

```text
docs/reviews/private-dry-run-harness-review.md
```

## Task List

- [x] Plan this slice.
- [x] RED: write failing dry-run tests.
- [x] GREEN: implement `scripts/private_dry_run.py`.
- [x] Add docs/examples/eval/CI/validator coverage.
- [x] Run full validation.
- [x] Independent review and fixes.
- [ ] Commit and push.

## Progress Log

- 2026-05-14: Plan created. Next task: write failing tests for dry-run harness behavior.

- 2026-05-14: TDD/tests/docs/CI/validator implemented. Full validation passed locally. Manual blocker review completed after subagent review timeout; manifest self-checksum marker fix applied. Next task: commit and push.
