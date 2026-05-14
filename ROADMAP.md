# Roadmap

This roadmap is durable project direction. Use it instead of relying on compressed chat history.

## Current Phase: Layered Knowledge Architecture Beta

Goal: make `insurance-copilot` directly usable as a Hermes skill package and a three-layer insurance knowledge project:

1. public general workflow skill;
2. public, collaboratively maintained institution knowledge packs;
3. private agent workspaces for customer and non-public materials.

## Completed Foundation

- Hermes-first standalone skill layout.
- Umbrella skill with workflow router.
- Core references for intake, gap analysis, product fit, compliance, policy review, replacement, claims, annuity/investment-linked review, renewal, and summaries.
- Templates for core outputs.
- Synthetic examples and expected output sketches.
- Static eval fixtures and runner.
- Packaging check and CI.
- Continuity, privacy, action-safety, jurisdiction adaptation, and quality-gate docs.

## Priority 1 — Public Institution Knowledge Packs

- Stabilize `knowledge/institutions/_template/` schema.
- Maintain seed AIA/友邦 public pack without non-public claims.
- Add source-first contribution workflow and provenance rules.
- Support future remote pack registry and selective page retrieval.
- Split mature institution packs into separate repos only when volume, maintainers, and release cadence justify it.

## Priority 2 — Agent Private Workspace

- Keep private customer data and non-public institution materials outside this public repo.
- Improve `agent-workspace-template/` for private LLM-wiki organization.
- Add private pack/workspace validation that agents can run locally.
- Provide safe promotion path from private notes to public contribution bundles.

## Priority 3 — Better Regression Testing

- Add model-in-the-loop eval harness when Hermes exposes a stable noninteractive skill execution path.
- Add more golden outputs for product-line-specific cases.
- Add knowledge-pack validation cases for source records, wikilinks, frontmatter, and PII scans.
- Track regression results in release notes.

## Priority 4 — Optional Integrations

- Implement MCP servers or adapters for CRM, policy document KB, product library, compliance script library, and renewal register only after privacy/security/compliance approval.
- Keep connectors read-only by default.
- Add audit logs and source timestamps.

## Priority 5 — Release Management

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
- Public storage of non-public institution materials.
