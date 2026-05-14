# Standards

This directory defines the evidence-driven standard used to curate public insurance institution packs.

The standard is intentionally versioned and evolvable. It starts small, records schema gaps while processing real public sources, and changes only through reviewed proposals.

## Operating Principle

```text
Observe real sources -> Propose schema change -> Validate against examples -> Review -> Migrate -> Release
```

Do not let one contributor's local model output become the canonical standard. The public repository accepts source packages, runs a common gateway, emits structured extraction files, and only then renders wiki pages.

## Files

- `current.yaml` — current schema/template/prompt versions.
- `source-taxonomy.yaml` — controlled source types, trust hierarchy, and risk flags.
- `page-type-registry.yaml` — canonical page types, required sections, and allowed source mappings.
- `quality-policy.yaml` — quality gates for staging outputs and merge readiness.
- `schema-evolution.md` — governance process for changing the standard.
- `changelog.md` — released standard changes.
- `proposals/` — reviewed or proposed schema evolution records.
