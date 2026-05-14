# Contributing

Thank you for improving Insurance Copilot.

## Rules

- Keep the project Hermes-first.
- Preserve the three-layer architecture: public general skill, public institution packs, private agent workspaces.
- Public institution packs must contain public/shareable knowledge only.
- Non-public institution materials and all customer-level data belong in the agent-private layer, not public pack paths.
- Do not add web app scaffolding unless explicitly requested.
- Do not make Claude plugin metadata the primary interface.
- Do not commit real customer PII, production policy documents, secrets, or credentials.
- Keep every customer-facing output as draft language for licensed/compliance review.
- Add or update eval fixtures for high-risk behavior changes.
- Use evidence-driven schema evolution for public knowledge standards; do not add one-off templates without a real-source rationale.
- Local agent drafts are hints only until normalized through source records, gateway staging, validators, and human review.

## Validate

Before committing:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
```

## Pull Request Expectations

- Explain the workflow or safety behavior changed.
- List files changed.
- Include validation output.
- Note any privacy, compliance, or side-effect implications.
