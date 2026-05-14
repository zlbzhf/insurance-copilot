# Staging

Staging contains normalized gateway output before it is reviewed and merged into public institution packs.

Typical output:

```text
staging/<institution>/<source-id>/
├── classification.yaml
├── extraction.yaml
├── proposed-pages/
├── provenance.json
├── schema-gaps.yaml
└── validation-report.md
```

Staging output is not canonical until maintainers review it and move approved content into `knowledge/institutions/<institution>/`.
