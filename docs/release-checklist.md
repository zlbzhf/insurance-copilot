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
- [ ] Stale installed runtime directory `~/.hermes/skills/insurance/insurance-copilot/` absent or deliberately archived before testing.
- [ ] `/skill insurance_copilot` load path tested after full-directory install.
- [ ] Telegram-safe `/insurance_copilot` direct command/menu name tested after `/reload-skills` or gateway restart. If needed, refresh the Bot API menu and verify the Bot API 100-command cap did not hide this skill from autocomplete.
- [ ] Confirm Hermes internal `/insurance-copilot` key still resolves from `/insurance_copilot`; do not rename repo/private slugs to underscores.
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
