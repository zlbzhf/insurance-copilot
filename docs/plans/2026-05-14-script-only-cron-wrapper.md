# Script-only Renewal Watcher Cron Wrapper Plan

> **For Hermes:** This plan is the durable handoff artifact. If context is compressed or the session is interrupted, resume by reading this file first, then `docs/plans/2026-05-14-local-renewal-watcher.md`, `docs/local-renewal-watcher.md`, and run `git status --short`. Do not rely on prior chat history.

**Goal:** Add a deployable-but-not-live script-only cron wrapper template for the Local Renewal Watcher. It should support `no_agent=True` Hermes cron watchdog semantics: silent when no review-worthy renewal rows exist, fail loudly on broken configuration, print an internal-only alert when rows require review, and never send customer messages or write back into the private workspace.

**Module role:** This is `Scheduled Managed Agents Layer v0.2`: move from manual watcher CLI to a safe script-only watchdog template and dry-run test harness, without creating a real cron job.

## Non-goals

- Do not create a live Hermes cron job in this phase.
- Do not deliver alerts to Telegram from tests/docs.
- Do not connect to CRM/calendar/carrier portals or messaging systems.
- Do not write output inside the private workspace.
- Do not use real customer data in fixtures.
- Do not add an LLM summary job as required behavior; only document it as optional after approval.

## Resume Instructions

1. Read this file and latest Progress Log entry.
2. Run:

```bash
git status --short
git log --oneline -3
```

3. Resume from the first incomplete task below.
4. Use TDD: failing tests for the wrapper before implementation.
5. Final validation:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help >/tmp/ingest_help.txt
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py tests/test_renewal_watcher_cron_wrapper.py -q
bash cron/scripts/renewal_watcher.sh --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --mode always >/tmp/cron-renewal-alert.md
git diff --check
git diff --cached --check
```

## Gate Model

- **Pre-flight gate:** current branch `main`; no unrelated dirty work.
- **TDD gate:** wrapper tests fail because script does not exist or lacks required semantics.
- **Cron safety gate:** wrapper prints alert only when configured; silent no-alert mode exits 0 with empty stdout; broken config exits non-zero.
- **No-side-effect gate:** wrapper uses stdout/temp output only, no network/subprocess other than local Python scripts, no customer send, no CRM/calendar write.
- **Workspace gate:** output artifacts are in `/tmp` or caller-provided outside path; never inside workspace.
- **Hermes gate:** docs show `cronjob`/Hermes `no_agent=True` semantics and optional LLM summary with per-job `custom:fufu` / `mimo-v2.5-pro` override, but do not schedule a job.
- **Review gate:** independent review must pass or blockers are fixed.

## Task 1: Failing wrapper tests

**Files:** create `tests/test_renewal_watcher_cron_wrapper.py`.

Acceptance criteria:

- test alert mode prints `Internal Renewal Watcher Alert`, `[verify]`, `No External Writes`;
- test `--mode alert-only` is silent when there are no actionable alerts;
- test missing workspace fails loudly;
- test output path inside workspace is rejected;
- test wrapper does not mutate source workspace files;
- test script works from repo root with synthetic workspace.

## Task 2: Implement wrapper script

**Files:** create `cron/scripts/renewal_watcher.sh`.

Acceptance criteria:

- Bash, `set -euo pipefail`.
- Args: `--workspace`, `--as-of`, `--mode always|alert-only`, optional `--output`.
- Generates connector bundle outside workspace, runs `scripts/renewal_watcher.py` with `--workspace`.
- In `alert-only`, suppresses output when JSON alert count is zero or only monitor items are present.
- Prints internal alert to stdout by default; explicit `--output` must be outside workspace.
- Broken config exits non-zero with useful stderr.

## Task 3: Docs/examples/CI/validator

Files:

- create `docs/script-only-cron-wrapper.md`;
- create `examples/cron/renewal-watcher-no-agent.md`;
- modify `cron/renewal-watcher-cookbook.md`;
- modify `docs/local-renewal-watcher.md`;
- modify `README.md`, `docs/quickstart.md`;
- modify `.github/workflows/validate.yml`, `scripts/validate_repo.py`.

Acceptance criteria:

- docs show no-agent watchdog semantics;
- docs mention empty stdout = silent, non-zero = error alert;
- docs include optional LLM summary job with per-job model override `custom:fufu` / `mimo-v2.5-pro` but no live scheduling;
- CI runs wrapper tests;
- validator requires wrapper script/docs/tests/CI.

## Task 4: Review / reflection / commit

Files:

- create `docs/reviews/script-only-cron-wrapper-review.md`;
- update Progress Log;
- run full validation and independent review;
- commit and push.

## Progress Log

- 2026-05-14: Plan created. Next task: Task 1 write failing wrapper tests.
- 2026-05-14: TDD tests added and verified red against missing `cron/scripts/renewal_watcher.sh`.
- 2026-05-14: Wrapper implemented and tests green; docs, example, CI, and validator updated.
- 2026-05-14: Review doc added. Next task: run full validation, independent review, fix blockers, commit, push.

- 2026-05-14: Independent review found TMPDIR/fail-loud/doc-copy issues; added failing tests for TMPDIR-inside-workspace and invalid `--as-of`, fixed wrapper and docs. Next task: rerun full validation and final review.
