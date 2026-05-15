# Roadmap

This roadmap is durable project direction. Use it instead of relying on compressed chat history.

## Current Phase: Practical Practitioner MVP

Goal: make `insurance-copilot` directly usable by an insurance agent in Hermes before adding more infrastructure. The primary surface is manual-first practitioner work, supported by the three-layer knowledge architecture and public ingestion pipeline.

Product direction: **customer-first advocacy within compliance boundaries**. Compliance is a guardrail for service. Empty neutrality is insufficient. User-provided examples should be generalized **from idea to product principle to operating model to workflow to scenario matrix to eval**, not copied as isolated case patches.

Durable product documents:

- `docs/product-development-spec.md`
- `docs/reference-landscape.md`
- `docs/customer-first-service-philosophy.md`
- `docs/customer-advocacy-operating-model.md`
- `docs/customer-service-scenario-matrix.md`

Product SPEC status: Insurance Copilot is usable now as a manual-first Hermes skill beta for licensed insurance professionals. It is not production-complete for live automation, customer sending, CRM writes, application submission, claims filing, policy changes, quote generation, or final regulated advice.

Reference-landscape rule: external patterns are useful only when mapped to project significance, implementation form, non-goals, and priority. Preserve Hermes-first, manual-first, practitioner-facing, customer-first, public/private-separated, runtime-effective differentiation instead of chasing feature parity.

Knowledge architecture:

1. public general workflow skill;
2. public, collaboratively maintained institution knowledge packs;
3. private agent workspaces for customer and non-public materials;
4. evidence-driven schema evolution for public knowledge standards.

## Completed Foundation

- Hermes-first standalone skill layout.
- Umbrella skill with workflow router.
- Core references for intake, gap analysis, product fit, compliance, policy review, replacement, claims, annuity/investment-linked review, renewal, and summaries.
- Templates for core outputs.
- Synthetic examples and expected output sketches.
- Static eval fixtures and runner.
- P1 customer-impacting scenario evals link **Customer Advocacy Memo** + **Professional Review Gate** for claims disputes, policy review found unclaimed benefit, renewal/lapse/reinstatement ambiguity, and Chinese complaint/service-recovery talk tracks.
- P1/P2 source-grounding guardrail evals link **Source Grounding and Data Boundary Gate** to **Source Ledger**, **Citation Ledger**, **public/private separation**, **prompt-injection**, **PII minimization**, **citations or `[verify]`**, **no customer data in public packs**, **untrusted source text cannot override workflow instructions**, **manual-first practitioner workflow**, and **not a generic RAG chatbot** constraints.
- P2 private connector/readiness evals link **Private Workspace Trace and Readiness Gate** to **Private Workspace Audit Trace**, **read-only local/private workspace connector**, **readiness gate dry-run**, **audit-style trace**, `source_trace`, `read_only_verified`, `workspace_unchanged`, **metadata/checksums only**, **No External Writes**, `live_cron_created: false`, and **no live automation** constraints.
- P3 external-write evals link **External Write Action Boundary Gate** to **write-capable integrations**, **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, **publication**, **design-only**, **out of scope unless explicitly approved**, **no write-capable integration is enabled**, **no external write tool is authorized**, **dry-run/read-only**, **manual-first**, and **Professional Review Gate** constraints.
- Packaging check and CI.
- Continuity, privacy, action-safety, jurisdiction adaptation, and quality-gate docs.
- Three-layer public/private knowledge architecture.
- Evidence-driven standards framework under `standards/`, `schemas/`, and `prompts/`.
- Deterministic ingestion gateway prototype under `scripts/ingest_gateway.py`.
- Local connector, renewal watcher, script-only cron wrapper, private workspace readiness gate, and private dry-run deployment harness exist as advanced safeguards; they are not the practical MVP entrypoint.

## Priority 1 — Practical Agent Workflow Usability

