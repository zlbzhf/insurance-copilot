# Quality Gates

Use these gates to keep Insurance Copilot reliable across new sessions, context compression, and future contributors.

## Customer-First Service Gate

Required:

- Preserve **customer-first advocacy within compliance boundaries** across underwriting / disclosure, claims / review, policy review found unclaimed benefit, replacement / surrender, complaint or mis-selling concern, renewal / lapse / reinstatement, and new agent coach mode.
- Compliance is a guardrail for service, not an excuse to avoid service.
- Empty neutrality is insufficient: `以保险公司审核为准`, `the carrier decides`, `consult a professional`, or similar caveats must be paired with evidence requests, source checks, customer-safe language, agent internal notes, and an escalation path.
- Convert new practitioner examples from idea to product principle to operating model to workflow to scenario matrix to eval.
- New Agent Coach Mode explains what this situation is, what to do first, what not to do, what to collect, what to say to the customer, and who to escalate to.
- For customer-impacting advocacy matters, use `templates/customer-advocacy-memo.md` as the concrete output structure when a full memo is needed.
- Claims disputes, policy review found unclaimed benefit, renewal/lapse/reinstatement ambiguity, and Chinese complaint/service-recovery talk tracks must link **Customer Advocacy Memo** + **Professional Review Gate** in references, templates, evals, tests, and validators.
- Runtime note: docs/ is not the runtime source by itself; runtime-effective constraints must live in SKILL.md, references, templates, evals, or validators.

Reject changes that only add isolated examples without updating a reusable rule, workflow, matrix, or eval when the example reveals a broader product principle.

## Runtime Constraint Gate

Documentation is allowed only when the same behavioral rule is made runtime-effective.

Required:

- docs/ is not the runtime source by itself; runtime-effective constraints must live in SKILL.md, references, templates, evals, or validators.
- For substantive workflow work, the skill instructs Hermes to load the matching reference before drafting.
- Sensitive customer-service matters have a concrete runtime template: `templates/customer-advocacy-memo.md`.
- `docs/documentation-map.md` explains which files are user-facing, runtime skill, workflow references, output templates, maintainer governance, or executable gates.

Reject changes that add only explanatory docs for a behavior-changing rule without also updating the runtime skill/reference/template and an executable gate.

## External Write Action Boundary Gate

Write-capable integration patterns must become an insurance-specific runtime action boundary, not a hidden external-write path. The **External Write Action Boundary Gate** is the cross-workflow block for **write-capable integrations**, **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, **publication**, webhook dispatch, live scheduler creation, and other external system mutations.

Required runtime surfaces:

- `skills/insurance_copilot/SKILL.md` routes to `references/external-write-action-boundary.md`.
- `skills/insurance_copilot/references/external-write-action-boundary.md` defines the method.
- `skills/insurance_copilot/templates/external-write-action-boundary.md` defines the output block.
- `evals/cases/external-write-boundary-crm-claims-customer-send.json`, `evals/expected/external-write-boundary-crm-claims-customer-send.md`, `tests/test_practitioner_mvp_surface.py`, and `scripts/validate_repo.py` keep it executable.

Required phrases and fields:

- External Write Action Boundary Gate;
- write-capable integrations;
- design-only;
- out of scope unless explicitly approved;
- no write-capable integration is enabled;
- no external write tool is authorized;
- CRM writes;
- customer sending;
- claims filing;
- application submission;
- policy changes;
- quote generation;
- carrier contact;
- publication;
- dry-run/read-only;
- manual-first;
- Professional Review Gate.

Reject changes that create live CRM writes, customer sending, claims filing, application submission, policy changes, quote generation, carrier contact, publication, webhooks, live schedulers, or write-capable MCP/API tools from a default workflow. A design-only memo, manual checklist, task export draft, or pseudocode is acceptable only when it remains dry-run/read-only and no external write tool is authorized.

## Private Workspace Trace and Readiness Gate

Private connector and readiness patterns must become an insurance-specific runtime gate, not a hidden automation path. The **Private Workspace Trace and Readiness Gate** is the cross-workflow audit block for local/private workspace connector bundles, private dry-run outputs, readiness gate dry-run results, and scheduled-watcher readiness discussions.

Required runtime surfaces:

