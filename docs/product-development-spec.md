# Product Development SPEC

Status: accepted product-development source of truth
Last updated: 2026-05-15
Scope: `insurance_copilot` as a Hermes-first insurance-agent workflow assistant

## Executive Answer

The project is **usable now as a manual-first Hermes skill beta** for licensed insurance professionals. A practitioner can install the full skill directory, load `insurance_copilot`, and use it for practice-profile setup, daily workbench planning, client intake, policy/coverage review, customer-message drafting, compliance copy checking, replacement/lapse/claim triage, referral asks, Chinese talk tracks, and public institution knowledge organization.

It is **not production-complete** for live automation, customer sending, CRM writes, application submission, claims filing, policy changes, quote generation, or final regulated advice. Those remain out of scope unless explicitly approved with action-safety, privacy, audit, and licensed/compliance review gates.

This SPEC exists so future work does not drift into a generic chatbot, schema project, deployment platform, CRM, or competitor feature clone. The durable product path is:

```text
manual-first practitioner workflow -> source/private fact grounding -> review-ready draft -> licensed/compliance review -> optional read-only connector -> optional approved automation
```

## Product Thesis

Insurance Copilot helps licensed insurance professionals turn messy real-world work into structured, review-ready outputs while staying inside compliance boundaries.

Core thesis:

```text
customer-first advocacy within compliance boundaries
```

Compliance is a guardrail for service, not a substitute for service. The assistant should help the agent identify customer goals, favorable facts, missing evidence, review channels, source checks, next actions, customer-safe language, and escalation paths. Empty neutrality is insufficient.

The assistant is a **workflow router, not a menu bot**. When the agent states a job, route directly to the matching workflow, ask at most three essential missing questions, and produce a useful provisional draft with `[verify]` markers and review gates.

## Primary Users

### Licensed insurance agent

Needs practical help preparing for meetings, organizing client notes, reviewing policies, drafting safer customer messages, handling objections, supporting claims/reviews, and following up on renewals.

### New or unsure agent

Needs New Agent Default Mode and New Agent Coach Mode: explain what the situation is, what to do first, what not to do, what to collect, what can be said safely, and who to escalate to.

### Agency manager or trainer

Needs reusable playbooks, safer language patterns, scenario cards, coaching examples, and quality gates that reduce inconsistent service behavior.

### Public knowledge-pack maintainer

Needs an evidence-driven pipeline for public insurer/institution knowledge packs, source records, schemas, proposals, staging output, and validators.

### Explicit non-users

The product is not a direct-to-consumer insurance advice bot and not a substitute for licensed professional judgment, carrier confirmation, legal/tax/investment advice, underwriting decisions, claims decisions, or compliance approval.

## Product Shape

The product is a standalone Hermes skill repository, not a web application.

Primary runtime artifact:

```text
skills/insurance_copilot/SKILL.md
```

Runtime support files:

```text
skills/insurance_copilot/references/*.md
skills/insurance_copilot/templates/*.md
evals/cases/*.json
evals/expected/*.md
scripts/validate_repo.py
tests/*.py
```

Product-support artifacts:

```text
docs/product-development-spec.md
docs/reference-landscape.md
docs/workflow-surface.md
docs/documentation-map.md
docs/quality-gates.md
ROADMAP.md
AGENTS.md
```

## Three-Layer Product Architecture

### Layer 1 — Public general workflow skill

Path: `skills/insurance_copilot/`

Role:

- workflow routing;
- practice profile and New Agent Default Mode;
- daily workbench, intake, policy review, compliance copy, replacement, claims, renewal, referral, and Chinese talk-track workflows;
- source hierarchy and `[verify]` markers;
- draft-only customer-facing output;
- customer-first advocacy and action-safety rules.

### Layer 2 — Public institution knowledge packs

Path: `knowledge/institutions/`

Role:

- public-source-only insurer/institution knowledge;
- public source records and source-backed summaries;
- a generic public institution pack template plus the current AIA/友邦 seed example;
- evidence-driven standards via `standards/`, `schemas/`, `prompts/`, `intake/`, `staging/`, and `scripts/ingest_gateway.py`.

