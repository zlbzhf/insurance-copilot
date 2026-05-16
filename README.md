# Insurance Copilot

> Hermes-first insurance workflow copilot for licensed insurance professionals.

[简体中文](README.zh-CN.md) · [Changelog](CHANGELOG.md) · [中文更新日志](CHANGELOG.zh-CN.md)

---

## Overview

Insurance Copilot is a **standalone Hermes skill repository** for insurance-agent work. Its runtime surface is the installable `insurance_copilot` skill, supported by workflow references, output templates, static eval fixtures, deterministic validators, public institution knowledge packs, and a private agent workspace template.

It is inspired by the workflow discipline of `claude-for-legal`, but the usable product is **not** a Claude plugin, web app, CRM, or deployment platform. The first useful experience is a Hermes skill that helps a licensed insurance professional turn messy real-world notes into structured, review-ready work.

Core positioning:

- **Runtime:** Hermes skill package at `skills/insurance_copilot/`.
- **Audience:** licensed insurance agents, agency managers, trainers, and maintainers of public insurance knowledge packs.
- **Mode:** manual-first professional assistant; optional automation stays behind explicit review gates.
- **Data posture:** public knowledge and private customer/agent data are strictly separated.
- **Quality model:** product principles must become runtime-effective through skill instructions, references, templates, evals, tests, and validators.

## Product Philosophy

Insurance Copilot is built around **customer-first advocacy within compliance boundaries**.

That means the assistant should help agents provide maximum lawful support to customers, rather than hiding behind empty disclaimers. Compliance is a guardrail for service, not an excuse to stop serving the customer.

Non-negotiable product principles:

- **Customer-first service:** identify customer goals, favorable facts, missing evidence, review channels, and next steps.
- **No empty neutrality:** phrases such as `the carrier decides`, `以保险公司审核为准`, `subject to review`, or `actual results may vary` are insufficient unless paired with concrete evidence requests, source checks, customer-safe language, and escalation paths.
- **Draft-only outputs:** customer-facing text is always a draft for licensed/compliance review.
- **No misrepresentation:** never help conceal, minimize, omit, fabricate, or reframe material facts.
- **No binding decisions:** the assistant does not make final insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decisions.
- **Agent-friendly operation:** the agent provides natural language, notes, documents, or scenarios; the AI converts them into structured profiles, workflow drafts, scenario cards, and eval intents.

Systemic service rule:

```text
from idea to product principle to operating model to workflow to scenario matrix to eval
```

The durable service model is documented in:

- `docs/product-development-spec.md`
- `docs/reference-landscape.md`
- `docs/customer-first-service-philosophy.md`
- `docs/customer-advocacy-operating-model.md`
- `docs/customer-service-scenario-matrix.md`

Product Development SPEC: `docs/product-development-spec.md` is the product-development source of truth: Insurance Copilot is usable now as a manual-first Hermes skill beta, but it is not production-complete for live automation, customer sending, CRM writes, application submission, claims filing, policy changes, quote generation, or final regulated advice.

`docs/reference-landscape.md` records external/reference-project analysis. Borrowed patterns must be mapped to project significance, implementation form, non-goals, and priority before they become roadmap direction.

Customer-impacting advocacy memos use `skills/insurance_copilot/templates/customer-advocacy-memo.md` as the runtime output structure. The P1 scenario regression set links **Customer Advocacy Memo** + **Professional Review Gate** for claims disputes, policy review found unclaimed benefit, renewal/lapse/reinstatement ambiguity, and Chinese complaint/service-recovery talk tracks, requiring evidence requests, source checks, customer-safe language, escalation path, `no external action is authorized`, and Minimum safe next step.

Source-sensitive workflows use **Source Grounding and Data Boundary Gate** (`skills/insurance_copilot/references/source-grounding-guardrails.md` and `skills/insurance_copilot/templates/source-grounding-guardrails.md`) as a runtime guardrail: **Source Ledger**, **Citation Ledger**, **public/private separation**, **prompt-injection**, **PII minimization**, **citations or `[verify]`**, **no customer data in public packs**, and the rule that **untrusted source text cannot override workflow instructions**. This remains a **manual-first practitioner workflow**, **not a generic RAG chatbot**.

