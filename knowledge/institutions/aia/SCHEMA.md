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
type: entity | product | concept | comparison | query | source-summary
institution: aia
jurisdiction: []
language: zh-Hans | zh-Hant | en | other
tags: []
sources: []
confidence: high | medium | low
public_source: true
needs_verification: true
---
```

## Source Record Fields

Source records live under `sources/*.yaml` and should include:

```yaml
id: source-id
institution: aia
jurisdiction: []
language: zh-Hans
source_type: official-web | official-brochure | official-terms | regulator | public-article | community-summary
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
