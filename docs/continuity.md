# Continuity and Handoff Protocol

This repository must remain usable even if a Hermes conversation is compressed, interrupted, or restarted in a new chat. Treat committed repository files as the source of truth, not prior chat memory.

## Authoritative Artifacts

Read these files first in a fresh session:

1. `AGENTS.md` — project rules and non-negotiables.
2. `README.md` — user-facing install/use docs.
3. `skills/insurance-copilot/SKILL.md` — canonical Hermes skill entry point.
4. `docs/quality-gates.md` — acceptance criteria and validation gates.
5. `ROADMAP.md` — current development priorities.
6. `scripts/validate_repo.py` — executable structural quality gate.

## Fresh Session Resume Procedure

From the repository root:

```bash
git status --short
git log --oneline -5
python3 scripts/validate_repo.py
```

Then read the relevant workflow reference under:

```text
skills/insurance-copilot/references/
```

Do not infer project state from an old conversation summary. If chat context and repository files disagree, trust the repository and current git state.

## Compression-Safe Development Rules

- Keep project intent in committed docs, not only in chat.
- Every structural decision should be reflected in `AGENTS.md`, `README.md`, `docs/`, or `skills/insurance-copilot/SKILL.md`.
- Every new workflow should have at least one reference file, one template or example if practical, and validator coverage if it affects structure.
- Before finalizing any development turn, run `python3 scripts/validate_repo.py` and commit/push unless the user explicitly asks not to.
- Avoid temporary TODO state as the only record of project direction. Durable direction belongs in `ROADMAP.md`.

## Canonical Current Direction

Insurance Copilot is a Hermes-first skill repository for licensed insurance professionals. It is inspired by `claude-for-legal` in methodology, but the deliverable is a Hermes skill package:

```text
skills/insurance-copilot/SKILL.md
```

The project should not drift back into Claude plugin packaging, web app scaffolding, or uncommitted chat-only plans.