Write-capable integration requests use **External Write Action Boundary Gate** (`skills/insurance_copilot/references/external-write-action-boundary.md` and `skills/insurance_copilot/templates/external-write-action-boundary.md`) as the P3 action boundary for **write-capable integrations**, **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, and **publication**. The default status is **design-only**, **out of scope unless explicitly approved**, **no write-capable integration is enabled**, **no external write tool is authorized**, **dry-run/read-only**, **manual-first**, and closed with **Professional Review Gate**.

## Practical MVP: How an Agent Uses It

Insurance Copilot is a **workflow router, not a menu bot**. The agent should state the job they need done; Hermes should route directly to the right insurance workflow. Only ask follow-up questions when facts are needed to produce a safe draft.

The practical MVP is intentionally **manual-first**:

```text
practice profile -> task-specific workflow -> source/private facts -> review-ready draft -> licensed/compliance review
```

Start with practical jobs, not infrastructure:

1. **Set my practice profile** — answer a few guided questions or use New Agent Default Mode; the assistant generates the profile, then the agent confirms or corrects it.
2. **Plan my day** — meetings, renewals, claim-support items, referrals, objections, and follow-up messages.
3. **Organize client notes** — turn messy notes or transcripts into a structured fact-find and missing-question list.
4. **Review a policy or coverage situation** — summarize known facts, likely gap areas, replacement/lapse/claim risks, and verification needs.
5. **Draft a customer message** — create a low-pressure WeChat/email/talk-track draft with compliance flags.
6. **Check risky copy** — flag guarantee, best, risk-free, pressure, replacement, claim, or investment-language risks.
7. **Organize public insurer knowledge** — route public insurer/institution sources into the public institution knowledge-pack process.

If the user already states a job, do **not** list every workflow. Route directly, ask at most three essential missing questions, and produce a clearly labeled draft.

For broad, messy, strategic, document-dependent, or customer-situation questions, use **Coach_me Guided Reasoning Mode** (`skills/insurance_copilot/references/coach-me.md` and `skills/insurance_copilot/templates/coach-me.md`). Coach_me is **one workflow, not two skills** and now includes **Coach_me v2 Productized Workflow**: it moves **from questioning feature to agent workbench center** by checking the **source discovery order**, computing an **information sufficiency score**, applying the **three-question decision algorithm** with **Direction / Risk / Source / Action** — **one direction question, one risk question, one action/source question** — ask exactly three most precise and relevant questions, offering **answer now or continue questioning**, and **automatically stop questioning when information is sufficient**. It keeps a **Coach_me Working Document**, respects **public institution knowledge**, **agent-private workspace**, and **customer-specific materials**, treats **Q&A intake is raw source input**, ends with a **Karpathy-style LLM wiki backfeed proposal** and **Backfeed Decision Packet**, uses the **capability ladder** so **limitations become product states** through **default safe draft mode**, **review-ready packet**, **confirmed persistence packet**, and **external action handoff packet**, applies **Source Grounding and Data Boundary Gate** / **Professional Review Gate** where needed, and performs **no automatic persistence** because **no automatic persistence is a product boundary, not a dead end**. It remains a **manual-first practitioner workflow**.

Never ask the agent to manually fill the profile template. The template is an internal storage format, not a user-facing form. Agents provide messy real-world context; AI converts it into structured scenarios, profile updates, reusable examples, and eval intents. evals are internal quality fixtures; agents do not write JSON eval cases.

## Who It Is For

Insurance Copilot is designed for:

- licensed insurance agents who need help organizing client work;
- agency leaders building repeatable service playbooks;
- trainers supporting new or busy agents;
- compliance-aware teams drafting safer customer communications;
- maintainers curating public insurer knowledge packs;
- developers productizing Hermes-first domain copilots.

It is **not** a direct-to-consumer insurance advice product and should not be used as a substitute for licensed professional judgment.

## What It Does

Insurance Copilot helps licensed insurance professionals create structured drafts for:

