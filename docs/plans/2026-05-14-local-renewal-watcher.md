# Local Renewal Watcher / Internal Alert Module Plan

> **For Hermes:** This plan is the durable handoff artifact. If context is compressed or the session is interrupted, resume by reading this file first, then `docs/plans/2026-05-14-local-file-connector-slice.md`, `docs/local-file-connectors.md`, `cron/renewal-watcher-cookbook.md`, and run `git status --short`. Do not rely on prior chat history.

**Goal:** Add a scheduled-agent-ready local renewal watcher that consumes a local-file connector JSON bundle or renewal-register CSV and emits internal-only renewal/lapse risk alerts. This is the first `Scheduled Managed Agents` vertical slice and must preserve no-customer-send/no-CRM-write boundaries.

**Architecture:** Implement a deterministic Python CLI under `scripts/renewal_watcher.py`. It reads either:

1. a JSON bundle produced by `scripts/local_file_connectors.py daily-workbench --format json`; or
2. a renewal register CSV directly.

It classifies renewal rows into D-30, D-14, D-7, D+1, grace-period-before-end, overdue/grace-ended, and verify-status buckets, then emits Markdown or JSON alerts for internal review only. It defaults to stdout and writes only to an explicit output path outside the workspace/input tree when requested.

**Tech Stack:** Python 3 standard library + pytest for tests. No network. No subprocess. No external writes except explicit report output.

---

## Why This Matters vs claude-for-legal

`claude-for-legal`-style professional assistants become practical when connectors feed scheduled monitors/watchers. This phase turns the local connector slice into a scheduled-agent-ready renewal/lapse alert module:

```text
local renewal register / connector bundle
→ watcher risk classification
→ internal-only alert
→ Hermes/Telegram scheduled report later
→ no customer send / no CRM write
```

## Non-goals

- Do not create or register an actual Hermes cron job in this phase.
- Do not send Telegram/customer messages automatically.
- Do not write CRM/calendar tasks.
- Do not connect to carrier portals, CRM, email, calendar, WeChat, WhatsApp, or AIA systems.
- Do not assert coverage active/lapsed/reinstated without `[verify]` markers.
- Do not ingest real customer data into public examples.

## Resume Instructions

1. Read this plan and latest Progress Log entry.
2. Run:

```bash
git status --short
git log --oneline -3
```

