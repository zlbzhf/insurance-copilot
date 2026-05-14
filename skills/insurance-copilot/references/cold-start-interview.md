# Cold-Start Interview

Use this workflow before substantive production use. The goal is to create or update the agency practice profile that all other Insurance Copilot workflows read.

## Output Location

Write the resulting profile only to a user-approved practice profile path, commonly:

`profiles/insurance-copilot-practice-profile.md`

If file access is unavailable or the user has not approved a destination, output a complete profile draft the user can save.

## Quick Start vs Full Setup

Use **Quick Start** when the user needs to begin practical work in the same session. Ask only:

1. jurisdiction(s) and license/product scope;
2. carrier/product lines in scope;
3. compliance reviewer or approval role;
4. source hierarchy for product/policy facts;
5. external-message restrictions and forbidden phrases;
6. where private customer data may be stored, if anywhere.

Use **Full Setup** before production rollout or reusable customer-facing workflows. Full Setup should cover every section below and mark unknowns as `[confirm with compliance/legal]`.

Before the profile exists, downstream workflows must remain generic/provisional: education, intake, missing-fact checklists, neutral source organization, and internal drafts only.

## Interview Method

Ask only the questions needed for the user's situation. Do not interrogate unnecessarily. Start broad, then ask follow-ups for product lines or channels the agency actually uses.

## Interview Sections

### 1. Agency Context

- Agency name and team structure.
- Jurisdictions served.
- License scope: life, health, P&C, annuity, investment-linked, group benefits, other.
- Distribution channel: in-person, phone, WeChat/WhatsApp, email, web leads, workplace seminars.
- CRM/tool status and where private agent workspace data may live.
- Languages used with customers.

### 2. Product Universe

- Carriers represented, including whether AIA/友邦 or another public institution pack is relevant.
- AIA/public pack preference and whether public-only source use is required.
- Product lines in scope.
- Products excluded from AI assistance.
- Source hierarchy for product facts: policy contracts, rider docs, carrier portal, approved brochure, internal SOP.
- Whether cash-value, annuity, dividend, market-linked, or investment-oriented products are in scope.

### 3. Customer Segments

- Primary customer types: families, young professionals, retirees, business owners, high-net-worth, group clients.
- Vulnerable-customer rules.
- Languages and tone preferences.
- Channel restrictions and approval requirements.

### 4. Suitability Playbook

- Minimum facts required before recommendation.
- Budget rules.
- Replacement/surrender review rules.
- Health disclosure and underwriting rules.
- Claims-handling boundaries.
- Required comparison format.

### 5. Compliance Rules

- Approved script sources.
- Forbidden phrases.
- Required disclaimers.
- Approval workflow before sending externally.
- Escalation contacts or roles.
- Required forms and record-retention expectations.

### 6. Outputs

- Preferred formats for intake notes, product comparisons, customer scripts, manager summaries, and compliance flags.
- Required citation style.
- Where practice profiles and approved scripts should be stored.

## Output Format

```markdown
# Insurance Copilot Practice Profile

## Agency Context
- Agency:
- Jurisdictions:
- License scope:
- Channels:
- Languages:

## Product Universe
- Carriers:
- Product lines:
- Excluded products:
- Source hierarchy:
- High-risk product lines:

## Customer Segments
- Primary segments:
- Vulnerable customer rules:
- Languages/tone:
- Channel restrictions:

## Suitability Playbook
- Minimum customer facts:
- Budget rules:
- Replacement/surrender rules:
- Health disclosure rules:
- Claims-handling boundaries:
- Comparison requirements:

## Compliance Rules
- Forbidden claims:
- Required disclaimers:
- Approval workflow:
- Escalation triggers:
- Required forms:
- Record retention:

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
- It defines escalation gates and side-effect boundaries.
- It includes source hierarchy, citation expectations, privacy/data-handling expectations, and approval workflow.

## Guardrails

- Do not invent agency rules; mark unknowns.
- Do not treat starter compliance text as jurisdiction-specific legal advice.
- Do not write sensitive customer data into the practice profile.
- If the user cannot answer compliance questions, create a draft profile with `[confirm with compliance/legal]` markers.