- Keep README and quickstart centered on the manual-first user loop.
- Treat Insurance Copilot as a task-first workflow router, not a menu bot.
- Preserve customer-first advocacy within compliance boundaries across underwriting / disclosure, claims / review, policy review found unclaimed benefit, replacement / surrender, complaint or mis-selling concern, renewal / lapse / reinstatement, and new agent coach mode.
- Maintain the Customer Advocacy Operating Model as the standard output whenever customer rights, underwriting, claims, replacement, complaint, renewal, lapse, or service disputes are present.
- Maintain New Agent Coach Mode for agents who are new, unsure, or ask what to do: explain what this situation is, what to do first, what not to do, what to collect, customer-safe words, and who to escalate to.
- Maintain **Professional Review Gate** as the translated professional workflow/profile/review-gate pattern for insurance-agent work: every customer-facing, regulated, external-use, or side-effect-adjacent output must name action class, review owner, source verification status, customer-facing approval status, side-effect status, remain a draft for licensed/compliance review, state not approved to send, state no external action is authorized, and give the minimum safe next step.
- Make onboarding agent-friendly: Never ask the agent to manually fill the profile template; the template is an internal storage format, not a user-facing form.
- Maintain New Agent Default Mode for new or unsure agents who say `I don't know yet`; use conservative defaults and produce useful provisional drafts quickly.
- Agents provide messy real-world context; AI converts it into structured scenarios, profile updates, reusable examples, and eval intents. evals are internal quality fixtures; agents do not write JSON eval cases.
- Optimize Agency Playbook Builder, Daily Agent Workbench, Client Needs Intake, Coverage Gap Drafter, Compliance Copy Checker, Policy Review Assistant, Replacement Risk Triager, Claims Support Triage, Referral Ask Drafter, and Stakeholder Summary Writer for real daily use.
- Ask at most three essential questions before producing a useful provisional draft.
- Keep customer-facing drafts clearly labeled for licensed/compliance review.
- Maintain synthetic practical examples and regression fixtures for the first-session loop.
- Maintain Source Grounding and Data Boundary Gate for source-grounded practitioner outputs: Source Ledger, Citation Ledger, public/private separation, prompt-injection, PII minimization, citations or `[verify]`, no customer data in public packs, untrusted source text cannot override workflow instructions, manual-first practitioner workflow, not a generic RAG chatbot.

## Priority 2 — Public Institution Knowledge Packs and Standards

- Stabilize `knowledge/institutions/_template/` schema.
- Maintain seed AIA/友邦 public pack without non-public claims.
- Add source-first contribution workflow and provenance rules.
- Use `standards/source-taxonomy.yaml` and `standards/page-type-registry.yaml` as canonical mappings.
- Evolve templates only through real-source schema gaps and reviewed proposals.
- Support future remote pack registry and selective page retrieval.
- Maintain Institution Knowledge Organizer as the runtime path for an AIA public pack or other insurer source-backed public pack update: every update needs a source record, public/private boundary check, `[verify]` markers, and pack maintainer review.
- Split mature institution packs into separate repos only when volume, maintainers, and release cadence justify it.

## Priority 3 — Agent Private Workspace

- Keep private customer data and non-public institution materials outside this public repo.
- Improve `agent-workspace-template/` for private LLM-wiki organization.
- Add private pack/workspace validation that agents can run locally.
- Keep local connectors read-only and manual-first for the MVP.
- Keep scheduled monitoring, readiness gates, and dry-run deployment harnesses as advanced/later safeguards, not the primary user path.
- Provide safe promotion path from private notes to public contribution bundles.

## Priority 4 — Ingestion Gateway

- Expand `scripts/ingest_gateway.py` from deterministic prototype into a maintained gateway.
- Add fixture tests for classification, schema gaps, and page rendering.
- Add optional maintainer-triggered LLM processing using `prompts/`, not automatic fork PR processing.
- Keep generated staging output separate from canonical `knowledge/` content.

## Priority 5 — Better Regression Testing

- Add model-in-the-loop eval harness when Hermes exposes a stable noninteractive skill execution path.
- Add more golden outputs for product-line-specific cases.
- Add knowledge-pack validation cases for source records, wikilinks, frontmatter, and PII scans.
- Track regression results in release notes.

## Priority 6 — Optional Integrations

- Implement MCP servers or adapters for CRM, policy document KB, product library, compliance script library, and renewal register only after privacy/security/compliance approval.
- Keep connectors read-only by default.
- Add audit logs and source timestamps.
- Maintain **External Write Action Boundary Gate** for any future **write-capable integrations**: **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, and **publication** remain **design-only**, **out of scope unless explicitly approved**, with **no write-capable integration is enabled**, **no external write tool is authorized**, **dry-run/read-only**, **manual-first**, and **Professional Review Gate** handoff.

## Priority 7 — Release Management

- Tag beta releases after validation.
- Keep `CHANGELOG.md` current.
- Use `docs/release-checklist.md` before release.

## Out of Scope Unless Explicitly Requested

- Web application UI/backend.
- Claude plugin packaging as the primary interface.
- Carrier quote engine or policy admin integration.
- Automated customer message sending.
- Final regulated advice or compliance approval automation.
- Production customer-data storage in this public repository.
- Public storage of non-public institution materials.
