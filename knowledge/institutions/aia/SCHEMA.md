# AIA Institution Pack Schema

## Domain

Public insurance institution knowledge for a single insurer or insurance institution.

## Conventions

- File names: lowercase, hyphens, no spaces.
- Every wiki page starts with YAML frontmatter.
- Use `[[wikilinks]]` between product, concept, entity, comparison, and query pages.
- Every substantive page must cite one or more source records from `sources/`.
- Every new or updated page must be listed in `index.md`.
- Every contribution must update `log.md`.
- Public sources only.
- Use `[verify]` when product facts need current official confirmation.

## Required Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | product-summary | policy-contract-summary | marketing-compliance-review | underwriting-rule-summary | claims-process-summary | renewal-service-process | service-process-summary | regulatory-guidance-summary | faq-summary | comparison | query | source-summary
institution: aia
jurisdiction: []
language: zh-Hans | zh-Hant | en | other
tags: []
sources: []
confidence: high | medium | low
public_source: true
needs_verification: true
schema_version: 0.2.0
---
```

## Source-to-Page Mapping

This pack follows the canonical mapping in `standards/source-taxonomy.yaml` and `standards/page-type-registry.yaml`.

Core principle: do not force every source into one generic product template. Product brochures, policy contracts, marketing material, underwriting guidance, claims processes, renewal service pages, regulatory guidance, FAQs, and community summaries can require different page types.

Examples:

- `official-brochure` -> `product-summary`, `concept`, `comparison`
- `official-terms` -> `policy-contract-summary`, `product-summary`, `concept`
- `approved-marketing-material` -> `marketing-compliance-review`, `concept`
- `official-underwriting-guide` -> `underwriting-rule-summary`, `concept`
- `official-service-guide` -> `claims-process-summary`, `renewal-service-process`, `service-process-summary`, `concept`
- `regulator-guidance` -> `regulatory-guidance-summary`, `concept`

If a real public source does not fit the current mapping, record a schema gap instead of inventing a one-off local template.

## Schema Evolution

Standards evolve through `standards/schema-evolution.md`:

```text
Observe -> Propose -> Validate -> Review -> Migrate -> Release
```

LLMs and local agents may suggest schema gaps, but canonical schema changes require reviewed proposals. Each page should include `schema_version` once generated or updated under versioned standards.

## Source Record Fields

Source records live under `sources/*.yaml` and should include:

```yaml
id: source-id
institution: aia
jurisdiction: []
language: zh-Hans
source_type: regulator-guidance | official-terms | official-service-guide | official-underwriting-guide | official-product-page | official-brochure | official-faq | approved-marketing-material | public-article | community-summary | unknown
source_url: https://example.com
retrieved_at: YYYY-MM-DD
public_source: true
redistribution:
  mode: link-only | summary-allowed | full-text-allowed
product_lines: []
status: queued | processed | superseded
submitted_by: github-user-or-unknown
```

## Tag Taxonomy

Use tags from this list unless the schema is updated first:

- institution
- product
- life
- health
- medical
- critical-illness
- savings
- annuity
- underwriting
- disclosure
- claims
- renewal
- service
- compliance
- replacement
- exclusion
- waiting-period
- public-source
- needs-verification

## Specialized Page Types

Required sections for specialized page types are maintained in `standards/page-type-registry.yaml`. Pack-local templates live under `templates/pages/`.

## Product Pages

Required sections:

- Source Status
- Overview
- Key Features
- Limitations / Exclusions
- Eligibility / Underwriting Notes
- Customer-Facing Cautions
- Related Concepts
- Open Questions / Verify

## Concept Pages

Required sections:

- Definition
- Why It Matters
- Institution-Specific Notes
- Related Pages
- Sources / Verify

## Confidence Rules

- `high`: supported by current official source and reviewed.
- `medium`: supported by one public official source but needs more review.
- `low`: community summary, stale source, or incomplete source context.

## Contradictions

Do not silently overwrite conflicting information. Note both claims with dates and sources, set `contested: true`, and flag for maintainer review.
