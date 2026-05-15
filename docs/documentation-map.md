# Documentation Map

This map prevents documentation sprawl. It explains who each artifact is for, whether it is runtime-effective, and how a product principle becomes an actual constraint.

Important: not every document is end-user reading. Final insurance-agent users should not need to read the whole repository before getting value.

## Runtime Effectiveness Rule

A principle is **runtime-effective** only when it appears in at least one of these places:

1. `skills/insurance-copilot/SKILL.md` — loaded into Hermes as the canonical runtime skill.
2. `skills/insurance-copilot/references/*.md` — loaded for the matching workflow before drafting.
3. `skills/insurance-copilot/templates/*.md` — shapes generated output.
4. `evals/cases/*.json` and `evals/expected/*.md` — regression fixtures.
5. `scripts/validate_repo.py` or `tests/*.py` — executable gates that fail when the constraint disappears.

`docs/` is useful for product explanation and maintenance, but `docs/` is not the runtime source by itself.

## Artifact Classes

### User-facing

Primary reader: insurance agents, managers, and practical users.

Files:

- `README.md`
- `docs/quickstart.md`
- `docs/workflow-surface.md`
- `examples/practical-mvp/*.md`

Purpose:

- Explain how to start quickly.
- Show task-first prompts and realistic examples.
- Keep the first-use experience manual-first and low burden.

Runtime effect:

- Indirect unless content is also present in the runtime skill, references, templates, evals, or validators.

### Runtime skill

Primary reader: Hermes at use time.

Files:

- `skills/insurance-copilot/SKILL.md`

Purpose:

- Define the core behavior, boundaries, routing rules, and source hierarchy.
- Keep customer-first advocacy, New Agent Coach Mode, draft-only action safety, and privacy rules in the model context when the skill is loaded.

Runtime effect:

- Direct. This is the main installable instruction surface.

### Workflow references

Primary reader: Hermes when a specific workflow is active.

Files:

- `skills/insurance-copilot/references/*.md`

Purpose:

- Provide workflow-specific triggers, inputs, steps, output format, guardrails, and escalation criteria.
- Prevent the umbrella skill from becoming too large while keeping detailed playbooks available.

Runtime effect:

- Direct when loaded. For substantive workflow work, load the matching reference before drafting.

### Output templates

Primary reader: Hermes and maintainers.

Files:

- `skills/insurance-copilot/templates/*.md`

Purpose:

- Turn principles into concrete output structure.
- Keep internal notes, customer-safe language, verification markers, and escalation paths visible in generated drafts.

Runtime effect:

- Direct when used. Templates are stronger than explanatory docs because they shape the final answer.

### Maintainer governance

Primary reader: future Hermes sessions, maintainers, and contributors.

Files:

- `AGENTS.md`
- `docs/continuity.md`
- `docs/quality-gates.md`
- `ROADMAP.md`
- `docs/product-development-spec.md`
- `docs/reference-landscape.md`
- `docs/architecture.md`
- `docs/evidence-driven-standards.md`

Purpose:

- Preserve project direction after context compression or handoff.
- Define non-negotiables, validation commands, and architecture boundaries.
- Record product-development source of truth, usable-state definition, and reference-project borrow/avoid decisions.
- Explain why public knowledge, private workspace data, and runtime skill behavior are separate.

Runtime effect:

- Indirect for end-user skill behavior.
- Direct for repository-development sessions because Hermes reads project instructions and validators enforce these rules.

### Executable gates

Primary reader: CI, maintainers, and future agents.

Files:

- `scripts/validate_repo.py`
- `scripts/run_evals.py`
- `scripts/package_skill.py`
- `scripts/validate_knowledge_pack.py`
- `scripts/validate_agent_workspace.py`
- `tests/*.py`
- `.github/workflows/validate.yml`

Purpose:

- Convert product and safety rules into failing checks.
- Prevent regressions such as doc-only principles, missing references, missing templates, unsafe examples, or public/private data boundary drift.

Runtime effect:

- Indirect at use time but strong at development time. These are the hard gates that keep runtime artifacts aligned.

### Knowledge packs

Primary reader: Hermes and maintainers when public insurer knowledge is needed.

Files:

- `knowledge/institutions/*`
- `standards/*`
- `schemas/*`
- `prompts/*`

Purpose:

- Store public, source-backed insurer knowledge in an LLM-wiki format.
- Keep public institution material separate from agent-private and customer-private data.

Runtime effect:

- Direct only when the relevant pack is read for a task.

### Advanced / later automation

Primary reader: maintainers and advanced operators.

Files:

- `cron/*`
- `mcp/*`
- `docs/local-file-connectors.md`
- `docs/local-renewal-watcher.md`
- `docs/script-only-cron-wrapper.md`
- `docs/private-workspace-readiness.md`
- `docs/private-dry-run-harness.md`

Purpose:

- Document optional future connectors, watcher recipes, and dry-run gates.
- Keep automation out of the practical MVP unless explicitly requested.

Runtime effect:

- None by default. Automation must not be introduced into user workflows unless requested and action-safety gates are satisfied.

## Product Principle Conversion Path

When a new product lesson appears, do not leave it as prose only.

Use this path:

```text
idea -> product principle -> operating model -> runtime skill/reference -> template -> eval -> validator/test
```

Minimum rule:

- If a principle changes assistant behavior, add or update `SKILL.md`, the relevant reference, and at least one template/eval/validator check.
- If it is only explanation for maintainers, keep it in `docs/` and label the reader clearly.
- If a feature is borrowed from an external/reference project, document project significance, implementation form, non-goals, and priority in `docs/reference-landscape.md` before treating it as roadmap direction.

## Current P0 Runtime Constraints

These constraints must not be docs-only:

- customer-first advocacy within compliance boundaries;
- Empty neutrality is insufficient;
- New Agent Coach Mode;
- draft-only customer-facing language;
- `[verify]` markers for missing sources;
- private/customer data stays outside public repo paths;
- no customer sending, filing, submission, cancellation, surrender, replacement, or policy change without explicit confirmation and required review.
