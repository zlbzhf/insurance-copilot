# GitHub Knowledge Governance

This project uses GitHub as a public knowledge governance layer rather than a direct dump of agent-generated notes.

## Recommended GitHub Flow

1. Contributor opens an issue or PR with a public source package.
2. CI runs deterministic validators only.
3. Maintainer reviews public/private boundary.
4. Maintainer may run `scripts/ingest_gateway.py` locally or through a controlled workflow.
5. Gateway output lands in `staging/` or a follow-up PR.
6. Domain maintainer reviews content and source mapping.
7. Schema maintainer reviews any standard changes.
8. Approved content is moved into `knowledge/institutions/<institution>/`.

## Why Not Auto-Merge LLM Output?

- Local contributor models vary in quality.
- Fork PRs cannot safely access secrets by default.
- `pull_request_target` workflows can be dangerous when misused.
- Raw documents can contain prompt injection.
- Copyright and privacy boundaries need human review.
- LLMs may overstate product, claims, underwriting, or marketing facts.

## GitHub LLM Options

GitHub Actions can call LLMs through GitHub Models or external provider secrets, but the safe default is controlled invocation after a maintainer marks a contribution as approved for processing.

A future workflow can be added with:

```text
workflow_dispatch or label-triggered action
  -> read approved source package
  -> call LLM using prompts/
  -> write staging artifacts
  -> open PR
```

The default CI should remain deterministic and cheap.

## Ownership

Use CODEOWNERS or reviewer conventions when the project grows:

```text
knowledge/institutions/aia/        @aia-pack-maintainers
knowledge/institutions/ping-an/    @ping-an-pack-maintainers
standards/ schemas/ prompts/       @schema-maintainers
scripts/                           @tooling-maintainers
```

## Merge Rule

No generated content should be merged into `knowledge/` unless it is:

- public-source backed;
- schema conformant;
- validator clean;
- reviewed by a relevant maintainer;
- marked with appropriate confidence and verification requirements.
