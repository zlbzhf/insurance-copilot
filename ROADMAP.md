# Roadmap

This roadmap is durable project direction. Use it instead of relying on compressed chat history.

## Current Phase: Productized Hermes Skill Beta

Goal: make `insurance-copilot` directly usable as a Hermes skill package for licensed insurance professionals, with safety boundaries, references, templates, examples, static evals, packaging checks, and CI.

## Completed Foundation

- Hermes-first standalone skill layout.
- Umbrella skill with workflow router.
- Core references for intake, gap analysis, product fit, compliance, policy review, replacement, claims, annuity/investment-linked review, renewal, and summaries.
- Templates for core outputs.
- Synthetic examples and expected output sketches.
- Static eval fixtures and runner.
- Packaging check and CI.
- Continuity, privacy, action-safety, jurisdiction adaptation, and quality-gate docs.

## Priority 1 — Practice-Specific Hardening

- Add a real agency-approved practice profile outside the public repo.
- Encode jurisdiction/product-line specific disclaimers, replacement forms, advertising limits, and escalation roles.
- Add agency-approved scripts and forbidden phrases as private references.

## Priority 2 — Better Regression Testing

- Add model-in-the-loop eval harness when Hermes exposes a stable noninteractive skill execution path.
- Add more golden outputs for product-line-specific cases.
- Track regression results in release notes.

## Priority 3 — Optional Integrations

- Implement MCP servers or adapters for CRM, policy document KB, product library, compliance script library, and renewal register only after privacy/security/compliance approval.
- Keep connectors read-only by default.
- Add audit logs and source timestamps.

## Priority 4 — Release Management

- Tag beta releases after validation.
- Keep `CHANGELOG.md` current.
- Use `docs/release-checklist.md` before release.

## Out of Scope Unless Explicitly Requested

- Web application UI/backend.
- Claude plugin packaging as the primary interface.
- Carrier quote engine or policy admin integration.
- Automated customer message sending.
- Final regulated advice or compliance approval automation.
- Production customer-data storage in this public repository.