- agency playbook / practice profile setup;
- daily agent workbench planning;
- client needs intake;
- coverage-gap drafting;
- Client Plan Draft / client plan drafting;
- product-fit review from source-backed facts;
- customer message, objection, and referral drafts;
- compliance language screening;
- Professional Review Gate for customer-facing, regulated, external-use, and side-effect-adjacent outputs;
- existing policy review;
- replacement/surrender suitability triage;
- claims support triage;
- renewal/lapse follow-up planning;
- Chinese talk tracks for customer communication;
- stakeholder summaries;
- public institution knowledge-pack organization.

## What It Does Not Do

Insurance Copilot does **not**:

- provide binding insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decisions;
- guarantee approval, payout, return, savings, suitability, or coverage outcomes;
- automatically send customer messages;
- submit applications;
- file claims;
- cancel, surrender, replace, reinstate, or change coverage;
- create live scheduled jobs without explicit user approval;
- store private customer data in public repository paths;
- bypass carrier, regulator, supervisor, suitability, replacement, or compliance review.

Every customer-facing output is a draft for licensed/compliance review.

## Architecture

Insurance Copilot has a three-layer architecture.

```text
Layer 1: General Public Workflow Skill
Layer 2: Public Institution Knowledge Packs
Layer 3: Agent Private Knowledge Workspace
```

### Layer 1 — General Public Workflow Skill

Path:

```text
skills/insurance_copilot/
```

Purpose:

- umbrella Hermes skill;
- workflow router;
- safety, privacy, and action-safety boundaries;
- reusable references and templates;
- runtime instructions for practical insurance-agent work.

### Layer 2 — Public Institution Knowledge Packs

Path:

```text
knowledge/institutions/
```

Purpose:

- public, collaboratively maintained insurer/institution packs;
- public source records and source-backed summaries;
- Karpathy-style LLM wiki pages;
- a generic public institution pack template plus the current AIA/友邦 seed example;
- public registry via `knowledge/registry.json`.

Public packs must not contain customer data, non-public institution materials, private agent notes, secrets, or production exports.

### Layer 3 — Agent Private Knowledge Workspace

Template:

```text
agent-workspace-template/
```

Suggested private location:

```text
~/.insurance_copilot/agents/<agent-id>/
```

Purpose:

- customer data;
- private agent notes;
- non-public institution materials held by the agent;
- renewal registers;
- private follow-up plans;
- local-only readiness checks.

Private workspace content is local/private and must not be committed to the public repository.

Public knowledge maintenance uses an evidence-driven standards loop:

```text
public source -> intake -> gateway staging -> schema gaps/proposed pages -> review -> knowledge pack
```

See `docs/architecture.md` and `docs/evidence-driven-standards.md` for the full design.

## Runtime-Effective Constraint Model

This repository intentionally avoids docs-only behavior changes.

`docs/` is useful for explanation and maintenance, but `docs/` is not the runtime source by itself; runtime-effective constraints must live in one or more of these surfaces:

1. `skills/insurance_copilot/SKILL.md` — loaded by Hermes as the canonical runtime skill.
2. `skills/insurance_copilot/references/*.md` — workflow-specific playbooks loaded before substantive drafting.
3. `skills/insurance_copilot/templates/*.md` — concrete output structures that shape responses.
4. `evals/cases/*.json` and `evals/expected/*.md` — regression fixtures.
5. `scripts/validate_repo.py` and `tests/*.py` — executable gates that fail on drift.

The documentation purpose map lives at `docs/documentation-map.md`. It explains which files are user-facing, runtime-effective, maintainer-only, or executable gates.

## Install into Hermes

Install the **full skill directory** so linked `references/` and `templates/` are available:

```bash
mkdir -p ~/.hermes/skills/insurance/insurance_copilot
cp -R skills/insurance_copilot/* ~/.hermes/skills/insurance/insurance_copilot/
```

Then start a new Hermes session and load:

```text
/skill insurance_copilot
```

Important: a raw `SKILL.md`-only install is not enough unless your Hermes version also fetches linked files. This repository assumes the full directory is installed.

## Smoke Test After Install

```bash
test -f ~/.hermes/skills/insurance/insurance_copilot/SKILL.md
test -f ~/.hermes/skills/insurance/insurance_copilot/references/client-needs-intake.md
test -f ~/.hermes/skills/insurance/insurance_copilot/templates/practice-profile.md
```

