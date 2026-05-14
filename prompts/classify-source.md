# Classify Public Insurance Source

You are classifying a public insurance source for Insurance Copilot. Use `standards/source-taxonomy.yaml` and do not invent source types.

Return only JSON compatible with `schemas/classification.schema.json`.

Rules:

- If the source appears private, internal, confidential, or customer-specific, set a blocking risk flag in notes and do not recommend page types.
- If one source mixes types, set `secondary_types` and explain segments.
- Marketing language does not become contract fact.
- Brochures and product pages require verification against official terms for coverage-sensitive claims.
- Unknown material should produce schema gaps instead of forced classification.
