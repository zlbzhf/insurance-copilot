# Insurance Agent Plugin

A Claude-style plugin inspired by the structure of `anthropics/claude-for-legal`, adapted for insurance agency workflows.

## Core Principle

Every output is a draft for licensed insurance-agent and compliance review. The plugin helps with intake, issue spotting, product-fit analysis, objection handling, renewal follow-up, and stakeholder summaries. It does **not** make underwriting decisions, sell products, guarantee outcomes, or replace licensed professional judgment.

## What This Mirrors from `claude-for-legal`

- Practice-area plugin folder with `.claude-plugin/plugin.json`.
- A large `CLAUDE.md` practice profile read by every skill.
- `skills/` directory with workflow-specific skills.
- Cold-start interview to learn the agency playbook.
- MCP connector placeholders for CRM, product library, and knowledge base.
- Scheduled/managed agent cookbook placeholders for monitoring workflows.
- Safety-first output: source markers, assumptions, uncertainty flags, and gates before irreversible actions.

## Target Users

- Licensed insurance agents / brokers.
- Agency managers.
- Sales support staff.
- Compliance reviewers.
- Customer service / renewal teams.

## Core Commands

- `/insurance-agent:cold-start-interview` — learn the agency playbook.
- `/insurance-agent:client-needs-intake` — collect customer facts and missing questions.
- `/insurance-agent:coverage-gap-analysis` — identify protection gaps.
- `/insurance-agent:product-fit-review` — review product fit and suitability cautions.
- `/insurance-agent:objection-response` — draft compliant objection-handling scripts.
- `/insurance-agent:compliance-check` — screen copy/scripts for risky claims.
- `/insurance-agent:policy-review` — summarize existing policy and replacement cautions.
- `/insurance-agent:renewal-review` — review upcoming renewal/lapse/action dates.
- `/insurance-agent:stakeholder-summary` — create concise summaries for customers, agents, or managers.

## Quick Start

1. Install or load this plugin folder in a Claude-compatible plugin environment.
2. Run:

```text
/insurance-agent:cold-start-interview
```

3. Answer questions about jurisdiction, license scope, carrier/product universe, customer segments, prohibited claims, escalation rules, and preferred output formats.
4. Use workflow commands such as:

```text
/insurance-agent:client-needs-intake
/insurance-agent:coverage-gap-analysis
/insurance-agent:product-fit-review product.pdf customer-notes.md
/insurance-agent:compliance-check sales-script.md
```

## Cold-Start Output

The cold-start interview should produce or update a plain-English practice profile similar to:

```text
~/.claude/plugins/config/insurance-agent/insurance-agent/CLAUDE.md
```

That profile should define:

- Jurisdictions and license context.
- Product lines and carriers in scope.
- Approved claims and forbidden phrases.
- Suitability and replacement review requirements.
- Escalation paths.
- Required disclaimers.
- Preferred customer-facing tone.

## Safety Gates

Require explicit human confirmation before:

- Sending customer communications.
- Submitting applications.
- Advising replacement/surrender/cancellation.
- Making claims or underwriting representations.
- Using marketing copy externally.
- Recording sensitive health/financial data in external systems.

## Limitations

- This project currently provides plugin instructions and workflow templates, not a production CRM or policy administration system.
- Connector entries in `.mcp.json` are placeholders and must be replaced with real agency-approved connectors.
- Product and regulatory information must be verified against current carrier, policy, and regulator sources.
