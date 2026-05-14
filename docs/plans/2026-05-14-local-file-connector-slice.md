# Local File Connector Slice Implementation Plan

> **For Hermes:** This plan is the durable handoff artifact. If context is compressed or the session is interrupted, resume by reading this file first, then `docs/plans/2026-05-14-practical-agent-workflow-beta.md`, `README.md`, `skills/insurance-copilot/SKILL.md`, and run `git status --short`. Do not rely on prior chat history.

**Goal:** Add a small read-only local-file connector slice that turns private workspace files into a Daily Agent Workbench input bundle without touching real systems or external side effects.

**Architecture:** Implement a deterministic Python CLI under `scripts/` that reads only local synthetic/private workspace files, normalizes renewal register rows, customer profiles, policy summaries, claim trackers, referral trackers, meeting notes, and tasks into a JSON or Markdown workbench bundle. The CLI never writes to CRM/calendar/customer channels; it only prints output or writes a local bundle file when explicitly requested. Tests use synthetic fixtures only.

**Tech Stack:** Python 3 standard library, pytest, Markdown/CSV/JSON/YAML-like frontmatter parsing without new dependencies, existing Hermes repo validators.

---

## Reference Shape: claude-for-legal -> insurance-copilot

This phase maps the `claude-for-legal` connector idea into a safe Hermes-first insurance slice:

- Legal connectors to CLM/DMS/e-discovery -> local read-only private workspace files.
- Managed agents -> daily workbench prompt bundle generated from connector output.
- Attorney review gate -> licensed/compliance review gate.
- No external writes -> no CRM/calendar/customer side effects.

## Non-goals

- Do not connect to real CRM, carrier portal, email, calendar, WeChat, WhatsApp, or AIA systems.
- Do not ingest real customer or insurer data into the public repo.
- Do not add a web UI or background daemon.
- Do not create deployed cron jobs yet; update cookbook/docs only.
- Do not bypass the practice profile gate or human review gates.

## Resume Instructions

1. Read this plan.
2. Run:

```bash
git status --short
git log --oneline -3
```

3. Resume from the next incomplete task in the Progress Log.
4. For code changes, use TDD: write tests first, run them to fail, implement, run to pass.
5. Before final handoff run the full verification suite:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help >/tmp/ingest_help.txt
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py -q
```

## Gate Model

- **Pre-flight gate:** repository on `main`, no uncommitted unrelated work, public files use synthetic/de-identified data only.
- **TDD gate:** every new connector behavior has a failing test before implementation.
- **Read-only gate:** connector code may read files and optionally write an explicit output path; it must not call network, subprocess external side-effect tools, or mutate workspace records.
- **Privacy gate:** committed fixtures must use `SYN-` refs and must not include real-looking PII.
- **Review gate:** generated bundles must label customer-facing text as draft and list verification/review gates.
- **Abort gate:** if context/tools run low, update Progress Log with completed tasks and next exact command.

---

## Task 1: Write failing tests for local connector CLI

**Objective:** Specify expected read-only behavior before implementation.

**Files:**
- Create: `tests/test_local_file_connectors.py`
- Test fixtures created inside pytest temp directories.

**Acceptance criteria:**

- Tests cover:
  - reading `renewal-registers/template-renewal-register.csv` style CSV;
  - reading customer/profile/policy/claim/referral/task Markdown files;
  - generating Markdown bundle with Today's Priorities, High-Risk Items, Verify Before Action, and No External Writes;
  - generating JSON bundle with normalized arrays;
  - rejecting missing workspace root;
  - not mutating source files.

**Command:**

```bash
python3 -m pytest tests/test_local_file_connectors.py -q
```

Expected before implementation: fail because `scripts/local_file_connectors.py` does not exist.

## Task 2: Implement local connector CLI

**Objective:** Make tests pass with a small deterministic read-only CLI.

**Files:**
- Create: `scripts/local_file_connectors.py`

**CLI shape:**

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace agent-workspace-template   --format markdown

python3 scripts/local_file_connectors.py daily-workbench   --workspace agent-workspace-template   --format json
```

Optional explicit write:

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace agent-workspace-template   --format markdown   --output /tmp/workbench.md
```

**Acceptance criteria:**

- Uses only Python stdlib.
- Reads local files under the workspace path.
- Emits JSON/Markdown to stdout by default.
- Writes only when `--output` is passed.
- Includes `read_only: true` / `no_external_writes: true` in JSON.
- Markdown includes `Draft for licensed/compliance review` and `No External Writes`.
- Sorts urgent renewal rows by due date/grace period when possible.
- Marks source statuses with `[verify]` when missing/unclear.

## Task 3: Add synthetic connector fixture workspace

**Objective:** Provide a public synthetic example that demonstrates the connector without real data.

**Files:**
- Create directory: `examples/local-connectors/synthetic-agent-workspace/`
- Add minimal files under:
  - `customers/` or `clients/`
  - `meetings/`
  - `policies/`
  - `renewal-registers/`
  - `claims/`
  - `referrals/`
  - `tasks/`
- Create expected output: `examples/local-connectors/expected-daily-workbench.md`

**Acceptance criteria:**

- All refs use `SYN-`.
- No phone/email/address/government IDs.
- Running CLI on this fixture produces a useful daily workbench.

## Task 4: Add connector docs and update quickstart/workflow surface

**Objective:** Explain how private local-file connectors fit the practical workflow.

**Files:**
- Create: `docs/local-file-connectors.md`
- Modify: `README.md`
- Modify: `docs/quickstart.md`
- Modify: `docs/workflow-surface.md`
- Modify: `mcp/README.md` if appropriate.

**Acceptance criteria:**

- Docs say connector is read-only and local-file only.
- Docs show commands for Markdown and JSON output.
- Docs explain how to paste bundle into Daily Agent Workbench.
- Docs warn not to commit private workspace outputs.

## Task 5: Add eval and validator coverage

**Objective:** Prevent future regressions.

**Files:**
- Add eval: `evals/cases/local-file-daily-workbench.json`
- Add expected: `evals/expected/local-file-daily-workbench.md`
- Modify: `scripts/validate_repo.py`
- Modify: `.github/workflows/validate.yml` if new commands should run in CI.

**Acceptance criteria:**

- `validate_repo.py` requires `scripts/local_file_connectors.py`, docs, tests, and local connector example.
- Eval count increases to at least 15.
- CI runs `python3 -m pytest tests/test_local_file_connectors.py -q`.

## Task 6: Reflection and iteration

**Objective:** Confirm this phase improved connector maturity without crossing safety/data boundaries.

**Files:**
- Create: `docs/reviews/local-file-connector-slice-review.md`
- Update this plan Progress Log.

**Acceptance criteria:**

- Review says what improved vs `claude-for-legal` connector gap.
- Review lists remaining gaps: no real connectors, no deployed cron, no real institution data.
- Any missed acceptance criteria are fixed before commit.

---

## Progress Log

- 2026-05-14: Plan created. Next task: Task 1 write failing tests for local connector CLI.

- 2026-05-14: Implemented local-file connector slice with tests, synthetic fixture, docs, eval, validators, CI, and review. Next: full verification, commit, push.
- 2026-05-14: Independent pre-commit review found symlink traversal and output-inside-workspace risks; fixed with regression tests and connector path guards. Next: rerun full verification, commit, push.
- 2026-05-14: Second review found CI pytest dependency risk; added `requirements-dev.txt` and CI install step. Next: final verification, commit, push.
