# Detect Schema Gaps

Compare a source classification and extraction record against the active standards.

Return JSON records compatible with `schemas/schema-gap.schema.json`.

A schema gap is warranted when:

- a real public source contains a recurring information type not represented by the current schema;
- a current required field is consistently irrelevant for a source type;
- a source contains multiple material types that existing mappings cannot represent;
- risk flags or provenance fields are insufficient for safe review.

Do not propose canonical schema changes for one-off wording preferences.
