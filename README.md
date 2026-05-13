# Insurance Copilot

Hermes-first insurance workflow copilot for licensed insurance professionals.

This project is inspired by the structure and safety discipline of `claude-for-legal`, but it is packaged for **Hermes Agent** as an installable skill, not as a Claude plugin.

## Status

Current status: early Hermes skill package.

Usable for:

- agency playbook cold-start interviews;
- client needs intake structuring;
- coverage gap analysis drafts;
- product-fit review drafts;
- objection response drafts;
- compliance language screening;
- existing policy review summaries;
- renewal/lapse follow-up planning;
- stakeholder summaries.

Not yet a full production insurance system. It does not connect to carrier portals, CRM systems, policy databases, quote engines, or compliance approval systems by default.

## Install into Hermes

From a local clone:

```bash
mkdir -p ~/.hermes/skills/insurance/insurance-copilot
cp -R skills/insurance-copilot/* ~/.hermes/skills/insurance/insurance-copilot/
```

Then start a new Hermes session and load:

```text
/skill insurance-copilot
```

From GitHub raw URL, if your Hermes version supports direct skill URL installation:

```bash
hermes skills install https://raw.githubusercontent.com/zlbzhf/insurance-copilot/main/skills/insurance-copilot/SKILL.md --name insurance-copilot
```

For local development inside this repository, run Hermes with this repo as the working directory so `AGENTS.md` is included in project context.

## Repository Layout

```text
skills/insurance-copilot/
  SKILL.md                 Umbrella Hermes skill
  references/              Workflow playbooks
  templates/               Reusable output templates
  scripts/                 Skill-local helper scripts
examples/                  Non-sensitive sample cases
cron/                      Scheduled workflow recipes for Hermes cron
mcp/                       Optional connector notes
scripts/validate_repo.py   Repository validator
AGENTS.md                  Hermes project instructions
```

## Safety Boundary

Insurance Copilot assists licensed insurance professionals with drafts and structured analysis. It does not provide binding insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decisions.

Every customer-facing output should be reviewed by the appropriate licensed professional and, where required, compliance/legal supervision.

## Validate

```bash
python3 scripts/validate_repo.py
```

## Development Roadmap

1. Harden the umbrella Hermes skill and linked workflow references.
2. Add realistic non-sensitive examples and expected outputs.
3. Add optional MCP connector recipes for CRM/product/policy knowledge bases.
4. Add Hermes cron recipes for renewal watch, compliance copy monitor, and replacement-risk review.
5. Build evaluation fixtures for compliance and hallucination regression testing.