3. Resume at the next incomplete task.
4. Use TDD for code: failing watcher tests first, then implementation.
5. Before final handoff run:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help >/tmp/ingest_help.txt
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py -q
python3 scripts/local_file_connectors.py daily-workbench --workspace examples/local-connectors/synthetic-agent-workspace --format json > /tmp/workbench.json
python3 scripts/renewal_watcher.py --bundle /tmp/workbench.json --as-of 2026-05-14 --format markdown >/tmp/renewal-alert.md
git diff --check
git diff --cached --check
```

## Gate Model

- **Pre-flight gate:** repo is on `main`, status is clean or only this phase's edits.
- **TDD gate:** watcher tests fail before watcher implementation.
- **Read-only gate:** watcher reads only local files; no network/subprocess; stdout by default; explicit output only outside input workspace/tree.
- **Privacy gate:** examples use `SYN-` refs only, no real PII.
- **Review gate:** alerts are internal-only and include `[verify]`, `No External Writes`, and licensed/compliance review language.
- **Cron gate:** docs may show cron prompts, but this phase must not create a live scheduled job.
- **Abort gate:** if interrupted, append exact next step to Progress Log.

---

## Task 1: Failing watcher tests

**Files:**
- Create: `tests/test_renewal_watcher.py`

**Acceptance criteria:** tests cover:

- JSON bundle input from local connector;
- direct CSV input;
- D-7 / D+1 / grace-period / grace-ended classification with `--as-of`;
- Markdown includes Internal Renewal Watcher Alert, `[verify]`, No External Writes, and draft-only language;
- JSON output includes `internal_only: true`, `no_external_writes: true`, counts, and alerts;
- missing input is rejected;
- symlink/outside input is rejected when workspace boundary is supplied;
- `--output` inside workspace/input directory is rejected.

**Expected before implementation:** fail because `scripts/renewal_watcher.py` does not exist.

## Task 2: Implement watcher CLI

**Files:**
- Create: `scripts/renewal_watcher.py`

**CLI shape:**

```bash
python3 scripts/renewal_watcher.py --bundle /tmp/workbench.json --as-of 2026-05-14 --format markdown
python3 scripts/renewal_watcher.py --csv examples/local-connectors/synthetic-agent-workspace/renewal-registers/synthetic-renewal-register.csv --as-of 2026-05-14 --format json
```

Optional output:

```bash
python3 scripts/renewal_watcher.py --bundle /tmp/workbench.json --as-of 2026-05-14 --format markdown --output /tmp/renewal-alert.md
```

**Acceptance criteria:**

- Python stdlib only.
- Exactly one of `--bundle` or `--csv` required.
- Parses dates conservatively; unknown dates become `[verify]` alert items.
- Sorts alerts by urgency.
- Does not emit customer-facing send-ready copy; only internal draft language.
- Refuses output inside workspace/input parent tree when `--workspace` supplied.

## Task 3: Synthetic examples and expected outputs

**Files:**
- Create: `examples/renewal-watcher/synthetic-renewal-alert.md`
- Create: `examples/renewal-watcher/synthetic-renewal-alert.json`
- Optionally create a direct CSV fixture if local connector fixture is insufficient.

**Acceptance criteria:**

- Generated from synthetic fixture.
- Contains D-7/D+1/grace examples or enough rows to demonstrate buckets.
- Uses only `SYN-` refs.

## Task 4: Docs / cookbook / cron no-agent pattern

**Files:**
- Create: `docs/local-renewal-watcher.md`
- Modify: `cron/renewal-watcher-cookbook.md`
- Modify: `cron/renewal-watcher.md`
- Modify: `README.md`
- Modify: `docs/quickstart.md`

**Acceptance criteria:**

- Docs explain internal-only watcher use.
- Docs show script-only/no-agent cron pattern but do not create a live cron job.
- Docs include a Hermes cron prompt template with no customer side effects.
- Docs say `custom:fufu` model override may be used for scheduled summary jobs if the user chooses to create them later, without changing global config.

## Task 5: Eval / validator / CI coverage

**Files:**
- Add: `evals/cases/local-renewal-watcher.json`
- Add: `evals/expected/local-renewal-watcher.md`
- Modify: `scripts/validate_repo.py`
- Modify: `.github/workflows/validate.yml`

**Acceptance criteria:**

- Eval count increases to at least 16.
- Validator requires watcher script, docs, tests, examples, CI pytest command.
- CI runs watcher tests.

## Task 6: Review and iteration

**Files:**
- Create: `docs/reviews/local-renewal-watcher-review.md`
- Update this plan Progress Log.

**Acceptance criteria:**

- Reflection compares this phase to scheduled/managed-agent gap.
- Independent review passes, or blockers are fixed and re-reviewed.
- Full verification suite passes.

---

## Progress Log

- 2026-05-14: Plan created. Next task: Task 1 write failing watcher tests.

- 2026-05-14: Task 1 completed. Failing tests were written and observed RED because `scripts/renewal_watcher.py` did not exist.

- 2026-05-14: Task 2 completed. `scripts/renewal_watcher.py` implemented; `python3 -m pytest tests/test_renewal_watcher.py -q` passes.

- 2026-05-14: Task 3-6 docs/eval/review assets drafted. Next task: run validator, CI-equivalent suite, independent review, then commit/push.

- 2026-05-14: Independent review suggested tighter output guards. Added failing tests for inferred CSV workspace output contamination and input overwrite, then fixed watcher and docs; watcher tests now pass 7 cases.

- 2026-05-14: Final review suggested hard-link overwrite protection. Added failing hardlink test, implemented `Path.samefile` guard; watcher tests now pass 8 cases.

- 2026-05-14: Final review found documented `/tmp` bundle + `--workspace` pattern was blocked. Added failing test allowing outside bundle artifacts while still rejecting symlinked bundles; fixed containment logic.