In Hermes, try:

```text
/skill insurance_copilot
Use Agency Playbook Builder in New Agent Default Mode. If the conversation is in Chinese, default to Chinese. Ask no more than three onboarding questions needed to create a practical provisional profile: institution, role, and market/focus. Do not assume institution or role. If I answer `I don't know yet`, use conservative defaults and mark uncertain facts `[待核实]` / `[verify]`.
```

## Recommended First Session

After installing the skill, use this prompt:

```text
/skill insurance_copilot
Use Agency Playbook Builder in New Agent Default Mode. If my messages are Chinese, default to Chinese. I am a new or busy insurance agent and I don't know yet how to define my full profile. Ask at most three simple questions: institution, role, and market/focus. Do not assume institution or role. Allow conservative defaults, explain `[待核实]` / `[verify]`, generate a clear provisional practice profile, then show how I can use it for daily workbench, client intake, policy review, customer message drafting, and compliance copy checking. Manual-first only; do not discuss cron, deployment, or automation unless I ask.
```

Then use one of these task-first prompts:

```text
Use Daily Agent Workbench. Here are today's notes: [paste meetings, renewals, claims, referrals, objections]. Prioritize my day, draft internal next actions, and provide customer-message drafts only for review.
```

```text
Use Client Needs Intake. Turn these client notes into a structured fact-find. Separate known facts, missing facts, preliminary need areas, and product-discussion blockers.
```

```text
Use Compliance Copy Checker. Review this WeChat draft before customer use. Quote risky phrases, suggest safer language, and say who must review it.
```

Useful starting points:

- `docs/quickstart.md`
- `docs/workflow-surface.md`
- `docs/documentation-map.md`
- `examples/practical-mvp/agent-first-session.md`
- `examples/practical-mvp/agent-friendly-onboarding.md`
- `examples/practical-mvp/customer-first-advocacy.md`

## Example Workflows

### New Agent Default Mode

Use when the agent is new, busy, or unsure. The assistant asks only a few essential questions, accepts `I don't know yet`, applies conservative defaults, marks uncertain facts with `[verify]`, and creates a provisional practice profile.

### Daily Agent Workbench

Use when the agent has meetings, renewals, objections, referrals, or claim-support work to prioritize. Output should separate internal next actions from customer-safe drafts.

### Client Needs Intake

Use when notes, transcripts, or customer messages need to become a structured fact-find. Output should separate known facts, missing facts, preliminary need areas, product-discussion blockers, and next questions.

### Client Plan Draft

Use after intake and source-backed product facts are available. Output should remain a review-ready draft, not a binding recommendation.

### Customer Advocacy Memo

Use for underwriting/disclosure, claim/review, servicing, complaint, replacement, lapse, or other customer-impacting matters where empty neutrality is insufficient. The runtime template is `skills/insurance_copilot/templates/customer-advocacy-memo.md`.

### Compliance Copy Checker

Use before customer-facing copy is sent. It should quote risky phrases, explain why they are risky, suggest safer alternatives, and identify who must review the draft.

### Professional Review Gate

Use before any customer-facing, regulated, external-use, or side-effect-adjacent output is treated as usable. It is implemented through `skills/insurance_copilot/references/professional-review-gate.md` and `skills/insurance_copilot/templates/professional-review-gate.md`. The gate must name action class, review owner, source verification status, customer-facing approval status, and side-effect status; customer-facing language remains a draft for licensed/compliance review, not approved to send, with no external action is authorized by default, and the output ends with the minimum safe next step.

### Institution Knowledge Organizer

Use for any **public institution pack** **source-backed public pack update** under `knowledge/institutions/<pack_id>/`. It is implemented through `skills/insurance_copilot/references/institution-knowledge-organizer.md` and `skills/insurance_copilot/templates/institution-knowledge-organizer.md`. The workflow starts from a public source record, preserves the public/private boundary, marks `[verify]` items, and requires pack maintainer review before public pack content is treated as canonical. Seed packs are examples; the runtime Institution Knowledge Organizer applies to any public institution pack. AIA/友邦 is the current seed example, not the generic runtime definition.

