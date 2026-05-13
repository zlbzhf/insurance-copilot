---
name: cold-start-interview
description: Learn an insurance agency's playbook before running other workflows.
---

# Cold-Start Interview

Use this skill before any substantive workflow. The goal is to create or update the agency practice profile that all other insurance-agent skills read.

## Output Location

Write the resulting profile to the configured plugin profile path, typically:

`~/.claude/plugins/config/insurance-agent/insurance-agent/CLAUDE.md`

If file access is unavailable, output a complete profile draft the user can paste into that path.

## Interview Sections

Ask only the questions needed for the user's situation; do not interrogate unnecessarily.

### 1. Agency Context

- Agency name and team structure.
- Jurisdictions served.
- License scope: life, health, P&C, annuity, investment-linked, group benefits, other.
- Distribution channel: in-person, phone, WeChat/WhatsApp, email, web leads, workplace seminars.

### 2. Product Universe

- Carriers represented.
- Product lines in scope.
- Products excluded from AI assistance.
- Source hierarchy for product facts: policy contracts, rider docs, carrier portal, approved brochure, internal SOP.

### 3. Customer Segments

- Primary customer types: families, young professionals, retirees, business owners, high-net-worth, group clients.
- Vulnerable-customer rules.
- Languages and tone preferences.

### 4. Suitability Playbook

- Minimum facts required before recommendation.
- Budget rules.
- Replacement/surrender review rules.
- Health disclosure and underwriting rules.
- Required comparison format.

### 5. Compliance Rules

- Forbidden phrases.
- Required disclaimers.
- Approval workflow before sending externally.
- Escalation contacts or roles.

### 6. Outputs

- Preferred formats for intake notes, product comparisons, customer scripts, manager summaries, and compliance flags.
- Required citation style.

## Profile Template

Produce this structure:

```markdown
# Insurance Agent Practice Profile

## Agency Context
- Agency:
- Jurisdictions:
- License scope:
- Channels:

## Product Universe
- Carriers:
- Product lines:
- Excluded products:
- Source hierarchy:

## Customer Segments
- Primary segments:
- Vulnerable customer rules:
- Languages/tone:

## Suitability Playbook
- Minimum customer facts:
- Budget rules:
- Replacement/surrender rules:
- Health disclosure rules:
- Comparison requirements:

## Compliance Rules
- Forbidden claims:
- Required disclaimers:
- Approval workflow:
- Escalation triggers:

## Output Formats
- Intake:
- Product-fit review:
- Customer script:
- Compliance check:
- Stakeholder summary:
```

## Completion Criteria

- The profile clearly says what the assistant may and may not do.
- It lists required facts before recommendations.
- It defines escalation gates.
- It includes source hierarchy and citation expectations.
