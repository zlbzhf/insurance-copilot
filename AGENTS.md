# Insurance Copilot — Hermes Project Instructions

This repository is Hermes-first. It is inspired by `claude-for-legal` workflow discipline, but the deliverable is a Hermes skill project, not a Claude plugin.

## Development Rules

- Primary installable artifact: `skills/insurance-copilot/SKILL.md`.
- Supporting skill files must live under `skills/insurance-copilot/references/`, `templates/`, `scripts/`, or `assets/`.
- Keep insurance outputs as drafts for licensed/compliance review.
- Do not add web app scaffolding unless explicitly requested.
- Do not make Claude plugin metadata or `CLAUDE.md` the main interface.
- Run `python3 scripts/validate_repo.py` before committing.

## Repository Layout

```text
skills/insurance-copilot/   Hermes skill package
examples/                   Non-sensitive sample inputs/expected outputs
cron/                       Hermes scheduled workflow recipes
mcp/                        Notes for optional MCP/data connectors
scripts/                    Repo validation and maintenance scripts
docs/                       Design notes
```

## GitHub Remote

Expected remote:

```text
git@github.com-insurance-copilot:zlbzhf/insurance-copilot.git
```
