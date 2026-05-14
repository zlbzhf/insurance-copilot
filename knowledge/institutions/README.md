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

1. Submit a public source record under `sources/` or a contribution bundle under `contributions/`.
2. Generate or propose wiki pages using the pack schema.
3. Run validators.
4. Open a PR.
5. Institution maintainers review before merge.

Curated pages are allowed only when they follow `SCHEMA.md`, cite public sources, mark confidence, and pass validation.
