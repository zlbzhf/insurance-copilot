# Contributing

Thank you for improving Insurance Copilot.

## Rules

- Keep the project Hermes-first.
- Do not add web app scaffolding unless explicitly requested.
- Do not make Claude plugin metadata the primary interface.
- Do not commit real customer PII, production policy documents, secrets, or credentials.
- Keep every customer-facing output as draft language for licensed/compliance review.
- Add or update eval fixtures for high-risk behavior changes.

## Validate

Before committing:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
```

## Pull Request Expectations

- Explain the workflow or safety behavior changed.
- List files changed.
- Include validation output.
- Note any privacy, compliance, or side-effect implications.
