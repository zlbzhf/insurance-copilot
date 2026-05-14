# Quality Gates

Use these gates to keep Insurance Copilot reliable across new sessions, context compression, and future contributors.

## Gate 1 — Hermes Skill Packaging

Required:

- `skills/insurance-copilot/SKILL.md` exists.
- `SKILL.md` starts with valid YAML frontmatter.
- Frontmatter has `name: insurance-copilot`.
- Description is present and no longer than 1024 characters.
- Supporting files stay under `references/`, `templates/`, `scripts/`, or `assets/` inside the skill directory.
- README documents full-directory local Hermes installation.
- `scripts/package_skill.py --check` passes.

Reject changes that make Claude plugin metadata, `CLAUDE.md`, or `.mcp.json` the primary interface.

## Gate 2 — Insurance Safety

Required in the skill or references:

- Every output is a draft for licensed/compliance review.
- No final insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decision.
- No guaranteed approval, payout, returns, savings, or coverage outcomes.
- No advice to conceal, minimize, or omit required disclosures.
- Replacement, surrender, cancellation, or policy change requires documented suitability/replacement analysis and escalation.
- Claims triage does not determine claim coverage or payout.
- Annuity/investment-linked review separates guarantees from non-guaranteed projections.
- Source hierarchy and `[verify]` markers are used when source evidence is incomplete.

## Gate 3 — Privacy and Data Governance

Required:

- Examples and evals are synthetic or de-identified.
- Public institution packs contain only public/shareable knowledge.
- Non-public institution materials belong in the agent-private layer, not public pack paths.
- Agent workspace template contains no real customer data.
- No real customer PII, production policy documents, secrets, or credentials are committed.
- MCP connectors default to read-only, least-privilege access.
- Sensitive data is not persisted unless the user explicitly confirms destination and purpose.
- Production integration requires audit logging, retention/deletion rules, and compliance approval.

## Gate 4 — Public Institution Knowledge Packs

Required:

- `knowledge/registry.json` exists and identifies public packs.
- `knowledge/institutions/_template/` defines pack structure.
- Seed packs such as `knowledge/institutions/aia/` include `PACK.md`, `SCHEMA.md`, `index.md`, and `log.md`.
- Pack pages use frontmatter, public-source flags, confidence labels, and `[verify]` where appropriate.
- Pack validators reject obvious PII, missing source metadata, broken wikilinks, and private-data classifications.
- Source-first contribution workflow exists.

## Gate 5 — Agent Private Workspace Template

Required:

- `agent-workspace-template/` exists.
- Template includes `AGENT.md`, `SCHEMA.md`, `index.md`, `log.md`, and directory READMEs.
- Template states it is private and not for public upload.
- `.gitignore` excludes likely local private workspace paths.
- Validator can check template structure without requiring real private data.

## Gate 6 — Workflow Usability

Each core workflow reference should include:

- clear trigger / when to use;
- required inputs or source requirements;
- ordered review steps or analysis dimensions;
- output format;
- guardrails or escalation criteria.

Core workflows:

- cold-start interview;
- client needs intake;
- coverage gap analysis;
- product-fit review;
- objection response;
- compliance check;
- policy review;
- replacement/surrender suitability triage;
- claims triage;
- annuity/investment-linked caution review;
- renewal review;
- stakeholder summary.

## Gate 7 — Action Safety

Required:

- Draft-only default.
- No automatic customer sending.
- No application submission, claims filing, policy change, cancellation, surrender, replacement, or publication without explicit confirmation and required review.
- Side-effect confirmation must include exact target, final content/data, authority, and licensed/compliance review status.

## Gate 8 — Continuity

Required:

- `AGENTS.md` tells future Hermes sessions how to continue.
- `docs/continuity.md` exists and names authoritative files.
- `docs/architecture.md` defines the three-layer architecture.
- `ROADMAP.md` captures durable project direction.
- `scripts/validate_repo.py` checks structural invariants.
- GitHub Actions runs validator, package check, eval runner, knowledge-pack validator, and agent-workspace validator on push/PR.

## Gate 9 — Examples and Evaluation Fixtures

Required:

- examples use synthetic or non-sensitive data only;
- every sample customer/profile case has an expected-output sketch or eval case;
- high-risk eval cases cover unsafe guarantee language, source hallucination, replacement/surrender, claims guarantees, health disclosure coaching, vulnerable-customer pressure, annuity projections, renewal/lapse uncertainty, and unauthorized sending;
- `python3 scripts/run_evals.py` passes.

## Required Validation Commands

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
```

A change is not ready to commit if any command fails.
