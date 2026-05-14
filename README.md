# Insurance Copilot

Hermes-first insurance workflow copilot and layered insurance knowledge project for licensed insurance professionals.

Insurance Copilot is inspired by the workflow discipline of `claude-for-legal`, but it is packaged for **Hermes Agent** as a full skill directory and public/private knowledge architecture, not as a Claude plugin or web app.

## Start Here: Practitioner Workflows

Start with a practical insurance job, not the standards pipeline. In Hermes, load the skill and ask for one of these workflows by name:

1. **Agency Playbook Builder** — create the practice profile and operating guardrails before customer work.
2. **Daily Agent Workbench** — plan today's meetings, follow-ups, renewal/lapse items, claims support, referrals, and draft messages.
3. **Client Needs Intake** — turn notes or a call transcript into a structured fact-find.
4. **Coverage Gap Drafter** — map known responsibilities and risks to possible gap areas without selecting products.
5. **Client Plan Draft** — combine intake, gap notes, and source-backed product facts into a review-ready proposal draft.
6. **Product Fit Reviewer** — compare a sourced product to documented needs without final-advice language.
7. **Compliance Copy Checker** — review customer-facing copy for risky claims, missing caveats, and escalation needs.
8. **Policy Review Assistant** — summarize existing policies before renewal, cross-sell, upsell, cancellation, surrender, or replacement discussion.
9. **Replacement Risk Triager** — treat any replacement, surrender, cancellation, reduction, or exchange as high-risk triage.
10. **Renewal/Lapse Follow-up Planner** — sort due dates, grace periods, lapse risk, and outreach drafts with carrier-status verification.
11. **Claims Support Triage** — organize claim facts, documents, deadlines, and neutral service language without deciding coverage or payout.
12. **Objection Response Drafter** — draft low-pressure, compliant responses to customer objections.
13. **Referral Ask Drafter** — create soft, non-misleading referral requests with opt-out language.
14. **Stakeholder Summary Writer** — separate agent, manager, compliance, and customer-safe summaries.
15. **Institution Knowledge Organizer** — organize public insurer/institution sources through the evidence-driven pack workflow.

If no practice profile exists, only use generic education, intake, missing-information checklists, or **Agency Playbook Builder** until the profile is supplied. Do not ask Insurance Copilot for specific product-fit conclusions, replacement suggestions, reusable customer scripts, or external-action drafts unless the profile/context is supplied or the output is clearly labeled provisional.

See `docs/workflow-surface.md` for when to use each workflow, required inputs, outputs, review owners, forbidden actions, and standard prompts.

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

1. cold-start practice profile gate;
2. Daily Agent Workbench loop;
3. client intake;
4. coverage gap drafting;
5. client plan/product-fit draft;
6. compliance check;
7. stakeholder summary.

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
