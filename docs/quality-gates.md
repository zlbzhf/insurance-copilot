# Quality Gates

Use these gates to keep Insurance Copilot reliable across new sessions, context compression, and future contributors.

## Gate 1 — Hermes Skill Packaging

Required:

- `skills/insurance-copilot/SKILL.md` exists.
- `SKILL.md` starts with valid YAML frontmatter.
- Frontmatter has `name: insurance-copilot`.
- Description is present and no longer than 1024 characters.
- Supporting files stay under `references/`, `templates/`, `scripts/`, or `assets/` inside the skill directory.
- README documents local Hermes installation.

Reject changes that make Claude plugin metadata, `CLAUDE.md`, or `.mcp.json` the primary interface.

## Gate 2 — Insurance Safety

Required in the skill or references:

- Every output is a draft for licensed/compliance review.
- No final insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decision.
- No guaranteed approval, payout, returns, savings, or coverage outcomes.
- No advice to conceal, minimize, or omit required disclosures.
- Replacement, surrender, cancellation, or policy change requires documented suitability/replacement analysis and escalation.
- Source hierarchy and `[verify]` markers are used when source evidence is incomplete.

## Gate 3 — Workflow Usability

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
- renewal review;
- stakeholder summary.

## Gate 4 — Continuity

Required:

- `AGENTS.md` tells future Hermes sessions how to continue.
- `docs/continuity.md` exists and names authoritative files.
- `ROADMAP.md` captures durable project direction.
- `scripts/validate_repo.py` checks structural invariants.
- GitHub Actions runs the validator on push/PR.

## Gate 5 — Examples and Evaluation Fixtures

Required:

- examples use synthetic or non-sensitive data only;
- every sample customer/profile case has an expected-output sketch or eval case;
- high-risk eval cases cover unsafe guarantee language and replacement/surrender risk;
- examples do not include real customer PII.

## Required Validation Command

```bash
python3 scripts/validate_repo.py
```

A change is not ready to commit if this command fails.