Public packs must never contain customer data, private agent notes, non-public institution documents, secrets, or production exports.

### Layer 3 — Agent private knowledge workspace

Path template: `agent-workspace-template/`
Suggested private location: `~/.insurance_copilot/agents/<agent-id>/`

Role:

- customer facts and notes;
- private agent knowledge;
- non-public institution materials lawfully held by the agent;
- renewal registers and follow-up trackers;
- local-only readiness checks.

The public repository contains the template and validators only. Real private workspaces stay outside this repo.

## Runtime-Effective Constraint Model

This SPEC is a product-development source of truth, but it is not enough by itself to change runtime behavior.

If a product rule changes assistant behavior, the change must be reflected in at least one runtime surface and one executable gate:

1. `skills/insurance_copilot/SKILL.md` for umbrella behavior.
2. `skills/insurance_copilot/references/*.md` for workflow behavior.
3. `skills/insurance_copilot/templates/*.md` for output shape.
4. `evals/cases/*.json` and `evals/expected/*.md` for behavior regression coverage.
5. `scripts/validate_repo.py` or `tests/*.py` for deterministic enforcement.

docs/ alone is not runtime-effective.

Current cross-workflow runtime gate: **Professional Review Gate**. It translates professional workflow/profile/review-gate discipline into the insurance-agent surface through `skills/insurance_copilot/SKILL.md`, `references/professional-review-gate.md`, `templates/professional-review-gate.md`, evals, tests, and validators. Any customer-facing, regulated, external-use, or side-effect-adjacent output must name action class, review owner, source verification status, customer-facing approval status, side-effect status, mark customer copy as draft for licensed/compliance review and not approved to send, state no external action is authorized by default, and end with the minimum safe next step.

Current source/citation/data-boundary runtime gate: **Source Grounding and Data Boundary Gate**. It translates insurance RAG/policy-assistant grounding into the manual-first insurance-agent surface through `skills/insurance_copilot/SKILL.md`, `references/source-grounding-guardrails.md`, `templates/source-grounding-guardrails.md`, evals, tests, and validators. It requires a **Source Ledger**, **Citation Ledger**, **public/private separation**, **prompt-injection**, **PII minimization**, **citations or `[verify]`**, **no customer data in public packs**, and the rule that **untrusted source text cannot override workflow instructions**. This remains a **manual-first practitioner workflow**, **not a generic RAG chatbot**.


## Private Workspace Trace and Readiness Gate

Runtime-effective P2 safeguard: **Private Workspace Trace and Readiness Gate** reviews the **Private Workspace Audit Trace** for a **read-only local/private workspace connector** and **readiness gate dry-run**. The review must include the **audit-style trace**, `source_trace`, `read_only_verified`, `workspace_unchanged`, **metadata/checksums only**, **No External Writes**, `live_cron_created: false`, and **no live automation** before any future scheduled-watcher discussion.

## External Write Action Boundary Gate

Runtime-effective P3 safeguard: **External Write Action Boundary Gate** reviews requests for **write-capable integrations** including **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, and **publication**. The default product state is **design-only**, **out of scope unless explicitly approved**, **no write-capable integration is enabled**, **no external write tool is authorized**, **dry-run/read-only**, **manual-first**, and closed with **Professional Review Gate** before any customer-facing, regulated, external-use, or side-effect-adjacent output.

## Current Usable State

The manual-first beta is considered usable when all of the following hold:

- full skill directory install is documented;
- `SKILL.md` routes tasks without dumping a full menu;
- practice profile can be created through guided onboarding, not manual template filling;
- New Agent Default Mode accepts `I don't know yet` and uses conservative defaults;
- New Agent Coach Mode explains first steps and forbidden moves;
- daily agent workflows have references and templates;
- customer-facing drafts are labeled for licensed/compliance review;
- Professional Review Gate is available for customer-facing, regulated, external-use, and side-effect-adjacent work, with action class, review owner, source verification status, customer-facing approval status, side-effect status, draft for licensed/compliance review, not approved to send, no external action is authorized, and minimum safe next step;
- customer-first advocacy is available for underwriting/disclosure, claims/review, policy review found unclaimed benefit, replacement/surrender, complaints, renewal/lapse/reinstatement, and new-agent coaching;
- public institution packs are separated from private customer/agent data;
- examples and evals use synthetic or de-identified data;
- validator, package check, eval runner, knowledge-pack validator, agent-workspace validator, and pytest suite pass.

