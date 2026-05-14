# Privacy and Data Handling

Insurance workflows often involve sensitive personal, health, financial, beneficiary, payment, and claims data. This repository is designed to minimize unnecessary data handling.

## Principles

- Use the minimum necessary data for the task.
- Prefer synthetic, de-identified, or redacted examples.
- Do not commit real customer PII or production policy documents.
- Do not persist sensitive customer data unless the user explicitly requests it and confirms the destination.
- Keep customer-facing drafts separate from internal notes.
- Use `[verify]` markers instead of inventing missing facts.

## Sensitive Data Categories

Treat these as sensitive:

- names, addresses, phone numbers, emails;
- dates of birth and government IDs;
- health, medication, underwriting, occupation, travel, hobby, and lifestyle disclosures;
- income, debt, assets, payment, banking, tax, and beneficiary details;
- policy numbers, claim numbers, and carrier portal data;
- complaint, claims, lapse, cancellation, reinstatement, or vulnerability notes.

## Repository Rules

- `examples/` and `evals/` must contain synthetic or de-identified data only.
- `knowledge/institutions/` is public-source-only; do not add customer data or non-public institution materials.
- `agent-workspace-template/` is only a template; real private workspaces should live outside the public repo, for example under `~/.insurance-copilot/agents/<agent-id>/`.
- Non-public institution notes belong in the agent-private workspace, not in a public pack.
- No real customer documents should be committed.
- If a sample resembles a real customer, rewrite it as synthetic.
- Validation should fail if obvious PII test patterns are added to examples/evals/public packs.

## Tool and MCP Rules

Before connecting production systems:

- use read-only access by default;
- scope credentials to the minimum required data;
- log what source was accessed and why;
- define retention and deletion expectations;
- ensure compliance/legal approval;
- avoid exposing secrets in prompts, docs, examples, or logs.

## Output Rules

When summarizing real customer materials:

- avoid repeating unnecessary identifiers;
- quote only the minimum necessary source text;
- mark missing or uncertain facts as `[verify]`;
- do not store outputs to disk unless the user confirms the path and purpose.
