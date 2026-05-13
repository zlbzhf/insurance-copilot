# Insurance Copilot

A Claude-style insurance-copilot workflow plugin inspired by `anthropics/claude-for-legal`.

This repository is intentionally focused on the plugin/agent structure, not a web application. The main project lives in:

```text
insurance-copilot/
```

## Purpose

Help licensed insurance agents and agency teams draft, organize, and review insurance workflow outputs:

- customer fact-find and needs intake;
- coverage gap analysis;
- product-fit and suitability review;
- objection-handling scripts;
- compliance screening for sales copy;
- existing policy review and replacement cautions;
- renewal/lapse follow-up;
- stakeholder summaries.

## Non-Negotiable Boundary

Every output is a draft for licensed agent and compliance review. This project does not provide binding insurance advice, legal advice, tax advice, investment advice, underwriting decisions, claims decisions, or product guarantees.

## Project Structure

```text
insurance-copilot/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── CLAUDE.md
├── README.md
├── connectors/
│   └── README.md
├── managed-agent-cookbooks/
│   └── README.md
├── references/
│   └── compliance-starter.md
└── skills/
    ├── cold-start-interview/
    ├── client-needs-intake/
    ├── coverage-gap-analysis/
    ├── product-fit-review/
    ├── objection-response/
    ├── compliance-check/
    ├── policy-review/
    ├── renewal-review/
    └── stakeholder-summary/
```

## Core Pattern Borrowed from `claude-for-legal`

- A practice-area plugin folder.
- `.claude-plugin/plugin.json` metadata.
- `CLAUDE.md` as the shared practice profile and safety policy.
- Workflow-specific `skills/`.
- A `cold-start-interview` skill that learns the agency playbook.
- MCP connector placeholders for CRM, product library, and knowledge base.
- Managed-agent cookbooks for recurring monitoring workflows.
- Human-review gates before consequential actions.

## First Command

```text
/insurance-copilot:cold-start-interview
```

Use this first to define jurisdiction, license scope, product universe, compliance rules, escalation paths, and preferred output formats.

## Important Files

- `insurance-copilot/CLAUDE.md` — global insurance-copilot practice profile.
- `insurance-copilot/skills/*/SKILL.md` — workflow definitions.
- `insurance-copilot/.mcp.json` — placeholder connectors.
- `insurance-copilot/managed-agent-cookbooks/README.md` — scheduled/monitoring agent patterns.
- `insurance-copilot/references/compliance-starter.md` — starter compliance checklist.