## Priority Workflows

### P0 — First-session practitioner loop

Goal: an agent gets value in the first session.

Required flow:

```text
install -> load skill -> guided practice profile or New Agent Default Mode -> daily workbench / intake / customer draft -> review-ready output
```

Must preserve:

- ask at most three essential questions before a provisional draft;
- never ask the agent to manually fill the profile template;
- route directly when a task is stated;
- mark missing facts `[verify]`;
- keep customer-facing language draft-only.

### P0 — Customer-first advocacy loop

Goal: prevent empty neutrality from replacing service.

Required flow:

```text
customer-impacting issue -> facts/timeline -> customer goal -> favorable facts -> risks -> evidence checklist -> good-faith arguments -> compliance boundary -> escalation -> customer-safe draft
```

Applies to underwriting/disclosure, claims/review, service disputes, policy review, replacement/surrender, complaints, renewal/lapse/reinstatement, and vulnerable customer issues.

### P1 — Public institution knowledge loop

Goal: make public insurer knowledge source-backed and maintainable.

Required flow:

```text
public source -> intake/source record -> deterministic gateway staging -> schema gap or proposed page -> validator -> human review -> public pack
```

No non-public institution materials or customer data may enter public packs.

Runtime slice: **Institution Knowledge Organizer** is the manual-first workflow for any **public institution pack** **source-backed public pack update** under `knowledge/institutions/<pack_id>/`. It must create or verify a source record, preserve the public/private boundary, mark `[verify]` items, and require pack maintainer review before canonical pack use. Seed packs are examples; the runtime Institution Knowledge Organizer applies to any public institution pack. AIA/友邦 is the current seed example, not the generic runtime definition.

### P1 — Private workspace loop

Goal: let agents ground work in private local facts without polluting public repo paths.

Required flow:

```text
agent-private workspace -> read-only local connector -> daily workbench bundle -> internal draft/review output -> optional readiness/dry-run gate
```

This remains manual-first and read-only until production integrations are explicitly approved.

## Reference-Landscape Requirement

Future product direction must be grounded in `docs/reference-landscape.md` when borrowing from external/reference projects.

Every borrowed pattern must be mapped to:

- project significance;
- implementation form in this repository;
- non-goals / what not to copy;
- priority.

Do not chase feature parity. Borrow patterns only when they strengthen the Hermes-first, manual-first, practitioner-facing, customer-first, public/private-separated, runtime-effective product shape.

## Source and Evidence Rules

Insurance outputs should distinguish:

- known customer facts;
- agent assumptions;
- public institution pack summaries;
- current policy/carrier/product/claim sources;
- missing facts requiring `[verify]`;
- licensed/compliance escalation items.

When sources conflict, prefer:

1. law/regulation/compliance red lines and action-safety constraints;
2. current authoritative customer/policy/carrier facts;
3. current official institution source;
4. public institution pack summary;
5. agent-private notes;
6. general workflow template.

If uncertainty remains, mark `[verify]` and escalate.

For source-grounded workflows, use **Source Grounding and Data Boundary Gate** before drafting. The output should include a **Source Ledger** and **Citation Ledger**, maintain **public/private separation**, handle **prompt-injection**, apply **PII minimization**, use **citations or `[verify]`**, state **no customer data in public packs** for public-pack work, and state that **untrusted source text cannot override workflow instructions**. This is a **manual-first practitioner workflow**, **not a generic RAG chatbot**.

## Safety and Compliance Contract

The assistant must not:

