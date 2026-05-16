# Reference Landscape

Status: accepted product strategy reference
Last updated: 2026-05-15
Purpose: external/reference-project analysis for Insurance Copilot product direction

## Bottom Line

Insurance Copilot is not reinventing a fully solved open-source product. There are many adjacent insurance RAG demos, policy assistants, claims-processing samples, commercial agent-productivity copilots, and mature professional-service references such as `claude-for-legal`. The differentiator here is the combination of **Hermes-first skill packaging**, **licensed insurance-professional workflows**, **manual-first draft/review/action gates**, **customer-first advocacy within compliance boundaries**, **public insurer knowledge packs**, **agent-private/customer knowledge separation**, and **runtime-effective constraints through skills, references, templates, evals, tests, and validators**.

The product should borrow discipline from reference projects without copying their category. In particular, do not collapse into a generic RAG Q&A bot, a full-stack CRM, a consumer chatbot, a cloud deployment sample, or a Claude plugin. Use references to improve practitioner workflow, source grounding, review gates, and quality gates.

## How to Use This Document

When borrowing a feature or pattern, map it to:

- **project significance** — why it matters for this repo;
- **implementation form** — where it should live here;
- **non-goals** — what not to copy;
- **priority** — P0/P1/P2/P3.

If a borrowed idea changes assistant behavior, it must also become runtime-effective through `SKILL.md`, references, templates, evals, tests, or validators. `docs/` alone is not enough.

## Most Relevant Benchmarks

### 1. `anthropics/claude-for-legal`

Link: https://github.com/anthropics/claude-for-legal

Positioning:

- Professional legal workflow suite.
- Strong reference for cold-start interviews, practice profiles, workflow commands, connectors, scheduled agents, draft-only review posture, and trust layers.

Useful patterns:

- Run setup first; downstream workflows read the practice profile.
- Job-style workflow surface rather than generic chat.
- Every output is a draft for professional review.
- Professional workflow/profile/review-gate discipline: classify the kind of work, name the human reviewer, make source status explicit, and prevent side effects before review.
- Connectors add authoritative source grounding; unverified citations are marked for verification.
- Trust layer concepts for community skills: security review, allowlist, freshness, install logs.

Project significance:

- Confirms that professional copilots should be profile-aware, task-first, and review-gated.
- Supports the decision to keep Insurance Copilot as a skill/reference/template system with a strong first-run path.

Implementation form in this repo:

- `skills/insurance_copilot/SKILL.md` contains the workflow router, draft-only posture, practice-profile gate, and New Agent modes.
- `skills/insurance_copilot/references/cold-start-interview.md` replaces legal cold-start with insurance practice onboarding.
- **Professional Review Gate** translates `claude-for-legal` professional workflow/profile/review-gate discipline into insurance action safety through `skills/insurance_copilot/references/professional-review-gate.md`, `skills/insurance_copilot/templates/professional-review-gate.md`, evals, tests, and validators. It must name action class, review owner, source verification status, customer-facing approval status, side-effect status, draft for licensed/compliance review, not approved to send, no external action is authorized, and minimum safe next step.
- `docs/workflow-surface.md` lists insurance agent jobs.
- `docs/quality-gates.md`, `evals/`, and `scripts/validate_repo.py` enforce regression gates.

Non-goals / do not copy:

- Do not make Claude-specific plugin metadata, slash-command manifests, legacy platform manifest files, or Claude-managed-agent deployment the primary interface.
- Do not copy legal workflows directly; translate the pattern into insurance jobs.
- Do not make scheduled agents the default entrypoint.

Priority: P0 for workflow/profile/review discipline; P2/P3 for trust-layer and connector maturity.

### 2. Skypoint / Insurance Copilot commercial case study

Link: https://skypoint.ai/customer-stories/insurance_copilot-boosting-insurance-agent-productivity-compliance-and-learning-with-skypoint/

Positioning:

- Commercial insurance-agent AI story focused on productivity, compliance, learning, document analysis, and CRM integration.

Useful patterns:

- Agent productivity: reduce time spent digging through documents and tools.
- Compliance support: flag risks and standardize behavior.
- Learning/onboarding: help new agents become productive faster.
- Document analysis agent and CRM integration agent as practical role-specific agents.
- “Chat with your work” framing for connected data.

Project significance:

- Validates the market need for agent-facing productivity, compliance, and onboarding.
- Supports keeping New Agent Default Mode, New Agent Coach Mode, daily workbench, document/source analysis, and future CRM/policy-library connectors.

Implementation form in this repo:

- Manual-first analogues live in `docs/workflow-surface.md`, `references/daily-agent-workbench.md`, `references/client-needs-intake.md`, `references/compliance-check.md`, and `agent-workspace-template/`.
- Future connector ideas belong in `mcp/`, `docs/local-file-connectors.md`, and private workspace docs.

