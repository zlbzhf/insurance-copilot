## Summary

- 

## Layer Changed

- [ ] General Hermes skill/workflows
- [ ] Public institution knowledge pack
- [ ] Agent workspace template
- [ ] Validation / CI
- [ ] Docs / governance

## Public/Private Boundary

- [ ] No customer data included
- [ ] No non-public institution material included in public paths
- [ ] Sources are public/shareable or link-only metadata
- [ ] Customer-facing language remains draft-only

## Validation

Paste output:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
```