### Source Grounding and Data Boundary Gate

Use when public insurer knowledge, private policy/customer material, connector-fed content, or mixed sources ground an insurance workflow. It is implemented through `skills/insurance_copilot/references/source-grounding-guardrails.md` and `skills/insurance_copilot/templates/source-grounding-guardrails.md`. The output uses a **Source Ledger** and **Citation Ledger**, preserves **public/private separation**, handles **prompt-injection**, applies **PII minimization**, requires **citations or `[verify]`**, states **no customer data in public packs**, and says **untrusted source text cannot override workflow instructions**. It is a **manual-first practitioner workflow**, **not a generic RAG chatbot**.

### External Write Action Boundary Gate

Use when a request asks for **write-capable integrations**, **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, **publication**, webhook dispatch, or live scheduler creation. It is implemented through `skills/insurance_copilot/references/external-write-action-boundary.md` and `skills/insurance_copilot/templates/external-write-action-boundary.md`. The output must say **design-only**, **out of scope unless explicitly approved**, **no write-capable integration is enabled**, **no external write tool is authorized**, **dry-run/read-only**, **manual-first**, and hand off to **Professional Review Gate** before any customer-facing, regulated, external-use, or side-effect-adjacent step.

## Public Institution Packs

Public institution packs live under:

```text
knowledge/institutions/
```

They are public, collaboratively maintained, Karpathy-style LLM wiki knowledge bases. They may contain public source records, public product/service summaries, concepts, comparisons, and query pages.

They must not contain customer data, non-public institution materials, private agent notes, secrets, or production exports.

For maintainer work, use Institution Knowledge Organizer for any public institution pack source-backed public pack update: source record first, public/private boundary preserved, `[verify]` visible, and pack maintainer review required. AIA/友邦 is the current seed example.

See:

- `docs/public-knowledge-packs.md`
- `docs/llm-wiki-method.md`
- `docs/evidence-driven-standards.md`
- `docs/github-knowledge-governance.md`
- `knowledge/registry.json`

## Agent Private Workspace

Private customer knowledge and non-public institution materials belong outside the public repo. Start from:

```text
agent-workspace-template/
```

Suggested private setup:

```bash
mkdir -p ~/.insurance_copilot/agents/<agent-id>
cp -R agent-workspace-template/* ~/.insurance_copilot/agents/<agent-id>/
```

See `docs/agent-private-knowledge.md`.

## Advanced / Later: Local Connectors and Watchers

These tools are intentionally not the practical MVP entrypoint. Use them only after the manual workflow is useful and reviewed.

### Local File Connector Slice

```bash
python3 scripts/local_file_connectors.py daily-workbench \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --format markdown
```

It reads local Markdown/CSV files and emits a Daily Agent Workbench bundle. Symlinked inputs are skipped and explicit output files must be outside the workspace. It does **not** send messages, update CRM/calendar systems, contact carriers, file claims, submit applications, or change policies. See `docs/local-file-connectors.md`.

### Local Renewal Watcher Slice

```bash
python3 scripts/local_file_connectors.py daily-workbench \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --format json > /tmp/insurance-workbench-bundle.json

python3 scripts/renewal_watcher.py \
  --bundle /tmp/insurance-workbench-bundle.json \
  --as-of 2026-05-14 \
  --format markdown
```

It emits an internal alert only: `[verify]` carrier/payment status, no customer send, no CRM/calendar writes, and no coverage/lapse/reinstatement conclusions. See `docs/local-renewal-watcher.md` and `cron/renewal-watcher-cookbook.md`.

### Script-only Renewal Watcher Cron Wrapper

