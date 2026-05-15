# Institution Knowledge Organizer Template

Use with `templates/institution-knowledge-organizer.md` and source workflow reference `references/institution-knowledge-organizer.md` for an **AIA public pack** or other insurer **source-backed public pack update**.

## Institution Knowledge Organizer
- Pack:
- Institution / jurisdiction:
- Workflow: source-backed public pack update
- Source record:
- Source URL / retrieved date:
- Source type:
- Page type:
- Redistribution mode:
- Source-backed status:
- `[verify]` items:
- Public/private boundary: public sources only; no customer data, private agent notes, secrets, production exports, or non-public institution materials
- Pack maintainer review:

## Source Record Checklist
- [ ] `id` is stable, lowercase, and source-specific.
- [ ] `institution` matches the pack ID.
- [ ] `source_type` is allowed by `standards/source-taxonomy.yaml`.
- [ ] `retrieved_at` is present.
- [ ] `public_source: true` is present.
- [ ] `redistribution.mode` is link-only unless rights are explicit.
- [ ] No private or customer material is referenced.

## Proposed Public Pack Pages
- Target page path:
- Required sections from `standards/page-type-registry.yaml`:
- Claims copied from source:
- Claims summarized from source:
- Claims marked `[verify]`:
- Related wikilinks:
- Schema gap, if any:

## Maintainer Handoff
- Files changed:
- Validator commands to run:
- Known freshness risks:
- Public/private boundary checks:
- Pack maintainer review owner:

## Professional Review Gate
Use this if the update is used to support a customer-facing, regulated, or external-use draft.

- Workflow: Institution Knowledge Organizer
- Action class:
- Review owner: pack maintainer review plus licensed/compliance review if customer-facing
- Source verification status:
- Customer-facing approval status: draft for licensed/compliance review; not approved to send
- Side-effect status: no external action is authorized
- Minimum safe next step:

## Forbidden Output States
- Do not present a public pack page as a final claims decision, underwriting decision, product recommendation, or compliance approval.
- Do not include customer data or private institution material.
- Do not omit the source record.
- Do not omit `[verify]` markers for freshness, claim-type requirements, policy terms, or review status.
- Do not bypass pack maintainer review.
