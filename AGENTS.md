# Insurance Copilot — Hermes Project Instructions

This repository is Hermes-first. It is inspired by `claude-for-legal` workflow discipline, but the deliverable is a Hermes skill project, not a Claude plugin.

## Source of Truth

If chat context, compression summaries, or memory conflict with repository files, trust the current repository files and git state.

Before substantive changes, read:

- `README.md`
- `skills/insurance-copilot/SKILL.md`
- `docs/continuity.md`
- `docs/quality-gates.md`
- `ROADMAP.md`

Then run:

```bash
git status --short
python3 scripts/validate_repo.py
```

## Development Rules

- Primary installable artifact: `skills/insurance-copilot/SKILL.md` plus its full support directory.
- Supporting skill files must live under `skills/insurance-copilot/references/`, `templates/`, `scripts/`, or `assets/`.
- Keep insurance outputs as drafts for licensed/compliance review.
- Use minimum necessary data; do not commit real customer PII, secrets, production policy documents, or claim files.
- Do not add web app scaffolding unless explicitly requested.
- Do not make Claude plugin metadata or `CLAUDE.md` the main interface.
- Do not add customer-sending, application-submission, claims-filing, or policy-change automation without explicit user request and action-safety design.
- Run all validation commands before committing.

## Required Validation

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
```

## Repository Layout

```text
skills/insurance-copilot/   Hermes skill package
examples/                   Synthetic sample inputs/expected outputs
evals/                      Static regression fixtures
cron/                       Hermes scheduled workflow recipes
mcp/                        Optional MCP/data connector contracts
scripts/                    Repo validation, packaging, eval scripts
docs/                       Design, privacy, action safety, continuity, quality gates
```

## GitHub Remote

Expected remote:

```text
git@github.com-insurance-copilot:zlbzhf/insurance-copilot.git
```
