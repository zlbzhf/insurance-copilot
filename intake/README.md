# Intake

Intake holds contribution packages that are not yet canonical knowledge.

Preferred package shape:

```text
intake/<institution>/<date-topic>/
├── intake.yaml
├── sources/
│   └── source-record.yaml
├── raw/
│   └── README.md or allowed source excerpts
├── contributor-notes.md
└── optional-local-draft.md
```

Rules:

- Intake may include contributor drafts, but they are hints only.
- Public boundary declarations are mandatory.
- Customer data and non-public institution materials are rejected.
- The gateway writes normalized output to `staging/`; maintainers decide what enters `knowledge/`.
