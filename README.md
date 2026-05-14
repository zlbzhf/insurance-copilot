# Insurance Copilot

Hermes-first insurance workflow copilot and layered insurance knowledge project for licensed insurance professionals.

Insurance Copilot is inspired by the workflow discipline of `claude-for-legal`, but it is packaged for **Hermes Agent** as a full skill directory and public/private knowledge architecture, not as a Claude plugin or web app.

## Architecture

Insurance Copilot has three layers:

1. **General public workflow skill** — `skills/insurance-copilot/`
2. **Public institution knowledge packs** — `knowledge/institutions/`
3. **Agent private knowledge workspace** — initialize from `agent-workspace-template/`, store privately outside this repo

Public knowledge maintenance also uses an evidence-driven standards loop:

```text
public source -> intake -> gateway staging -> schema gaps/proposed pages -> review -> knowledge pack
```

See `docs/architecture.md` and `docs/evidence-driven-standards.md` for the full design.

## What It Does

Insurance Copilot helps licensed insurance professionals create structured drafts for:

- agency playbook cold-start interviews;
- client needs intake;
- coverage gap analysis;
- product-fit review;
- objection response scripts;
- compliance language screening;
- existing policy review;
- replacement/surrender suitability triage;
- claims question triage;
- annuity or investment-linked caution review;
- renewal/lapse follow-up planning;
- stakeholder summaries;
- public institution knowledge-pack organization.

## What It Does Not Do

It does not provide binding insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decisions. It does not automatically send customer messages, submit applications, file claims, cancel/replace coverage, or make binding representations.

Every customer-facing output is a draft for licensed/compliance review.

## Install into Hermes

Install the **full skill directory** so linked `references/` and `templates/` are available:

```bash
mkdir -p ~/.hermes/skills/insurance/insurance-copilot
cp -R skills/insurance-copilot/* ~/.hermes/skills/insurance/insurance-copilot/
```

Then start a new Hermes session and load:

```text
/skill insurance-copilot
```

Important: a raw `SKILL.md`-only install is not enough unless your Hermes version also fetches linked files. This repository assumes the full directory is installed.

## Smoke Test After Install

```bash
test -f ~/.hermes/skills/insurance/insurance-copilot/SKILL.md
test -f ~/.hermes/skills/insurance/insurance-copilot/references/client-needs-intake.md
test -f ~/.hermes/skills/insurance/insurance-copilot/templates/practice-profile.md
```

In Hermes, try:

```text
/skill insurance-copilot
Help me run a cold-start interview for an insurance agency. Ask only the first few essential questions.
```

## Public Institution Packs

Public institution packs live under:

```text
knowledge/institutions/
```

They are public, collaboratively maintained, Karpathy-style LLM wiki knowledge bases. They may contain public source records, public product/service summaries, concepts, comparisons, and query pages.

They must not contain customer data, non-public institution materials, private agent notes, secrets, or production exports.

See:

- `docs/public-knowledge-packs.md`
- `docs/llm-wiki-method.md`
- `docs/evidence-driven-standards.md`
- `docs/github-knowledge-governance.md`
- `knowledge/registry.json`

## Agent Private Workspace

Private customer knowledge and non-public institution materials belong outside the public repo. Start from:

```text
agent-workspace-template/
```

Suggested private location:

```bash
mkdir -p ~/.insurance-copilot/agents/<agent-id>
cp -R agent-workspace-template/* ~/.insurance-copilot/agents/<agent-id>/
```

See `docs/agent-private-knowledge.md`.

## Quickstart

See:

```text
docs/quickstart.md
```

The quickstart walks through:

1. cold-start practice profile;
2. client intake;
3. coverage gap analysis;
4. product-fit review;
5. compliance check;
6. stakeholder summary.

## Repository Layout

```text
skills/insurance-copilot/     Umbrella Hermes skill package
standards/                     Versioned public-knowledge standard and schema evolution policy
schemas/                       Machine-readable schemas for intake/classification/extraction/gaps
prompts/                       Prompt contracts for future controlled LLM gateway runs
intake/                        Source package templates before canonical processing
staging/                       Gateway output before human-reviewed merge
knowledge/institutions/       Public institution LLM wiki packs
agent-workspace-template/     Template for private agent knowledge workspace
contributions/                Public contribution templates and workflow docs
examples/                     Synthetic sample cases and expected outputs
evals/                        Regression fixtures and expected outputs
cron/                         Scheduled workflow recipes for Hermes cron
mcp/                          Optional connector notes and contracts
docs/                         Architecture, privacy, action safety, quality gates
scripts/                      Repo validation, packaging, eval, pack helpers
AGENTS.md                     Hermes project instructions
ROADMAP.md                    Durable project direction
```

## Validate

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
```

CI runs these checks on push and pull request.

## Production Readiness Notes

Before connecting production data or systems, read:

- `docs/privacy-and-data-handling.md`
- `docs/action-safety.md`
- `docs/jurisdiction-adaptation.md`
- `mcp/README.md`

Production use requires institution/practice-specific compliance/legal review, source-of-truth integrations, access control, audit logging, retention rules, and licensed human supervision.