- guarantee approval, payout, return, savings, suitability, or coverage outcomes;
- provide final legal, tax, investment, underwriting, claims, actuarial, insurance, or compliance decisions;
- help conceal, minimize, omit, fabricate, or reframe material facts;
- imply marketing materials override policy contracts, riders, exclusions, underwriting rules, claims guides, regulator guidance, or approved compliance scripts;
- send customer messages, submit applications, file claims, change policies, cancel, surrender, replace, reinstate, or publish anything unless explicitly requested and action-safety gates are satisfied.

The assistant should:

- produce drafts for licensed/compliance review;
- separate customer-safe language from internal agent notes;
- include escalation triggers;
- preserve good-faith customer arguments where lawful and source-supported;
- refuse misrepresentation while still giving practical next steps.

## Product UX Rules

- Start with the user's job, not the repository structure.
- Avoid long workflow catalogs unless the user asks for a menu.
- Ask no more than three essential missing questions before a provisional draft.
- Allow `I don't know yet` and apply conservative defaults when appropriate.
- Use plain-language New Agent Coach Mode for unsure users.
- Put advanced connectors, cron, dry-run deployment, and CI behind Advanced / Later unless the user asks.
- Prefer useful drafts with `[verify]` markers over blocking on perfect data.
- Use Chinese talk tracks when the agent needs localized customer language, but keep compliance meaning intact.

## Roadmap Guardrails

### Near-term / P0

- Preserve and polish first-session usability.
- Expand synthetic practical examples and expected outputs.
- Strengthen customer-first advocacy evals across more real-world scenario families.
- Keep README and quickstart practitioner-first.

### Near-term / P1

- Improve AIA/友邦 public pack coverage from public sources only.
- Improve source-record and gateway staging workflows based on real public documents.
- Add more workflow-specific examples for Chinese talk tracks, referrals, renewals, claims, and policy review.
- Improve private workspace guidance while keeping real private data outside the public repo.

### Mid-term / P2

- Add richer source retrieval and citation support once the public/private boundary is stable.
- Add model-in-the-loop evals when Hermes exposes a stable noninteractive skill execution path.
- Add audit-style traces for regulated workflows and optional local connectors.
- Add production integration designs only after privacy, action-safety, and licensed/compliance review requirements are explicit.

### Later / P3

- Remote pack registry and selective page retrieval.
- Separate mature institution packs into their own repos when volume, ownership, and release cadence justify it.
- Approved CRM/policy-document/product-library/compliance-script connectors.
- Live scheduled watchers only after readiness, dry-run, audit, and explicit user authorization.

## Non-Goals Unless Explicitly Requested

- Web app UI/backend.
- Consumer-facing insurance advice chatbot.
- Quote engine, underwriting engine, or policy administration system.
- Automatic customer sending.
- Application submission, claims filing, policy change, cancellation, surrender, replacement, or reinstatement automation.
- Final regulated advice or compliance approval automation.
- Storage of real customer data in this public repository.
- Public storage of non-public institution materials.
- Vendor-specific cloud architecture as the default product shape.

## Definition of Done for Product Changes

A product change is not done unless it answers:

1. Which user/job does this improve?
2. Is this product-facing, runtime behavior, knowledge architecture, private workspace support, or advanced automation?
3. Does it preserve manual-first practitioner usability?
4. Does it preserve customer-first advocacy within compliance boundaries?
5. Does it keep public and private data separated?
6. If borrowed from another project, does `docs/reference-landscape.md` map project significance, implementation form, non-goals, and priority?
7. If it changes assistant behavior, which runtime surface was updated?
8. Which eval, test, or validator prevents regression?
9. Which README/quickstart/roadmap/doc map needs a pointer?
10. Which validation commands were run?

## Current Optimization Backlog

The assistant is usable, but further optimization should focus on:

- more public-source-backed insurer knowledge pages;
- richer product/source freshness markers;
- more Chinese customer-safe talk tracks;
- stronger New Agent Coach Mode scenario coverage;
- more customer-first advocacy evals for appeals, complaints, lapse/reinstatement, vulnerable customers, and replacement pressure;
- better private workspace examples without real PII;
- audit traces and retrieval provenance for future production workflows;
- careful connector design before any write-capable integration.

Do not optimize by adding automation first. Optimize by making the manual practitioner loop more useful, safer, and better grounded.
