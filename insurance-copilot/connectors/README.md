# Insurance Copilot Connectors

Connector placeholders for production integration.

## CRM Connector

Expected capabilities:

- Read customer profile and interaction notes.
- Read policy list and renewal dates.
- Write draft notes only after human approval.
- Enforce PII/PHI minimization and audit logs.

## Product Library Connector

Expected capabilities:

- Search current product contracts, riders, underwriting guides, rate sheets, and approved brochures.
- Return source citations with version/date.
- Mark stale or superseded documents.

## Compliance Knowledge Connector

Expected capabilities:

- Search approved scripts, forbidden phrases, regulator guidance, carrier notices, and agency SOPs.
- Return jurisdiction and effective date.
- Support escalation routing.

## Messaging Connector

Expected capabilities:

- Draft-only by default.
- Require explicit approval before sending.
- Preserve customer communication logs.
