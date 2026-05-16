# Changelog

[简体中文](CHANGELOG.zh-CN.md) · [README](README.md)

All notable changes to this project will be documented in this file.

This project is currently pre-1.0 and milestone-based. The changelog follows a human-readable structure inspired by [Keep a Changelog](https://keepachangelog.com/) and uses semantic-versioning-style milestones where useful.

## [Unreleased]

### Added

- Added Chinese Telegram onboarding docs/examples/eval coverage and validator checks for `/skill insurance_copilot`, institution/role confirmation, `[待核实]` explanation, and existing-profile summary behavior.
- Added `docs/product-development-spec.md` as the durable product-development source of truth and usable-state definition.
- Added `docs/reference-landscape.md` to map external/reference projects to project significance, implementation form, non-goals, and priority.
- Added the Professional Review Gate workflow reference, template, eval, example, and validator coverage so customer-facing, regulated, external-use, and side-effect-adjacent outputs classify action class, review owner, source verification status, customer-facing approval status, side-effect status, draft for licensed/compliance review, not approved to send, no external action is authorized, and minimum safe next step.
- Added Institution Knowledge Organizer runtime reference/template/eval/validator coverage plus an AIA public pack source-backed public pack update with source record, public/private boundary, `[verify]`, No customer data, not a final claims decision, and pack maintainer review markers.
- Added P1 customer-impacting scenario evals linking Customer Advocacy Memo and Professional Review Gate for claims disputes, policy review found unclaimed benefit, renewal/lapse/reinstatement ambiguity, and Chinese complaint/service-recovery talk tracks.
- Added Source Grounding and Data Boundary Gate runtime reference/template/evals/validator coverage for Source Ledger, Citation Ledger, public/private separation, prompt-injection, PII minimization, citations or `[verify]`, no customer data in public packs, untrusted source text cannot override workflow instructions, manual-first practitioner workflow, and not a generic RAG chatbot behavior.
- Added generic-first architecture safeguards: `tests/test_generic_first_architecture.py`, `evals/cases/institution-public-pack-source-backed-generic.json`, and `evals/expected/institution-public-pack-source-backed-generic.md`.
- Added registry-driven public knowledge pack validation through `scripts/validate_all_knowledge_packs.py` so CI validates all registered public institution packs rather than only the AIA seed pack.

### Changed

- Renamed the installable Hermes skill directory/frontmatter identity to underscore-safe `insurance_copilot` while preserving the public repo slug `insurance-copilot` and private workspace root `~/.insurance-copilot/agents/<agent-id>/`.
- Clarified that Insurance Copilot is usable now as a manual-first Hermes skill beta, but not production-complete for live automation, customer sending, CRM writes, application submission, claims filing, policy changes, quote generation, or final regulated advice.
- Generalized Institution Knowledge Organizer from an AIA-first workflow to a pack-agnostic public institution pack workflow under `knowledge/institutions/<pack_id>/`; AIA/友邦 remains the current seed example, not the generic runtime definition.
- Updated README, Chinese README, CI, contribution templates, intake templates, and private workspace defaults to use registry-driven validation and generic institution placeholders.

### Fixed

- Fixed stale hyphenated skill-install guidance that could cause Telegram command/menu drift; documented the Hermes internal hyphen-key versus Telegram underscore-command mapping and release cleanup steps.
- Fixed AIA-overfit wording and defaults that could make the generic product layer appear AIA-specific.
- Fixed validation coverage so generic Institution Knowledge Organizer behavior and AIA seed-pack behavior are checked separately.

### Security and Compliance

- Hardened public/private separation by preventing generic templates from defaulting to `institution: aia` or `default_institution_pack: aia`.
- Preserved AIA seed-pack source-backed claims checks while adding pack-agnostic safeguards for future public institution packs.

## [0.1.0] - 2026-05-15

### Added

- Added the Hermes-first `insurance_copilot` skill package for licensed insurance professionals.
- Added the umbrella skill at `skills/insurance_copilot/SKILL.md` with task-first routing, safety boundaries, privacy guidance, New Agent Default Mode, New Agent Coach Mode, customer-first advocacy, and draft-only action safety.
- Added workflow references for agency playbook setup, daily workbench, client needs intake, coverage-gap drafting, client plan drafting, product-fit review, compliance copy checking, existing policy review, replacement/surrender suitability triage, claims support triage, renewal/lapse follow-up, objection response, referral asks, Chinese talk tracks, annuity/investment-linked caution review, stakeholder summaries, and baseline compliance vocabulary.
- Added output templates for practice profiles, client intake, coverage-gap analysis, product-fit review, compliance checks, policy review, replacement/surrender triage, claims triage, renewal review, stakeholder summaries, objection responses, daily workbench output, client plan drafts, Chinese talk tracks, referral asks, and customer advocacy memos.
- Added practical MVP examples for first-session onboarding, agent-friendly New Agent Default Mode, and customer-first advocacy.
- Added static eval fixtures and expected outputs for practical workflow behavior, compliance boundaries, customer-safe drafting, and systemic customer-advocacy scenarios.
- Added deterministic quality gates through `scripts/validate_repo.py`, `scripts/package_skill.py --check`, `scripts/run_evals.py`, pytest coverage, and GitHub Actions validation.
- Added continuity and governance documents: `AGENTS.md`, `ROADMAP.md`, `docs/continuity.md`, `docs/quality-gates.md`, and `docs/release-checklist.md`.
- Added `docs/documentation-map.md` to classify user-facing docs, runtime skill files, workflow references, output templates, maintainer governance, executable gates, knowledge packs, and optional automation.
- Added the three-layer knowledge architecture: public general workflow skill, public institution knowledge packs, and agent private knowledge workspace template.
- Added public institution knowledge-pack infrastructure, including `knowledge/registry.json`, the public AIA/友邦 seed pack, the `_template` pack, source-record templates, contribution templates, validation hooks, and public knowledge governance docs.
- Added evidence-driven standards for public knowledge maintenance, including source taxonomy, page type registry, quality policy, schema evolution governance, machine-readable schemas, and prompt contracts.
- Added a deterministic ingestion gateway prototype that stages classification, extraction, schema gaps, proposed pages, provenance, and validation reports without auto-merging generated content.
- Added the agent private workspace template with workspace schema, index/log structure, sample folders, validation script, and privacy-oriented documentation.
- Added read-only local connector slices for daily workbench generation from local Markdown/CSV workspaces.
- Added local renewal watcher scripts, examples, and cron wrapper templates for future internal alerting workflows.
- Added private workspace readiness checks and a private dry-run deployment harness that remain read-only and perform No External Writes.
- Added bilingual project surface files: `README.md`, `README.zh-CN.md`, `CHANGELOG.md`, and `CHANGELOG.zh-CN.md`.

### Changed

- Repositioned the project from a Claude-style/plugin-inspired prototype into a Hermes-first standalone skill repository.
- Refocused the front-door user experience from schema, gateway, deployment, or automation concerns to practical insurance-agent workflows.
- Elevated **customer-first advocacy within compliance boundaries** as a core product principle.
- Strengthened the rule that empty neutrality is insufficient unless paired with evidence requests, source checks, next actions, customer-safe language, and escalation paths.
- Clarified that `docs/` is not the runtime source by itself; behavior-changing rules must be made runtime-effective through `SKILL.md`, references, templates, evals, tests, or validators.
- Clarified that templates and eval JSON are internal maintainer/runtime artifacts, not forms that agents must manually fill.
- Clarified the public/private data boundary: public insurer knowledge belongs in `knowledge/institutions/`, while customer data and non-public materials belong in private workspaces outside the public repo.
- Moved optional connector, watcher, cron, and private dry-run flows behind an Advanced / Later positioning so the manual-first MVP remains the default user path.

### Fixed

- Removed drift toward Claude plugin, slash-command plugin, web-app, or deployment-platform positioning as the primary product surface.
- Hardened validation against docs-only regressions, missing workflow references, missing templates, stale platform-specific language, missing safety phrases, and incomplete package bundles.
- Added regression coverage so practical onboarding, customer-first advocacy, New Agent Coach Mode, and runtime-effective documentation gates remain protected.

### Security and Compliance

- Added privacy and data minimization guidance for sensitive health, financial, claims, beneficiary, payment, contact, and identity data.
- Added action-safety guidance requiring customer-facing drafts, irreversible actions, submissions, policy changes, claims filing, cancellation, surrender, replacement, and binding representations to remain under licensed/compliance review.
- Added public/private knowledge separation to prevent customer data or non-public institution material from entering public repository paths.
- Added PII-like fixture scanning for committed examples, evals, public knowledge packs, and workspace templates.
- Added read-only / No External Writes constraints for local connector, renewal watcher, readiness, and dry-run harness flows.
- Added jurisdiction adaptation guidance requiring institution/practice-specific compliance/legal review before production use.
