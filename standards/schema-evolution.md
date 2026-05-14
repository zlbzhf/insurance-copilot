# Schema Evolution Process

The public knowledge standard evolves from real sources, not from one-time speculation.

## Loop

```text
Observe -> Propose -> Validate -> Review -> Migrate -> Release
```

## 1. Observe

The ingestion gateway processes public sources and records places where the active standard is insufficient. These are written as schema gap records, not silently turned into new fields.

Examples:

- a source contains non-guaranteed projections but no field captures projection assumptions;
- a source mixes brochure language and contract clauses;
- a new public material format appears, such as a short video script or interactive calculator;
- a required section is repeatedly empty across real sources and should be made optional or redesigned.

## 2. Propose

A schema change starts as a proposal under `standards/proposals/` using `schemas/schema-gap.schema.json` or a more detailed proposal markdown file.

A proposal must include:

- triggering source IDs;
- current limitation;
- proposed change;
- examples from real public sources;
- migration impact;
- validator/template/prompt updates required;
- compatibility assessment.

## 3. Validate

Before merging a schema change, test it against:

- the triggering source;
- at least one existing source or page when available;
- validator behavior;
- generated template output.

## 4. Review

Schema proposals require human review. LLMs may draft proposals but must not auto-merge canonical schema changes.

Required reviewers:

- a schema maintainer for any change under `standards/`, `schemas/`, `prompts/`, or templates;
- an institution pack maintainer if the change affects an existing pack;
- a compliance-minded reviewer for source types involving claims, underwriting, replacement, marketing, guarantees, or regulatory material.

## 5. Migrate

Backward-compatible optional fields are preferred. Breaking changes require a migration note and should update existing pages or explicitly mark old pages as legacy.

## 6. Release

On release, update:

- `standards/current.yaml`;
- `standards/changelog.md`;
- affected schemas;
- prompts;
- validators;
- page/source templates;
- docs and examples.

Agents preparing new contribution bundles should sync the current standard before drafting.