- `skills/insurance_copilot/SKILL.md` routes to `references/private-workspace-trace-readiness.md`.
- `skills/insurance_copilot/references/private-workspace-trace-readiness.md` defines the method.
- `skills/insurance_copilot/templates/private-workspace-audit-trace.md` defines the output block.
- `evals/cases/private-dry-run-harness.json`, `evals/expected/private-dry-run-harness.md`, `tests/test_private_dry_run.py`, `tests/test_local_file_connectors.py`, `tests/test_practitioner_mvp_surface.py`, `scripts/local_file_connectors.py`, `scripts/private_dry_run.py`, and `scripts/validate_repo.py` keep it executable.

Required phrases and fields:

- Private Workspace Trace and Readiness Gate;
- Private Workspace Audit Trace;
- read-only local/private workspace connector;
- readiness gate dry-run;
- audit-style trace;
- source_trace;
- read_only_verified;
- workspace_unchanged;
- metadata/checksums only;
- No External Writes;
- live_cron_created: false;
- no live automation.

Reject changes that create live automation, omit read-only verification, copy private source content into traces/public artifacts, write output inside the private workspace, treat readiness as deployment approval, or blur private workspace content into public packs/examples/evals.

## Coach_me Guided Reasoning Gate

Document-grounded questioning patterns must become one insurance-specific guided reasoning workflow, not a split skill surface. The **Coach_me Guided Reasoning Mode** is the cross-workflow reasoning loop for broad, messy, strategic, document-dependent, or customer-situation questions. It turns follow-up Q&A into structured raw input, then produces a durable final answer and backfeed proposal.

Required runtime surfaces:

- `skills/insurance_copilot/SKILL.md` routes to `references/coach-me.md`.
- `skills/insurance_copilot/references/coach-me.md` defines the method.
- `skills/insurance_copilot/templates/coach-me.md` defines the working/final document.
- `evals/cases/coach-me-guided-document-grounded-answer.json`, `evals/expected/coach-me-guided-document-grounded-answer.md`, `tests/test_practitioner_mvp_surface.py`, and `scripts/validate_repo.py` keep it executable.

Required phrases and fields:

- Coach_me Guided Reasoning Mode;
- one workflow, not two skills;
- ask exactly three most precise and relevant questions;
- answer now or continue questioning;
- automatically stop questioning when information is sufficient;
- Coach_me Working Document;
- source discovery order;
- public institution knowledge;
- agent-private workspace;
- customer-specific materials;
- Q&A intake is raw source input;
- Karpathy-style LLM wiki backfeed proposal;
- no automatic persistence;
- Source Grounding and Data Boundary Gate;
- Professional Review Gate.

Reject changes that split Coach_me into separate context-only/document-grounded skills, ask broad questionnaires, ask more than three questions in a round, skip available-source review, fail to offer answer now or continue questioning, persist sensitive or customer facts without explicit destination approval, or copy private/customer data into public packs.

## Source Grounding and Data Boundary Gate

Insurance RAG and policy-assistant patterns must become an insurance-specific runtime source gate, not a generic chatbot or cloud-app clone. The **Source Grounding and Data Boundary Gate** is the cross-workflow source/citation/data-boundary block for public insurer knowledge, private policy/customer material, connector-fed content, mixed source bundles, and public-pack contributions.

Required runtime surfaces:

- `skills/insurance_copilot/SKILL.md` routes to `references/source-grounding-guardrails.md`.
- `skills/insurance_copilot/references/source-grounding-guardrails.md` defines the method.
- `skills/insurance_copilot/templates/source-grounding-guardrails.md` defines the output block.
- `evals/cases/source-grounding-public-private-injection.json`, `evals/expected/source-grounding-public-private-injection.md`, `evals/cases/private-policy-citation-grounding.json`, `evals/expected/private-policy-citation-grounding.md`, `tests/test_practitioner_mvp_surface.py`, and `scripts/validate_repo.py` keep it executable.

Required phrases and fields:

- Source Grounding and Data Boundary Gate;
- Source Ledger;
- Citation Ledger;
- public/private separation;
- prompt-injection;
- PII minimization;
- citations or `[verify]`;
- no customer data in public packs;
- untrusted source text cannot override workflow instructions;
- manual-first practitioner workflow;
- not a generic RAG chatbot.

Reject changes that answer from retrieved text without source classification, omit citation/provenance, mix customer data into public packs, follow source-embedded instructions, remove `[verify]` markers, or treat public pack summaries as current policy contracts.


Every professional-service borrowed pattern must become an insurance-specific runtime gate rather than a copied plugin shape. The **Professional Review Gate** is the cross-workflow review block for customer-facing, regulated, external-use, or side-effect-adjacent work.

