# Private Workspace Readiness Validator + Retention/Audit Pack Plan

> **For Hermes:** This plan is the durable handoff artifact. If context is compressed or the session is interrupted, resume by reading this file first, then run the state/validation commands below. Do not rely on prior chat history.

## Goal

Add a private-workspace readiness gate before any real scheduled renewal watcher is deployed.

The validator should answer:

```text
Is this private agent workspace structurally ready, fresh enough, privacy-safe enough, and audit/retention-aware enough to connect to script-only scheduled monitoring?
```

This phase productizes the step between:

```text
agent private workspace template
→ local connector / renewal watcher / cron wrapper
```

and a future live job.

## Resume Instructions

Read first:

1. `docs/plans/2026-05-14-private-workspace-readiness.md`
2. `scripts/validate_agent_workspace.py`
3. `scripts/local_file_connectors.py`
4. `scripts/renewal_watcher.py`
5. `docs/script-only-cron-wrapper.md`
6. `docs/agent-private-knowledge.md`
7. `docs/quality-gates.md`
8. `README.md`

Then run:

```bash
git status --short
git log --oneline -5
python3 scripts/validate_repo.py
```

Resume from the first unchecked task in this plan, not from chat memory.

## Non-goals

- Do not create a live Hermes cron job.
- Do not connect CRM, calendar, carrier, email, messaging, or policy-admin systems.
- Do not store production private workspace data in this public repo.
- Do not auto-delete or mutate private workspace files.
- Do not produce final compliance approval or final regulated advice.
- Do not add a web app or UI.
- Do not promote private notes into public knowledge packs in this phase.

## Gate Model

### Pre-flight gate

- Current branch is `main` and git state is known.
- Existing validators pass before substantive edits, or current failures are documented.
- Plan exists before implementation.

### Revision gate

Every implementation task must be checked against:

- TDD cycle: failing tests observed before production code.
- Readiness output has both JSON and Markdown forms.
- No source workspace mutation during normal validation.
- Explicit report output must be outside the workspace.
- Safety boundaries remain internal/read-only.

### Escalation gate

Stop and ask if any requested change would:

- validate or process real private data inside this public repo;
- require automated deletion/retention enforcement;
- create live scheduled jobs;
- send customer communications or write external systems;
- decide coverage/lapse/reinstatement status.

### Abort gate

If tool calls/context are running out:

- update this Progress Log with completed tasks and next command;
- keep all changes either committed or clearly visible in `git status --short`;
- do not leave a half-created live integration.

## Task 1 — TDD for readiness validator

Create failing tests first for a new script, expected path:

```text
scripts/private_workspace_readiness.py
tests/test_private_workspace_readiness.py
```

Behavior to cover:

- template/synthetic workspace can produce a Markdown readiness report.
- JSON output includes `ready_for_cron`, `summary`, `checks`, `risks`, and `recommended_next_actions`.
- required directories/files are checked.
- renewal register freshness is checked against `--as-of` and `--max-stale-days`.
- stale renewal register blocks readiness.
- risky PII-like content in synthetic/template mode blocks readiness.
- source workspace file hashes are unchanged after validation.
- `--output` inside workspace is rejected.
- explicit output outside workspace works.
- report includes retention/audit checklist items.

Acceptance command:

```bash
python3 -m pytest tests/test_private_workspace_readiness.py -q
```

## Task 2 — Implement validator

Implement minimal deterministic validator:

```bash
python3 scripts/private_workspace_readiness.py   --workspace examples/local-connectors/synthetic-agent-workspace   --as-of 2026-05-14   --format markdown
```

Expected report sections:

- `# Private Workspace Readiness Report`
- `Readiness Verdict`
- `Workspace Structure`
- `Renewal Register Freshness`
- `Privacy / PII Scan`
- `Output Boundary`
- `Retention / Audit Checklist`
- `Scheduled Watcher Deployment Gate`
- `Recommended Next Actions`
- `No External Writes`

JSON fields:

```json
{
  "ready_for_cron": false,
  "internal_only": true,
  "no_external_writes": true,
  "summary": {...},
  "checks": [...],
  "risks": [...],
  "recommended_next_actions": [...]
}
```

## Task 3 — Docs, examples, evals, CI, validator

Add or update:

```text
docs/private-workspace-readiness.md
examples/private-workspace-readiness/synthetic-readiness-report.md
examples/private-workspace-readiness/synthetic-readiness-report.json
docs/reviews/private-workspace-readiness-review.md
evals/cases/private-workspace-readiness.json
evals/expected/private-workspace-readiness.md
.github/workflows/validate.yml
scripts/validate_repo.py
README.md
docs/quickstart.md
docs/script-only-cron-wrapper.md
ROADMAP.md
```

Validator/CI should run:

```bash
python3 -m pytest tests/test_private_workspace_readiness.py -q
python3 scripts/private_workspace_readiness.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --format json
```

## Task 4 — Full verification and independent review

Run:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_all_knowledge_packs.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help >/tmp/ingest_help.txt
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py tests/test_renewal_watcher_cron_wrapper.py tests/test_private_workspace_readiness.py -q
git diff --check
git diff --cached --check
```

Request independent review focused on:

- no source mutation;
- output contamination;
- PII false negatives in examples/templates;
- stale source logic;
- no live cron side effects;
- docs matching implementation.

Fix review blockers with failing tests first.

## Task 5 — Commit and push

Commit with:

```text
feat: add private workspace readiness gate
```

Push to `origin main` only after all validation and review pass.

## Progress Log

- 2026-05-14: Plan created. Next task: Task 1 write failing readiness validator tests.

- 2026-05-14: TDD tests, validator, docs, examples, evals, CI, and validator updates completed.
- 2026-05-14: Independent review found symlink/freshness/hardlink blockers. Added failing regression tests for symlinked required paths/register dirs, blank/stale/future per-row `status_as_of`, and output hardlink aliases. Fixed validator and regenerated examples.