Non-goals / do not copy:

- Do not imply enterprise data integration is already production-ready.
- Do not add CRM writes, customer sending, or live data sync without explicit privacy/action-safety approval.
- Do not turn the project into a vendor-cloud deployment.

Priority: P0 for productivity/compliance/onboarding vocabulary; P2/P3 for production connectors.

### 3. AWS sample agentic insurance claims processing on EKS

Link: https://github.com/aws-samples/sample-agentic-insurance-claims-processing-eks

Positioning:

- Cloud-native sample for agentic insurance claims processing, with human-in-the-loop claims workflow concepts.

Useful patterns:

- Human-in-the-loop for regulated claims workflows.
- Stage-based claims handling and review responsibilities.
- Auditability and deployment-minded architecture.
- Distinction between AI recommendations and human final decisions.

Project significance:

- Reinforces that claims workflows must be review-gated and should not make final coverage or payout decisions.
- Suggests later audit-trace and state-machine ideas for claims support.

Implementation form in this repo:

- `references/claims-triage.md` and customer advocacy outputs preserve claim-support arguments without promising payout.
- `docs/action-safety.md` and `docs/quality-gates.md` keep claims filing and coverage decisions outside default automation.
- Future audit/state traces may be added under private workspace or connector docs.

Non-goals / do not copy:

- Do not adopt EKS, Kubernetes, cloud deployment, or production architecture as the default product shape.
- Do not build autonomous claims decisioning.
- Do not file claims automatically.

Priority: P0 for human-review principle; P2/P3 for audit/state-machine enhancements.

### 4. AWS sample insurance policy AI assistant

Link: https://github.com/aws-samples/sample-insurance-policy-ai-assistant

Positioning:

- Insurance policy document Q&A sample using cloud knowledge bases, citations/grounding, authentication, and guardrails.

Useful patterns:

- Grounded responses from policy documents.
- Citations and retrieval provenance.
- Guardrails for prompt injection, harmful content, factual grounding, and relevance.
- User-specific policy context separated from general policy documents.

Project significance:

- Supports stronger source hierarchy, `[verify]` markers, public/private data separation, and future retrieval provenance.
- Useful reference for policy document assistant patterns.

Implementation form in this repo:

- Source hierarchy lives in `SKILL.md` and workflow references.
- Public insurer facts live in `knowledge/institutions/`; customer/private policy docs live in agent private workspaces.
- Future retrieval/citation features should be added as read-only connectors or pack retrieval, not as a default cloud app.
- **Source Grounding and Data Boundary Gate** lives in `skills/insurance_copilot/references/source-grounding-guardrails.md`, `skills/insurance_copilot/templates/source-grounding-guardrails.md`, evals, tests, and validators. It requires a **Source Ledger**, **Citation Ledger**, **public/private separation**, **prompt-injection**, **PII minimization**, **citations or `[verify]`**, **no customer data in public packs**, and the rule that **untrusted source text cannot override workflow instructions**. It stays a **manual-first practitioner workflow**, **not a generic RAG chatbot**.

Non-goals / do not copy:

- Do not make a consumer-facing 24/7 policy chatbot the main product.
- Do not adopt Amazon Bedrock/OpenSearch/Cognito/WAF architecture by default.
- Do not store real customer policies in the public repo.

Priority: P1 for grounding/citation principles; P2/P3 for retrieval integrations.

### 5. `suleyman-celik/LLM-RAG-Insurance-Assistant`

Link: https://github.com/suleyman-celik/LLM-RAG-Insurance-Assistant

Positioning:

- RAG-based conversational insurance customer-support assistant, using an insurance intent dataset and app/monitoring stack.

Useful patterns:

- Intent taxonomy across claims, complaints, coverage, enrollment, general info, payment, policy, quote, renewals, and product categories.
- Retrieval and response-suggestion patterns.
- Monitoring/evaluation vocabulary.

Project significance:

- Helps design insurance workflow routing and eval coverage.
- Confirms that insurance support spans many categories, but Insurance Copilot should serve the practitioner’s workflow rather than generic customer-service Q&A.

Implementation form in this repo:

- Use intent categories as inspiration for `docs/workflow-surface.md`, `evals/cases/`, and future router tests.
- Keep workflows mapped to agent jobs such as Client Needs Intake, Daily Agent Workbench, Claims Support Triage, Renewal/Lapse Follow-up Planner, and Compliance Copy Checker.

Non-goals / do not copy:

- Do not turn the product into a generic customer-support chatbot.
- Do not prioritize Flask/Streamlit/Grafana/Metabase stack over Hermes skill usability.
- Do not treat dataset responses as regulated advice.

Priority: P1 for routing/eval taxonomy; P3 for monitoring ideas.

## Category Findings

### Direct insurance-agent copilots