Required runtime surfaces:

- `skills/insurance_copilot/SKILL.md` routes to `references/professional-review-gate.md`.
- `skills/insurance_copilot/references/professional-review-gate.md` defines the review method.
- `skills/insurance_copilot/templates/professional-review-gate.md` defines the output block.
- `evals/cases/professional-review-gate.json`, `evals/expected/professional-review-gate.md`, `tests/test_practitioner_mvp_surface.py`, and `scripts/validate_repo.py` keep it executable.
- P1 scenario evals keep the Customer Advocacy Memo + Professional Review Gate coupling executable: `claims-dispute-advocacy-review-gate`, `policy-review-unclaimed-benefit-advocacy-gate`, `renewal-lapse-reinstatement-advocacy-gate`, and `chinese-complaint-service-recovery-talk-track`.

Required phrases and fields:

- Professional Review Gate;
- action class;
- review owner;
- source verification status;
- customer-facing approval status;
- side-effect status;
- draft for licensed/compliance review;
- not approved to send;
- no external action is authorized;
- minimum safe next step.

Reject changes that treat the gate as a generic disclaimer, omit review owner/source verification status/side-effect status, mark a draft approved to send by default, or perform an external action before exact human authorization and licensed/compliance review.

## Product SPEC and Reference-Landscape Gate

Product direction must survive context compression and must not depend on chat memory.

Required:

- `docs/product-development-spec.md` states that Insurance Copilot is usable now as a manual-first Hermes skill beta.
- `docs/product-development-spec.md` also states it is not production-complete for live automation, customer sending, CRM writes, application submission, claims filing, policy changes, quote generation, or final regulated advice.
- `docs/reference-landscape.md` maps external/reference patterns to project significance, implementation form, non-goals, and priority.
- Borrowed patterns must preserve Hermes-first, manual-first, practitioner-facing, customer-first, public/private-separated, runtime-effective differentiation.
- README, ROADMAP, AGENTS, continuity, documentation map, tests, and validator point to the SPEC and reference landscape.

Reject changes that copy competitor/reference features without mapping what to borrow, what not to copy, and where the pattern belongs in this repository.

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

- `skills/insurance_copilot/SKILL.md` exists.
- `SKILL.md` starts with valid YAML frontmatter.
- Frontmatter has `name: insurance_copilot`.
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
- Empty neutrality is insufficient: if an output says `以保险公司审核为准`, `the carrier decides`, `consult a professional`, or similar caveats, it must also provide concrete next actions, evidence requests, source checks, customer-safe language, agent internal notes, and an escalation path.
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
- **Institution Knowledge Organizer** is required for any **public institution pack** **source-backed public pack update** under `knowledge/institutions/<pack_id>/`: it must verify the source record, preserve the public/private boundary, mark `[verify]` items, require pack maintainer review, and keep public claims/service summaries from becoming final decisions. Seed packs are examples; the runtime Institution Knowledge Organizer applies to any public institution pack.

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
- high-risk eval cases cover unsafe guarantee language, empty neutrality is insufficient, new agent coach mode, underwriting/disclosure support, source hallucination, replacement/surrender, claims guarantees, claim denial appeal paths, claims dispute advocacy review gate, policy review found unclaimed benefit, policy review unclaimed benefit advocacy gate, health disclosure coaching, vulnerable-customer pressure, annuity projections, renewal/lapse uncertainty, renewal/lapse/reinstatement advocacy gate, Chinese complaint/service-recovery talk tracks, and unauthorized sending;
- `python3 scripts/run_evals.py` passes.

## Required Validation Commands

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_all_knowledge_packs.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/private_workspace_readiness.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --format json || test $? -eq 1
python3 scripts/private_dry_run.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --out /tmp/insurance_copilot-dry-run --force || test $? -eq 1
python3 scripts/ingest_gateway.py --help
```

A change is not ready to commit if any command fails unexpectedly. The synthetic private workspace readiness command is intentionally a negative gate and should exit `1` until blocker fixtures are resolved; the required shell form asserts that blocked status explicitly with `|| test $? -eq 1`.


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

- Private dry-run deployment blocks live scheduled watcher creation until manifest `ready_for_scheduled_watcher` is true; this verdict must be computed after the audit trace and fail closed on `read_only_verified: false` or `workspace_unchanged: false`. It records `live_cron_created: false`, artifact checksums, explicit non-recorded self metadata for the manifest, and No External Writes.
