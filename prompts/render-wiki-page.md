# Render Wiki Page Candidate

Render a markdown wiki page only from validated source records, classifications, and canonical extraction records.

Rules:

- Use a page type from `standards/page-type-registry.yaml`.
- Include all required sections for the page type.
- Keep source status, confidence, `[verify]` markers, and customer-facing cautions visible.
- Do not add facts not present in extraction claims.
- Use `[[wikilinks]]` for related concepts and pages.
- Generated pages are candidates and require human review before becoming high confidence.
