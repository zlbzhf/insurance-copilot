# Roadmap

This roadmap is durable project direction. Use it instead of relying on compressed chat history.

## Current Phase: Hermes Skill Hardening

Goal: make `insurance-copilot` a reliable Hermes skill package that can be installed, loaded, validated, and extended safely.

### Priority 1 — Skill Quality

- Expand each workflow reference into a complete playbook.
- Add more templates for product-fit review, policy review, renewal review, and stakeholder summary.
- Add explicit escalation criteria for replacement/surrender, vulnerable customers, and investment-linked products.

### Priority 2 — Examples and Regression Fixtures

- Add synthetic examples for family protection, policy replacement, renewal/lapse, product comparison, and unsafe marketing copy.
- Add expected-output sketches that future contributors can compare against.
- Keep examples non-sensitive and clearly synthetic.

### Priority 3 — Validation and CI

- Keep `scripts/validate_repo.py` strict enough to prevent drift.
- Add checks when new required files/workflows are introduced.
- Keep GitHub Actions validator green.

### Priority 4 — Optional Integrations

- Document MCP connector patterns for CRM, policy knowledge base, product library, and approved scripts.
- Add Hermes cron recipes for renewal watcher, compliance copy monitor, and replacement-risk monitor.
- Do not connect production customer data until privacy, access control, audit logging, and compliance review are designed.

## Out of Scope Unless Explicitly Requested

- Web application UI/backend.
- Claude plugin packaging as the primary interface.
- Carrier quote engine or policy admin integration.
- Automated customer message sending.
- Final regulated advice or compliance approval automation.
