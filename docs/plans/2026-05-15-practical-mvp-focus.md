# Practical MVP Focus Plan

> **For Hermes:** Keep this plan as the final scope guard for the usable practitioner release. Do not expand into cron/deployment work unless the user explicitly asks.

**Goal:** Deliver a usable manual-first Insurance Copilot version for insurance agents.

**Architecture:** The primary user surface is the Hermes skill and its task-first workflow router. Public institution packs and private workspaces support the workflows. Local connectors/watchers remain advanced/later safeguards.

**Tech Stack:** Markdown Hermes skill, references/templates, synthetic examples, static evals, pytest repository checks.

---

## Scope Freeze

In scope:

- README and quickstart that explain how an agent actually uses the project.
- Practical first-session example.
- Task-first routing rules in `SKILL.md`.
- Static eval and pytest regression for the practical MVP surface.
- Existing validators updated only enough to preserve delivery quality.

Out of scope unless explicitly requested:

- new cron jobs;
- scheduled watcher deployment;
- new CI infrastructure beyond validating the deliverable;
- production integrations;
- web UI/backend;
- carrier quote/policy-admin integration.

## Acceptance Criteria

- A new user can install the skill and run a practical manual-first first session.
- README starts with practical use, not infrastructure.
- Quickstart shows the 30-minute loop before advanced tools.
- `SKILL.md` tells Hermes to route directly to tasks, ask at most three essential questions, and avoid menu dumping.
- Example and eval cover practice profile, daily workbench, client intake, and compliance copy checking.
- Validation, evals, tests, and CI pass.

## Verification Commands

```bash
python3 -m pytest tests/test_practitioner_mvp_surface.py -q
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py tests/test_renewal_watcher_cron_wrapper.py tests/test_private_workspace_readiness.py tests/test_private_dry_run.py tests/test_practitioner_mvp_surface.py -q
```
