# Release Checklist

Use this checklist before tagging or announcing a usable release.

## Validation

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
```

## Manual Review

- [ ] README install instructions tested from a clean clone.
- [ ] `/skill insurance-copilot` load path tested after full-directory install.
- [ ] All references and templates included in package.
- [ ] No real customer PII in examples or evals.
- [ ] Safety boundaries preserved in `SKILL.md`.
- [ ] High-risk workflows require escalation.
- [ ] CHANGELOG updated.

## Release Notes

Document:

- version;
- new workflows/templates;
- validation results;
- known limitations;
- production-data warning.
