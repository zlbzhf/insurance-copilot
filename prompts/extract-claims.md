# Extract Canonical Claims

Extract claims into the canonical extraction record, not directly into wiki pages.

Return only JSON compatible with `schemas/extraction-record.schema.json`.

Rules:

- Every claim must have a source locator.
- Keep confidence low unless the source is authoritative and the claim is directly stated.
- Mark product availability, premiums, riders, underwriting, exclusions, claims status, legal/tax advice, and guarantees as requiring verification.
- Preserve uncertainty and do not upgrade marketing statements into guarantees.
- Record schema gaps when useful source structure cannot fit the current schema.
