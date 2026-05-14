# Evidence-Driven Standards

Insurance Copilot does not assume that the first set of templates is final. Public insurance documents vary by institution, jurisdiction, product line, channel, and publication format. The standard therefore evolves through real source processing.

## Problem

A one-time template taxonomy is too brittle. If maintainers invent templates only from examples, the project becomes experience-driven rather than evidence-driven. If contributors upload local Hermes outputs directly, the public pack becomes inconsistent because different agents and models have different capability levels.

## Design Principle

```text
Contributors provide evidence.
The gateway normalizes evidence.
Schemas constrain outputs.
Humans review changes.
Standards evolve through proposals.
```

## Four Layers

1. **Raw / Source Layer** — public source records and allowed excerpts.
2. **Extraction Layer** — structured classification and canonical extraction records.
3. **Canonical Knowledge Layer** — reviewed source-backed claims and pages.
4. **Rendered Wiki Layer** — human-readable markdown pages in public institution packs.

The ingestion path should not be `raw -> LLM -> final markdown`. It should be:

```text
source record + raw text
  -> classification
  -> extraction record
  -> schema-gap report
  -> proposed pages
  -> validation
  -> human review
  -> knowledge pack merge
```

## Standard Evolution Loop

```text
Observe -> Propose -> Validate -> Review -> Migrate -> Release
```

- **Observe:** gateway or reviewer finds that real public sources do not fit the current schema.
- **Propose:** create a schema gap or proposal under `standards/proposals/`.
- **Validate:** test the change against real sources and existing pages.
- **Review:** schema and institution maintainers decide whether the change is useful beyond a one-off case.
- **Migrate:** update validators, templates, prompts, and existing pages if needed.
- **Release:** update `standards/current.yaml` and `standards/changelog.md`.

## Contributor Quality Strategy

Contributors have different local Hermes setups and model capabilities, so the public repository should not treat local drafts as canonical.

Contributor tiers:

- **Source-only contributor:** submits public URL/source metadata. Lowest barrier and safest default.
- **Draft contributor:** includes a local draft, treated as hints only.
- **Trusted curator:** may submit proposed pages but still needs validators and review.
- **Pack maintainer:** reviews pack-specific content under CODEOWNER-style governance.

## LLM Use

LLMs can help classify, extract, and propose schema gaps, but canonical changes require deterministic validation and human review.

GitHub Actions can run deterministic validation by default. LLM processing should be maintainer-approved because fork PRs, secrets, prompt injection, copyright risk, and privacy mistakes require controlled handling.

## Current Implementation

- `standards/` defines current schema versions, source taxonomy, page type registry, and quality policy.
- `schemas/` contains machine-readable schemas.
- `prompts/` contains prompt contracts for future LLM-assisted gateway runs.
- `scripts/ingest_gateway.py` is a deterministic prototype that writes staging outputs without merging to `knowledge/`.
- `staging/` documents normalized gateway output.
- `intake/` documents source package input.
