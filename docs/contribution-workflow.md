# Public Knowledge Contribution Workflow

This workflow keeps public institution packs consistent across many contributors and many local Hermes setups.

## Do Not Directly Upload Local Private Wikis

Agent-local Hermes instances may help organize documents, but public contributions must be normalized through schema and validation. Do not copy private workspace pages directly into `knowledge/institutions/`.

## Preferred Contribution Bundle

```text
contributions/<institution>/<github-user>/<date-topic>/
├── contribution.yaml
├── sources/
│   └── source-record.yaml
├── proposed-pages/
│   └── products/example-product.md
├── provenance.json
└── notes.md
```

## Review Checklist

- Source is public/shareable or link-only.
- No customer data.
- No non-public/confidential institution material.
- Proposed pages cite source records.
- Confidence and `[verify]` markers are appropriate.
- Wikilinks resolve.
- Validator passes.

## Commands

```bash
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_repo.py
```
