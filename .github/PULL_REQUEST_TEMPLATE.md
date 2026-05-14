## Summary

- 

## Layer Changed

- [ ] General Hermes skill/workflows
- [ ] Public institution knowledge pack
- [ ] Standards / schemas / prompts / ingestion gateway
- [ ] Agent workspace template
- [ ] Validation / CI
- [ ] Docs / governance

## Public/Private Boundary

- [ ] No customer data included
- [ ] No non-public institution material included in public paths
- [ ] Sources are public/shareable or link-only metadata
- [ ] Customer-facing language remains draft-only

## Standards / Gateway

- [ ] New source/page types are backed by real source evidence or schema-gap proposals
- [ ] Generated staging output was reviewed before moving content into `knowledge/`
- [ ] Standards changes update `standards/current.yaml`, `standards/changelog.md`, schemas, templates, prompts, and validators as needed

## Validation

Paste output:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
```
