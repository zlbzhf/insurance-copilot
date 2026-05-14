# Public Institution Knowledge Packs

Institution packs are public, collaboratively maintained LLM-wiki-style knowledge bases for insurers such as AIA/友邦、平安、太平洋, and others.

## Hard Boundary

`knowledge/institutions/*` is public knowledge only.

Do not add:

- customer data;
- private agent notes;
- unpublished internal training material;
- confidential SOPs;
- production CRM/policy/claims exports;
- full copyrighted documents unless redistribution is clearly allowed.

If a material is not public/shareable, keep it in an agent-private workspace, even if the material is about an institution.

## Contribution Model

Preferred flow:

1. Submit a public source record or source package.
2. Stage source classification and extraction through `scripts/ingest_gateway.py` when adding new public source material.
3. Review `staging/<institution>/<source-id>/classification.yaml`, `extraction.yaml`, `schema-gaps.yaml`, proposed pages, provenance, and validation report.
4. If the source does not fit the current standard, create a schema-gap/proposal instead of forcing it into a generic template.
5. Move reviewed and approved content into the institution pack.
6. Run validators.
7. Open a PR.
8. Institution maintainers and schema maintainers review before merge when applicable.

Curated pages are allowed only when they follow `SCHEMA.md`, cite public sources, mark confidence, and pass validation.