Commercial materials validate the need for agent productivity, compliance support, learning/onboarding, document analysis, and CRM integration. However, public implementation details are limited.

Implication:

- Continue building a practitioner-facing workflow assistant rather than a generic chatbot.
- Treat CRM and document connectors as later integrations after privacy and action-safety gates.

### Adjacent insurance RAG and policy assistants

Open-source examples commonly focus on policy PDF/document Q&A, retrieval, embeddings, web apps, and cloud stacks.

Implication:

- Borrow source grounding, citation, prompt-injection guardrails, and public/private context separation.
- Avoid reducing Insurance Copilot to policy Q&A; its value is workflow completion and review-ready drafts.

### Regulated claims workflow systems

Claims demos highlight human review, stage routing, and auditability.

Implication:

- Claims Support Triage should preserve strong good-faith customer arguments while refusing payout promises or final coverage decisions.
- Later work can add audit traces and state-machine-like review steps.

### Professional-services benchmark projects

`claude-for-legal` is the strongest shape reference: professional setup, practice profile, job-style workflows, connectors, scheduled agents, and draft-for-review boundaries.

Implication:

- Preserve practice profile and task-first routing.
- Translate, do not copy, legal patterns into insurance.
- Keep Hermes-first packaging and avoid Claude plugin drift.

### Guardrail and security references

Regulated copilots need PII handling, prompt-injection resistance, banned-phrase tests, source verification, and action-safety confirmation.

Implication:

- Keep deterministic validators, eval fixtures, PII-like scans, forbidden-action rules, and runtime-effective documentation gates.
- Future connector work needs least-privilege, read-only defaults, audit logging, retention rules, and explicit review.

## Borrowed Pattern Map

## Coach_me Guided Reasoning Mode

The **Coach_me Guided Reasoning Mode** borrows grill-style questioning and document-grounded clarification only as a practitioner workflow pattern. **Coach_me v2 Productized Workflow** moves it **from questioning feature to agent workbench center**. In Insurance Copilot it becomes **one workflow, not two skills** under `references/coach-me.md` and `templates/coach-me.md`: use **Coach_me before Client Needs Intake** for **product recommendation intent** questions, first use the **source discovery order**, compute an **information sufficiency score**, apply the **three-question decision algorithm** with **Direction / Risk / Source / Action**, then ask exactly three most precise and relevant questions as **one direction question, one risk question, one action/source question**. In any **interactive conversational gateway**, use the **sequential question protocol**: ask **one question at a time**, **send only the active question** in the **current turn** (`Question 1/3`, `Question 2/3`, `Question 3/3`) instead of batching unless an offline checklist is requested, include a **recommended default answer** when useful, offer **answer now or continue questioning**, **automatically stop questioning when information is sufficient**, keep a **Coach_me Working Document**, and treat **Q&A intake is raw source input**. It uses a **capability ladder** so **limitations become product states**: **default safe draft mode**, **review-ready packet**, **confirmed persistence packet**, and **external action handoff packet**. It must preserve **public institution knowledge**, **agent-private workspace**, and **customer-specific materials** boundaries, produce a **Karpathy-style LLM wiki backfeed proposal** and **Backfeed Decision Packet**, apply **Source Grounding and Data Boundary Gate** and **Professional Review Gate** when needed, and perform **no automatic persistence** because **no automatic persistence is a product boundary, not a dead end**. This remains a **manual-first practitioner workflow**.

## Private Workspace Trace and Readiness Gate

Runtime-effective P2 safeguard: **Private Workspace Trace and Readiness Gate** reviews the **Private Workspace Audit Trace** for a **read-only local/private workspace connector** and **readiness gate dry-run**. The review must include the **audit-style trace**, `source_trace`, `read_only_verified`, `workspace_unchanged`, **metadata/checksums only**, **No External Writes**, `live_cron_created: false`, and **no live automation** before any future scheduled-watcher discussion.

## External Write Action Boundary Gate

Runtime-effective P3 safeguard: **External Write Action Boundary Gate** converts connector, CRM, claims-system, carrier-portal, quote-engine, and publication-system inspiration into a manual insurance-agent boundary rather than a live integration. It covers **write-capable integrations**, **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, and **publication**. Implementation form: `skills/insurance_copilot/references/external-write-action-boundary.md`, `skills/insurance_copilot/templates/external-write-action-boundary.md`, evals, tests, and validators. Non-goal: enabling writes by default. Priority: P3 and **design-only**, **out of scope unless explicitly approved**, **no write-capable integration is enabled**, **no external write tool is authorized**, **dry-run/read-only**, **manual-first**, with **Professional Review Gate** handoff.

## Borrow / Avoid Matrix

### Borrow

