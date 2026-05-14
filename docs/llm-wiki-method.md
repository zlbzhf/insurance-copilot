# LLM Wiki Method for Insurance Knowledge

Insurance Copilot uses a Karpathy-style LLM wiki pattern for both public institution packs and private agent workspaces.

## Why This Matters

Insurance knowledge is document-heavy, versioned, jurisdiction-dependent, and easy to misquote. A wiki structure helps keep knowledge organized, sourced, and cross-linked instead of re-deriving context from raw documents every time.

## Core Files

```text
SCHEMA.md   pack-local conventions and links to canonical standards
index.md    catalog of pages and one-line summaries
log.md      append-only maintenance history
raw/        immutable source material when redistribution allows
sources/    source metadata records
entities/   institution/entity pages
products/   product summaries
contracts/  contract/terms summaries
marketing/  marketing compliance reviews
underwriting/ public underwriting/disclosure guidance
service-processes/ claims, renewal, payment, lapse, reinstatement processes
regulatory/ regulator guidance summaries
faqs/       public FAQ summaries
concepts/   reusable concept pages
comparisons/ side-by-side analyses
queries/    filed reusable query answers
templates/  source/page templates aligned with standards/
```

Canonical source type and page type definitions live in `standards/source-taxonomy.yaml` and `standards/page-type-registry.yaml`.

## Operating Loop

1. Orient: read `SCHEMA.md`, `index.md`, recent `log.md`, and the current standard in `standards/current.yaml`.
2. Add or review source records.
3. Run the gateway for new public sources when appropriate.
4. Review staging output, schema gaps, and proposed pages.
5. Create/update product, contract, marketing, service, regulatory, FAQ, concept, entity, comparison, or query pages.
6. Add wikilinks and confidence labels.
7. Update `index.md`.
8. Append to `log.md`.
9. Run validators.

## Evidence-Driven Standard Evolution

The wiki schema should become more precise as real documents are processed. If a source does not fit current templates, record a schema gap rather than forcing the source into a generic page. See `docs/evidence-driven-standards.md` and `standards/schema-evolution.md`.

## Insurance-Specific Rules

- Distinguish official contract/terms from brochure summaries.
- Mark stale or single-source claims as `confidence: low` or `medium`.
- Use `[verify]` for product availability, premiums, underwriting classes, riders, exclusions, renewal/lapse status, and claims status.
- Do not write final recommendations into public knowledge pages.
- Do not convert marketing language into guarantees.
