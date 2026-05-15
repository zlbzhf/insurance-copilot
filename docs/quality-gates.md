# Quality Gates

Use these gates to keep Insurance Copilot reliable across new sessions, context compression, and future contributors.

## Agent-Friendly Onboarding Gate

The practice profile template is an internal storage format, not a user-facing form.

Required:

- Never ask the agent to manually fill the profile template.
- New Agent Default Mode exists for new, busy, or unsure agents who say `I don't know yet`.
- Onboarding asks no more than three questions before producing a provisional profile.
- Each onboarding question allows `I don't know yet` or conservative defaults.
- The profile is treated as dynamic and updateable through agent corrections, compliance feedback, and repeated scenarios.
- Agents provide messy real-world context; AI converts it into structured scenarios, profile updates, reusable examples, and eval intents.
- evals are internal quality fixtures; agents do not write JSON eval cases.

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
- Underwriting/disclosure support helps the customer present accurate, complete, and favorable-underwriting-relevant facts through approved forms and source documents, without concealment or misrepresentation.
- Claims support is customer-first: it develops the strongest good-faith claim-support position, claim advocacy memo, and client-interest action plan without promising payout or giving unauthorized legal advice.
- Do not use neutral caveats as a substitute for service; pair caveats with evidence requests, source checks, escalation owners, and customer-safe drafts.
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
- `standards/`, `schemas/`, and `prompts/` define the evidence-driven public knowledge standard.
- `knowledge/institutions/_template/` defines pack structure.
- Seed packs such as `knowledge/institutions/aia/` include `PACK.md`, `SCHEMA.md`, `index.md`, and `log.md`.
- Pack pages use frontmatter, public-source flags, confidence labels, schema versions, and `[verify]` where appropriate.
- Pack validators reject obvious PII, missing source metadata, broken wikilinks, unknown page/source types, and private-data classifications.
- Source-first contribution workflow exists.
- `scripts/ingest_gateway.py` can stage source classification/extraction without merging generated output into `knowledge/`.
- Schema gaps are recorded rather than forcing unmatched documents into generic templates.

## Gate 5 — Agent Private Workspace Template

Required:

- `agent-workspace-template/` exists.
- Template includes `AGENT.md`, `SCHEMA.md`, `index.md`, `log.md`, and directory READMEs.
- Template states it is private and not for public upload.
- `.gitignore` excludes likely local private workspace paths.
- Validator can check template structure without requiring real private data.
- Private workspace readiness gate exists before scheduled monitoring and checks structure, freshness, PII-like risks, output boundaries, and retention/audit readiness.

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
- GitHub Actions runs validator, package check, eval runner, knowledge-pack validator, agent-workspace validator, and gateway smoke check on push/PR.

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
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/private_workspace_readiness.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --format json
python3 scripts/private_dry_run.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --out /tmp/insurance-copilot-dry-run --force || test $? -eq 1
python3 scripts/ingest_gateway.py --help
```

A change is not ready to commit if any command fails.


## Practical Workflow Beta Gates

To avoid architecture-only drift, every major release must preserve first-day practitioner usability:

- README exposes practitioner workflows before standards/schema details.
- `docs/workflow-surface.md` maps each job-style workflow to required inputs, output, review owner, forbidden actions, and standard prompt.
- Practice profile gate prevents specific product-fit conclusions, replacement suggestions, reusable customer scripts, and external-action drafts when practice context is missing.
- Private workspace template includes CRM-lite areas for leads, opportunities, meetings, policies, renewals, claims, referrals, and tasks.
- Daily Agent Workbench and Client Plan Draft have references, templates, examples, and eval fixtures.
- Chinese talk tracks and referral asks include forbidden phrases, `[verify]` items, escalation triggers, and review gates.
- Synthetic end-to-end demos prove a realistic loop without real customer or insurer data.

These gates are intentionally closer to `claude-for-legal` usability discipline: task surface first, professional profile next, connectors/workspaces as support, review gates always.

- Private workspace readiness blocks symlinked required workspace paths, validates every renewal row freshness timestamp, rejects future dates, and prevents output hardlink aliases to workspace files.

- Private dry-run deployment blocks live scheduled watcher creation until manifest `ready_for_scheduled_watcher` is true; it records `live_cron_created: false`, artifact checksums, and No External Writes.
