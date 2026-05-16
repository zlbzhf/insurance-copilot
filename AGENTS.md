# Insurance Copilot — Hermes Project Instructions

This repository is Hermes-first. It is inspired by `claude-for-legal` workflow discipline, but the deliverable is a Hermes skill and layered knowledge project, not a Claude plugin.

## Source of Truth

If chat context, compression summaries, or memory conflict with repository files, trust the current repository files and git state.

Before substantive changes, read:

- `README.md`
- `skills/insurance_copilot/SKILL.md`
- `docs/product-development-spec.md`
- `docs/reference-landscape.md`
- `docs/architecture.md`
- `docs/evidence-driven-standards.md`
- `standards/current.yaml`
- `standards/source-taxonomy.yaml`
- `standards/page-type-registry.yaml`
- `docs/continuity.md`
- `docs/quality-gates.md`
- `docs/documentation-map.md`
- `ROADMAP.md`

Then run:

```bash
git status --short
python3 scripts/validate_repo.py
```

## Three-Layer Architecture

1. `skills/insurance_copilot/` — public general Hermes workflow skill.
2. `knowledge/institutions/` — public institution LLM wiki packs only.
3. `agent-workspace-template/` — template for private agent workspaces stored outside this repo.

Non-public institution materials belong in the agent-private layer, not in public institution packs.

Public institution pack standards evolve through `standards/`, `schemas/`, `prompts/`, `intake/`, `staging/`, and `scripts/ingest_gateway.py`. Do not add one-off templates solely from intuition; record schema gaps from real source processing and update standards through reviewed proposals.

## Product Development SPEC

`docs/product-development-spec.md` is the durable product-development source of truth. Treat the project as usable now as a manual-first Hermes skill beta, but not production-complete for live automation, customer sending, CRM writes, application submission, claims filing, policy changes, quote generation, or final regulated advice.

When borrowing from external/reference projects, use `docs/reference-landscape.md`. Every borrowed pattern must be mapped to project significance, implementation form, non-goals, and priority. Do not chase feature parity or drift into a generic RAG chatbot, web app, CRM, cloud deployment sample, or Claude plugin.

## Development Rules

- Primary installable artifact: `skills/insurance_copilot/SKILL.md` plus its full support directory.
- Supporting skill files must live under `skills/insurance_copilot/references/`, `templates/`, `scripts/`, or `assets/`.
- Keep public institution packs public-source-only and schema-validated.
- Keep agent workspace template free of real customer data.
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
python3 scripts/validate_all_knowledge_packs.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
```

## Repository Layout

```text
skills/insurance_copilot/   Hermes skill package
standards/                   Evidence-driven public knowledge standard
schemas/                     Machine-readable schemas
prompts/                     Controlled LLM gateway prompt contracts
intake/                      Source packages before normalization
staging/                     Gateway output before review
knowledge/institutions/     Public institution knowledge packs
agent-workspace-template/   Template for private agent workspace
contributions/              Public contribution templates and workflow
examples/                   Synthetic sample inputs/expected outputs
evals/                      Static regression fixtures
cron/                       Hermes scheduled workflow recipes
mcp/                        Optional Hermes MCP/data connector contracts
scripts/                    Repo validation, packaging, eval, pack scripts
docs/                       Architecture, privacy, action safety, continuity, quality gates
```

## GitHub Remote

Expected remote:

```text
git@github.com-insurance-copilot:zlbzhf/insurance-copilot.git
```