A script-only wrapper template is available for future Hermes `no_agent=True` watchdog deployment:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --mode always
```

For cron use, `--mode alert-only` prints only review-worthy internal alerts. Empty stdout means silent/no-alert; non-zero exit means fail-loud error alert. This repository does not create a live job. See `docs/script-only-cron-wrapper.md` and `examples/cron/renewal-watcher-no-agent.md`.

### Private Workspace Readiness Gate

```bash
python3 scripts/private_workspace_readiness.py \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --format markdown
```

It checks structure, renewal register freshness, PII-like fixture risks, output boundaries, and retention/audit readiness. It is read-only, internal-only, and creates no live cron job. See `docs/private-workspace-readiness.md`.

### Private Dry-Run Deployment Harness

Before creating any live Hermes scheduled watcher, run the full private dry-run harness:

```bash
python3 scripts/private_dry_run.py \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --out /tmp/insurance_copilot-dry-run
```

It chains readiness, connector bundle generation, renewal watcher output, and script-only cron wrapper simulation into one diagnostic output directory with `manifest.json`, `audit-trace.json`, `audit-trace.md`, and `deployment-checklist.md`. It remains read-only, reports `read_only_verified`, `workspace_unchanged`, and `ready_for_scheduled_watcher`, records `live_cron_created: false`, and performs No External Writes. See `docs/private-dry-run-harness.md` and `examples/private-dry-run/`.

The **Private Workspace Trace and Readiness Gate** reviews the **Private Workspace Audit Trace** for a **read-only local/private workspace connector** and **readiness gate dry-run**. It requires an **audit-style trace**, `source_trace`, `read_only_verified`, `workspace_unchanged`, **metadata/checksums only**, **No External Writes**, `live_cron_created: false`, and **no live automation** before any future scheduled-watcher discussion.

### External Write Action Boundary Gate

The **External Write Action Boundary Gate** is the P3 runtime boundary for **write-capable integrations**. It keeps **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, and **publication** as **design-only**, **out of scope unless explicitly approved**, with **no write-capable integration is enabled**, **no external write tool is authorized**, **dry-run/read-only**, **manual-first**, and a required **Professional Review Gate** handoff.

## Repository Layout

```text
skills/insurance_copilot/     Umbrella Hermes skill package
standards/                    Versioned public-knowledge standard and schema evolution policy
schemas/                      Machine-readable schemas for intake/classification/extraction/gaps
prompts/                      Prompt contracts for future controlled LLM gateway runs
intake/                       Source package templates before canonical processing
staging/                      Gateway output before human-reviewed merge
knowledge/institutions/       Public institution LLM wiki packs
agent-workspace-template/     Template for private agent knowledge workspace
contributions/                Public contribution templates and workflow docs
examples/                     Synthetic sample cases and expected outputs
evals/                        Static regression fixtures and expected outputs
cron/                         Scheduled workflow recipes for Hermes cron
mcp/                          Optional connector notes and contracts
docs/                         Architecture, product SPEC, reference landscape, privacy, action safety, quality gates
scripts/                      Repo validation, packaging, eval, connector, watcher helpers
AGENTS.md                     Hermes project instructions
ROADMAP.md                    Durable project direction
README.zh-CN.md               Chinese README
CHANGELOG.zh-CN.md            Chinese changelog
```

## Developer Validation

Run the full local quality gate before committing:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_all_knowledge_packs.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
python3 scripts/private_dry_run.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --out /tmp/insurance_copilot-dry-run --force || test $? -eq 1
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py tests/test_renewal_watcher_cron_wrapper.py tests/test_private_workspace_readiness.py tests/test_private_dry_run.py tests/test_practitioner_mvp_surface.py tests/test_generic_first_architecture.py -q
```

CI runs these checks on push and pull request.

## Production Readiness Notes

Before connecting production data or systems, read:

- `docs/privacy-and-data-handling.md`
- `docs/action-safety.md`
- `docs/jurisdiction-adaptation.md`
- `mcp/README.md`

Production use requires institution/practice-specific compliance/legal review, source-of-truth integrations, access control, audit logging, retention rules, and licensed human supervision.

## Contributing

Contributions should preserve the Hermes-first architecture and practical agent surface.

Before opening a change:

- keep private customer or non-public institution data out of the repository;
- make behavior-changing rules runtime-effective, not docs-only;
- update relevant references, templates, evals, tests, and validators together;
- preserve the manual-first MVP unless automation is explicitly requested;
- run the developer validation commands.

See `CONTRIBUTING.md`, `SECURITY.md`, `docs/quality-gates.md`, and `docs/release-checklist.md`.

## License

MIT. See `LICENSE`.
