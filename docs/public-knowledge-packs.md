# Public Institution Knowledge Packs

Public institution packs are collaborative knowledge bases for insurers such as AIA/友邦、平安、太平洋, and others.

## Boundary

Public packs may contain:

- public source metadata and links;
- public official product/service summaries;
- public claims/renewal/service process summaries;
- public regulator references;
- community-authored summaries with sources and confidence labels.

Public packs must not contain:

- customer data;
- private agent notes;
- non-public internal training material;
- confidential SOPs;
- private CRM/policy/claims exports;
- full copyrighted documents unless redistribution is allowed.

Non-public institution materials belong in the agent-private layer, not a separate private institution pack under the public repo.

## LLM Wiki Structure

Each pack should follow:

```text
PACK.md                 Manifest and scope
SCHEMA.md               Pack-local schema and links to canonical standards
index.md                Content catalog
log.md                  Append-only maintenance log
sources/                Public source records
raw/                    Optional allowed raw extracts
entities/               Institution/entity pages
products/               Product summaries
contracts/              Policy contract / terms summaries
marketing/              Marketing compliance reviews
underwriting/           Public underwriting/disclosure guidance
service-processes/      Claims, renewal, payment, lapse, reinstatement processes
regulatory/             Regulator guidance summaries
faqs/                   Public FAQ summaries
source-summaries/       Source summaries for third-party/community/unknown materials
concepts/               Concepts such as underwriting disclosure
comparisons/            Public sourced comparisons
queries/                Filed answers worth preserving
templates/              Pack-local source and page templates aligned with standards/
contributions/          Reviewable contribution bundles
```

## Source-First Maintenance

Preferred contribution flow:

1. Add a source record under `sources/` or contribution bundle under `contributions/`.
2. Generate proposed pages from the source using templates and schema.
3. Include provenance linking claims to sources.
4. Run validation.
5. Submit PR.
6. Maintainers review facts, sources, and public/private boundary.

Directly uploading locally curated wiki pages is allowed only when they pass schema, cite sources, and include confidence labels.

## Remote-First Use

The registry in `knowledge/registry.json` lets Hermes discover packs and indexes without cloning every institution pack locally. Future tooling can fetch only relevant pages from remote repositories.
