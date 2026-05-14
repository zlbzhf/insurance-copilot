# LLM Wiki Method for Insurance Knowledge

Insurance Copilot uses a Karpathy-style LLM wiki pattern for both public institution packs and private agent workspaces.

## Why This Matters

Insurance knowledge is document-heavy, versioned, jurisdiction-dependent, and easy to misquote. A wiki structure helps keep knowledge organized, sourced, and cross-linked instead of re-deriving context from raw documents every time.

## Core Files

```text
SCHEMA.md   conventions, page types, taxonomy, confidence rules
index.md    catalog of pages and one-line summaries
log.md      append-only maintenance history
raw/        immutable source material when allowed
sources/    source metadata records
products/   product pages
concepts/   reusable concept pages
entities/   institution/entity pages
```

## Operating Loop

1. Orient: read `SCHEMA.md`, `index.md`, recent `log.md`.
2. Add or review source records.
3. Create/update product, concept, entity, comparison, or query pages.
4. Add wikilinks and confidence labels.
5. Update `index.md`.
6. Append to `log.md`.
7. Run validators.

## Insurance-Specific Rules

- Distinguish official contract/terms from brochure summaries.
- Mark stale or single-source claims as `confidence: low` or `medium`.
- Use `[verify]` for product availability, premiums, underwriting classes, riders, exclusions, renewal/lapse status, and claims status.
- Do not write final recommendations into public knowledge pages.
- Do not convert marketing language into guarantees.
