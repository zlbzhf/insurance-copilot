# Roadmap

This roadmap is durable project direction. Use it instead of relying on compressed chat history.

## Current Phase: Evidence-Driven Knowledge Architecture Beta

Goal: make `insurance-copilot` directly usable as a Hermes skill package and a three-layer insurance knowledge project with a standards-driven public ingestion pipeline:

1. public general workflow skill;
2. public, collaboratively maintained institution knowledge packs;
3. private agent workspaces for customer and non-public materials;
4. evidence-driven schema evolution for public knowledge standards.

## Completed Foundation

- Hermes-first standalone skill layout.
- Umbrella skill with workflow router.
- Core references for intake, gap analysis, product fit, compliance, policy review, replacement, claims, annuity/investment-linked review, renewal, and summaries.
- Templates for core outputs.
- Synthetic examples and expected output sketches.
- Static eval fixtures and runner.
- Packaging check and CI.
- Continuity, privacy, action-safety, jurisdiction adaptation, and quality-gate docs.
- Three-layer public/private knowledge architecture.
- Evidence-driven standards framework under `standards/`, `schemas/`, and `prompts/`.
- Deterministic ingestion gateway prototype under `scripts/ingest_gateway.py`.
- Local connector, renewal watcher, script-only cron wrapper, and private workspace readiness gate before scheduled monitoring.

## Priority 1 — Public Institution Knowledge Packs and Standards

- Stabilize `knowledge/institutions/_template/` schema.
- Maintain seed AIA/友邦 public pack without non-public claims.
- Add source-first contribution workflow and provenance rules.
- Use `standards/source-taxonomy.yaml` and `standards/page-type-registry.yaml` as canonical mappings.
- Evolve templates only through real-source schema gaps and reviewed proposals.
- Support future remote pack registry and selective page retrieval.
- Split mature institution packs into separate repos only when volume, maintainers, and release cadence justify it.

## Priority 2 — Ingestion Gateway

- Expand `scripts/ingest_gateway.py` from deterministic prototype into a maintained gateway.
- Add fixture tests for classification, schema gaps, and page rendering.
- Add optional maintainer-triggered LLM processing using `prompts/`, not automatic fork PR processing.
- Keep generated staging output separate from canonical `knowledge/` content.

## Priority 3 — Agent Private Workspace

- Keep private customer data and non-public institution materials outside this public repo.
- Improve `agent-workspace-template/` for private LLM-wiki organization.
- Add private pack/workspace validation that agents can run locally.
- Private workspace readiness gate before scheduled monitoring: structure, freshness, privacy/PII-like risks, output boundary, retention/audit readiness.
- Provide safe promotion path from private notes to public contribution bundles.

## Priority 4 — Better Regression Testing

- Add model-in-the-loop eval harness when Hermes exposes a stable noninteractive skill execution path.
- Add more golden outputs for product-line-specific cases.
- Add knowledge-pack validation cases for source records, wikilinks, frontmatter, and PII scans.
- Track regression results in release notes.

## Priority 5 — Optional Integrations

- Implement MCP servers or adapters for CRM, policy document KB, product library, compliance script library, and renewal register only after privacy/security/compliance approval.
- Keep connectors read-only by default.
- Add audit logs and source timestamps.

## Priority 6 — Release Management

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
