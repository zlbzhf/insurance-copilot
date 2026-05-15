# Public Knowledge Contribution Workflow

This workflow keeps public institution packs consistent across many contributors and many local Hermes setups.

## Rule: Do Not Directly Upload Local Private Wikis

Agent-local Hermes instances may help organize documents, but public contributions must be normalized through schema and validation. Do not copy private workspace pages directly into `knowledge/institutions/`.

## Preferred Flow

```text
public source package
  -> intake validation
  -> gateway classification
  -> canonical extraction record
  -> proposed wiki pages
  -> schema-gap report when needed
  -> deterministic validators
  -> human review
  -> merge into public institution pack
```

## Preferred Contribution Bundle

```text
contributions/<institution>/<github-user>/<date-topic>/
├── contribution.yaml
├── sources/
│   └── source-record.yaml
├── raw/
│   └── optional-public-excerpt-or-README.md
├── proposed-pages/
│   └── optional-local-draft.md
├── provenance.json
└── notes.md
```

Local drafts are useful hints, not canonical truth. The gateway should re-check the raw/source evidence.

## Source-Only Contribution

The safest contribution is a source-only bundle:

```text
source_url + institution + jurisdiction + source_type_hint + public boundary declarations
```

A maintainer or gateway can then classify and extract consistently.

## Gateway Command

For a source record:

```bash
python3 scripts/ingest_gateway.py path/to/source-record.yaml --raw-text path/to/public-excerpt.md
```

This writes:

```text
staging/<institution>/<source-id>/
├── classification.yaml
├── extraction.yaml
├── proposed-pages/
├── provenance.json
├── schema-gaps.yaml
└── validation-report.md
```

Staging output is not canonical. Human review is required before moving approved pages into `knowledge/institutions/<institution>/`.

## Schema Gaps

If the source does not fit current source types or page types, do not force it into the closest template. Record a schema gap using `standards/schema-evolution.md` and `schemas/schema-gap.schema.json`.

## Review Checklist

- Source is public/shareable or link-only.
- No customer data.
- No non-public/confidential institution material.
- Source type and page type follow `standards/source-taxonomy.yaml` and `standards/page-type-registry.yaml`.
- Proposed pages cite source records.
- Confidence and `[verify]` markers are appropriate.
- Wikilinks resolve.
- Gateway output is reviewed, not blindly merged.
- Validator passes.

## Commands

```bash
python3 scripts/validate_all_knowledge_packs.py
python3 scripts/validate_repo.py
```
