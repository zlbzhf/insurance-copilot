# Cold-Start Interview

Use this workflow before substantive production use. The goal is to create or update the agency practice profile that all other Insurance Copilot workflows read.

## Output Location

Write the resulting profile only to a user-approved practice profile path, commonly:

`profiles/insurance-copilot-practice-profile.md`

If file access is unavailable or the user has not approved a destination, output a complete profile draft the user can save.

## Interview Method

Ask only the questions needed for the user's situation. Do not interrogate unnecessarily. Start broad, then ask follow-ups for product lines or channels the agency actually uses.

## Interview Sections

### 1. Agency Context

- Agency name and team structure.
- Jurisdictions served.
- License scope: life, health, P&C, annuity, investment-linked, group benefits, other.
- Distribution channel: in-person, phone, WeChat/WhatsApp, email, web leads, workplace seminars.
- Languages used with customers.

### 2. Product Universe

- Carriers represented.
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