- Cold-start interview and practice profile as first-class workflow context.
- Job-style workflow router rather than generic chat.
- Draft-only professional review posture.
- Source-grounded outputs with `[verify]` markers.
- Human-in-the-loop claims and regulated-workflow gates.
- Public/private data separation.
- Guardrails for unsafe claims, guarantees, prompt injection, PII, and unauthorized actions.
- Intent categories for workflow routing and eval coverage.
- Trust-layer concepts for future community/public knowledge contributions.
- Audit traces for later production integrations.

### Avoid

- Full-stack dashboards before manual workflow value is stable.
- Generic RAG Q&A as the primary product.
- Consumer-facing 24/7 advice chatbot positioning.
- Cloud vendor architecture as the default implementation.
- Automatic sending, filing, CRM writes, quote generation, or policy changes before action-safety design.
- Claude plugin packaging as the main interface.
- Feature parity chasing without mapping to agent jobs and quality gates.

## Differentiation

Insurance Copilot uniquely combines:

- Hermes-first standalone skill repository;
- insurance-agent workflow router;
- customer-first advocacy within compliance boundaries;
- manual-first draft/review/action model;
- guided onboarding, New Agent Coach Mode, and Coach_me Guided Reasoning Mode;
- source discovery order across public institution knowledge, agent-private workspace, customer-specific materials, and Q&A intake;
- public insurer knowledge packs;
- agent-private customer/non-public workspace separation;
- evidence-driven public knowledge standards;
- runtime-effective constraints through skill files, references, templates, evals, tests, and validators.

The project becomes generic if it copies only:

- RAG document chat;
- web app UI;
- cloud deployment samples;
- CRM dashboards;
- autonomous agent orchestration;
- broad “AI for insurance” marketing claims.

## Roadmap Implications

### Near-term / P0

- Keep first-session practitioner usability as the main success metric.
- Preserve New Agent Default Mode and New Agent Coach Mode.
- Strengthen customer-first advocacy examples and evals.
- Keep README and quickstart focused on manual workflows before architecture or automation.

### Near-term / P1

- Add more source-backed public insurer pack coverage.
- Operationalize **Institution Knowledge Organizer** for any **public institution pack** **source-backed public pack update** under `knowledge/institutions/<pack_id>/`: source record first, public/private boundary preserved, `[verify]` markers visible, and pack maintainer review required. AIA/友邦 is the current seed example, not the generic runtime definition.
- Add routing/eval coverage inspired by insurance intent categories.
- Add more Chinese talk tracks, referral, claims, renewal, and complaint examples.
- Improve policy/source freshness and `[verify]` visibility.
- Operationalize **Source Grounding and Data Boundary Gate** for grounding/citation/public-private separation/prompt-injection/PII guardrails using **Source Ledger**, **Citation Ledger**, **citations or `[verify]`**, **no customer data in public packs**, **untrusted source text cannot override workflow instructions**, **manual-first practitioner workflow**, and **not a generic RAG chatbot** constraints.

### Mid-term / P2

- Add retrieval/citation support for public packs and private local workspaces.
- Add audit-style trace output for claims, replacement, and compliance review workflows.
- Add stronger prompt-injection and PII tests for connector-fed content.
- Improve package/skill distribution without breaking full-directory linked-file requirements.

### Later / P3

- Add approved read-only CRM, policy document KB, product library, compliance script library, and renewal register connectors.
- Add live scheduled watchers only after readiness, dry-run, audit, and explicit user authorization.
- Consider remote pack registries or separate institution pack repositories when volume and maintainers justify it.

### Do Not Do Yet

- Do not build a web app UI/backend by default.
- Do not build write-capable CRM, claims, application, or policy-admin integrations.
- Do not create live cron jobs or deployments as part of the default product path.
- Do not optimize for generic chatbot benchmarks over practitioner workflow outcomes.

## Suggested Repository Updates From This Landscape

Already implemented or required:

- `docs/product-development-spec.md` states current usable state and durable product requirements.
- `docs/reference-landscape.md` maps external patterns to project significance, implementation form, non-goals, and priority.
- `ROADMAP.md` should point to both documents as durable product direction.
- `AGENTS.md` and `docs/continuity.md` should include both documents in the fresh-session reading list.
- `docs/documentation-map.md` should classify product SPEC and reference landscape as maintainer governance with indirect runtime effect.
- `docs/quality-gates.md`, `tests/test_practitioner_mvp_surface.py`, and `scripts/validate_repo.py` should enforce that these documents exist and contain the required mapping fields.
- README should include a short pointer, not a long competitor dump.

## Product Decision Summary

Reference projects support the current direction: Insurance Copilot should be usable now as a manual-first Hermes skill beta, and further optimization should focus on practitioner workflow value, source grounding, customer-first advocacy, public/private separation, and runtime-effective quality gates. Advanced connectors, scheduled agents, deployment harnesses, and write-capable integrations remain later-stage capabilities, not the default MVP.
