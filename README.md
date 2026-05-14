# Insurance Copilot

Hermes-first insurance workflow copilot for licensed insurance professionals.

Insurance Copilot is inspired by the workflow discipline of `claude-for-legal`, but it is packaged for **Hermes Agent** as a full skill directory, not as a Claude plugin or web app.

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
- stakeholder summaries.

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
skills/insurance-copilot/
  SKILL.md                 Umbrella Hermes skill
  references/              Workflow playbooks
  templates/               Reusable output templates
  scripts/                 Skill-local helper scripts
examples/                  Synthetic sample cases and expected outputs
evals/                     Regression fixtures and expected outputs
cron/                      Scheduled workflow recipes for Hermes cron
mcp/                       Optional connector notes and contracts
docs/                      Design, privacy, action safety, quality gates
scripts/                   Repo validation, packaging, eval helpers
AGENTS.md                  Hermes project instructions
ROADMAP.md                 Durable project direction
```

## Validate

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
```

CI runs these checks on push and pull request.

## Production Readiness Notes

Before connecting production data or systems, read:

- `docs/privacy-and-data-handling.md`
- `docs/action-safety.md`
- `docs/jurisdiction-adaptation.md`
- `mcp/README.md`

Production use requires agency-specific compliance/legal review, source-of-truth integrations, access control, audit logging, retention rules, and licensed human supervision.
