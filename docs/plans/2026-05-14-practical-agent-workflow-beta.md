# Practical Agent Workflow Beta Implementation Plan

> **For Hermes:** This plan is the durable handoff artifact for improving Insurance Copilot without context loss. If a conversation is compressed or interrupted, resume by reading this file, `AGENTS.md`, `README.md`, `skills/insurance-copilot/SKILL.md`, and running the validation commands at the bottom. Use subagent-driven-development for independent tasks when context is tight.

**Goal:** Move Insurance Copilot from an architecture-first insurance knowledge framework toward a practitioner-facing assistant whose feasibility, usability, and professional discipline are closer to `claude-for-legal`.

**Architecture:** Keep the existing Hermes-first three-layer design. Shift the first user experience from standards/schema/gateway to job-style insurance workflows: cold-start profile, daily workbench, client plan draft, private CRM-lite workspace, compliant Chinese talk tracks, renewal/lapse operations, and synthetic end-to-end demos. Evidence-driven standards remain a maintenance layer, not the front-door user experience.

**Tech Stack:** Markdown Hermes skill files, repository validators in Python 3, synthetic examples/evals, GitHub Actions validation.

---

## Reference Shape: claude-for-legal -> insurance-copilot

`claude-for-legal` succeeds because it foregrounds:

1. quick install and first command;
2. cold-start interview / practice profile;
3. job-style workflow commands and named agents;
4. connectors to authoritative systems;
5. scheduled watchers;
6. explicit professional review gates.

Insurance Copilot should map those patterns as follows:

- Claude plugin slash commands -> Hermes job-style invocation prompts and workflow router entries.
- `CLAUDE.md` practice profile -> private `agent-workspace-template/AGENT.md` + `templates/practice-profile.md` + profile gating rules.
- Practice-area agents -> Hermes cron/watch cookbook recipes under `cron/`.
- Legal connectors -> insurance read-only connector contracts and local-file examples under `mcp/` and `agent-workspace-template/`.
- Attorney review draft -> licensed/compliance review draft with role/destination-sensitive output headers.

## Non-goals for this phase

- Do not add a web app.
- Do not add Claude plugin metadata.
- Do not ingest real AIA/customer data yet.
- Do not automate customer sending, policy changes, claims filing, application submission, or CRM writes.
- Do not keep expanding schemas unless required by the practical workflows below.

## Context-Continuity Rules

When resuming after interruption:

1. Read this plan first.
2. Run `git status --short` before edits.
3. Complete only the next unchecked task below; do not redesign the whole project.
4. After each task, update this plan's **Progress Log** and run the relevant targeted validator/test.
5. Keep public repo artifacts synthetic/de-identified only.
6. Full verification before final commit/push:

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_all_knowledge_packs.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/_template --template
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
python3 -m pytest tests/test_ingest_gateway.py -q
```

## Gate Model

- **Pre-flight gate:** repo clean enough to edit; plan exists; no real customer data in intended files.
- **Revision gate:** after each implementation task, compare files to this plan's acceptance criteria and revise before moving on.
- **Escalation gate:** if a task requires real institution/customer data, stop and keep only synthetic placeholders unless user explicitly authorizes a separate data-source task.
- **Abort gate:** if context gets tight or tool calls are near limit, update Progress Log and stop with a clear resume point.

---

## Task 1: Add practitioner-first workflow surface

**Objective:** Make the project read like a usable insurance assistant, not a standards project.

**Files:**
- Create: `docs/workflow-surface.md`
- Modify: `README.md`
- Modify: `docs/quickstart.md`
- Modify: `skills/insurance-copilot/SKILL.md`

**Required workflow names:**

- Agency Playbook Builder
- Daily Agent Workbench
- Client Needs Intake
- Coverage Gap Drafter
- Client Plan Draft
- Product Fit Reviewer
- Compliance Copy Checker
- Policy Review Assistant
- Replacement Risk Triager
- Renewal/Lapse Follow-up Planner
- Claims Support Triage
- Objection Response Drafter
- Referral Ask Drafter
- Stakeholder Summary Writer
- Institution Knowledge Organizer

**Acceptance criteria:**

- README has a top-level `## Start Here: Practitioner Workflows` before architecture-heavy sections.
- `docs/workflow-surface.md` includes for each workflow: when to use, required inputs, output, review owner, forbidden actions, standard prompt.
- `SKILL.md` router mentions all new job-style names and maps them to references/templates.
- Quickstart starts with cold-start and a practical daily/client loop, not standards.

---

## Task 2: Strengthen cold-start / practice-profile gate

**Objective:** Match `claude-for-legal` discipline: without a profile, do not pretend to know the agency's playbook.

**Files:**
- Modify: `skills/insurance-copilot/SKILL.md`
- Modify: `skills/insurance-copilot/references/cold-start-interview.md`
- Modify: `skills/insurance-copilot/templates/practice-profile.md`
- Modify: `docs/quickstart.md`

**Acceptance criteria:**

- `SKILL.md` has a `Practice Profile Gate` section.
- Gate allows only generic education, intake, missing-info checklists, and profile creation before a profile exists.
- Gate blocks specific product-fit conclusions, replacement suggestions, customer-facing scripts, and external action drafts unless profile/context is supplied or output is clearly provisional.
- Cold-start reference supports Quick Start and Full Setup modes.
- Practice profile template includes: role/license scope, jurisdictions, carrier/product lines, approved script sources, compliance reviewer, escalation path, customer data policy, CRM/tool status, institution/public pack preference, output style.

---

## Task 3: Build CRM-lite private workspace templates

**Objective:** Make the private workspace useful for daily customer operations while keeping it public-template safe.

**Files:**
- Create directories and README/template files under:
  - `agent-workspace-template/leads/`
  - `agent-workspace-template/opportunities/`
  - `agent-workspace-template/meetings/`
  - `agent-workspace-template/policies/`
  - `agent-workspace-template/claims/`
  - `agent-workspace-template/referrals/`
  - `agent-workspace-template/tasks/`
- Create: `agent-workspace-template/renewal-registers/template-renewal-register.csv`
- Create: `agent-workspace-template/tasks/template-daily-workbench.md`
- Modify: `agent-workspace-template/README.md`
- Modify: `agent-workspace-template/SCHEMA.md`
- Modify: `agent-workspace-template/index.md`
- Modify: `scripts/validate_agent_workspace.py`

**Acceptance criteria:**

- Workspace validator requires the new CRM-lite directories.
- Template contains no real PII.
- Templates support: lead, customer, opportunity, meeting note, policy summary, renewal register, claim tracker, referral tracker, task list.
- README clearly says private workspace is not public and may contain sensitive data only in private copies.

---

## Task 4: Add Daily Agent Workbench workflow

**Objective:** Provide a daily operating loop for real insurance agents.

**Files:**
- Create: `skills/insurance-copilot/references/daily-agent-workbench.md`
- Create: `skills/insurance-copilot/templates/daily-agent-workbench.md`
- Add synthetic example: `examples/expected-outputs/daily-agent-workbench.md`
- Add eval case: `evals/cases/daily-agent-workbench.json`
- Add expected eval: `evals/expected/daily-agent-workbench.md`
- Modify: `scripts/validate_repo.py`

**Acceptance criteria:**

- Workflow covers meetings, follow-ups, renewal/lapse, claim deadlines, replacement risks, referrals, missing facts, and compliance-sensitive drafts.
- Output sections include: Today's Priorities, High-Risk Items, Customer Follow-ups, Draft Talk Tracks, Verify Before Action, CRM/Calendar Task Export Draft.
- It explicitly forbids automatic sending and CRM writes.
- Eval checks include `draft`, `[verify]`, `no automatic sending`, and task prioritization.

---

## Task 5: Add Client Plan Draft workflow

**Objective:** Turn intake + gap + product facts into a review-ready client proposal draft without pretending to make final recommendations.

**Files:**
- Create: `skills/insurance-copilot/references/client-plan-draft.md`
- Create: `skills/insurance-copilot/templates/client-plan-draft.md`
- Add example: `examples/expected-outputs/client-plan-draft.md`
- Add eval case: `evals/cases/client-plan-draft.json`
- Add expected eval: `evals/expected/client-plan-draft.md`
- Modify: `scripts/validate_repo.py`

**Acceptance criteria:**

- Output includes customer profile, confirmed needs, missing facts, current coverage, gap summary, candidate solution categories, product/source caveats, compliance flags, customer-safe summary, internal notes, next questions.
- No `best`, `guaranteed`, or final advice language.
- Requires source hierarchy and `[verify]` for product facts.

---

## Task 6: Add Chinese talk tracks and referral workflow

**Objective:** Add practical Chinese-language daily communication support with compliance safeguards.

**Files:**
- Create: `skills/insurance-copilot/references/chinese-talk-tracks.md`
- Create: `skills/insurance-copilot/references/referral-ask.md`
- Create: `skills/insurance-copilot/templates/chinese-talk-tracks.md`
- Create: `skills/insurance-copilot/templates/referral-ask.md`
- Add examples/evals as needed.
- Modify: `scripts/validate_repo.py`

**Acceptance criteria:**

- Talk tracks cover WeChat/WhatsApp short messages, phone invite, policy review invite, premium reminder, claims care, referral ask, event invite, objection follow-up.
- Each track includes: scenario, safe draft, forbidden phrases, verify items, escalation triggers.
- Referral workflow is low-pressure, non-misleading, no guaranteed outcomes, no exploitation of vulnerable customers.

---

## Task 7: Upgrade renewal/lapse operations

**Objective:** Make renewal/lapse support operational, not just conceptual.

**Files:**
- Modify: `skills/insurance-copilot/references/renewal-review.md`
- Modify: `skills/insurance-copilot/templates/renewal-review.md`
- Modify: `cron/renewal-watcher.md`
- Create: `cron/renewal-watcher-cookbook.md`
- Create or update examples/evals if needed.

**Acceptance criteria:**

- Includes D-30, D-14, D-7, D+1, grace-period-before-end stages.
- Requires carrier status verification.
- Produces internal task list and customer draft language separately.
- Cookbook states tool scope, inputs, outputs, cadence, review owner, forbidden actions, and handoff gate.

---

## Task 8: Add synthetic end-to-end demo

**Objective:** Prove the project helps an agent complete a realistic daily loop without real data.

**Files:**
- Create: `examples/end-to-end/family-protection-workflow.md`
- Create supporting synthetic inputs under `examples/end-to-end/` if useful.
- Modify: `docs/quickstart.md`
- Modify: `README.md`

**Acceptance criteria:**

- Demo runs: cold-start assumptions -> intake -> coverage gap -> client plan draft -> compliance check -> stakeholder summary -> daily workbench next actions.
- Uses synthetic data only.
- Shows where `[verify]` appears.
- Shows review gates before customer-facing use.

---

## Task 9: Quality gates and validators

**Objective:** Prevent future context loss or regression from removing practitioner-first assets.

**Files:**
- Modify: `scripts/validate_repo.py`
- Modify: `scripts/validate_agent_workspace.py`
- Modify: `docs/quality-gates.md`
- Modify: `.github/workflows/validate.yml` only if new commands are added.

**Acceptance criteria:**

- Validator requires new core references/templates and `docs/workflow-surface.md`.
- Validator requires CRM-lite workspace directories.
- Validator requires at least 12 eval cases after new workflows.
- Quality gates mention first-day usability, daily workflow coverage, and practical workflow beta.

---

## Task 10: Reflection and iteration

**Objective:** Check whether implementation met the plan and improve once before final handoff.

**Files:**
- Create: `docs/reviews/practical-agent-workflow-beta-review.md`
- Modify files as needed based on review.

**Acceptance criteria:**

- Review answers: what improved vs `claude-for-legal`, what remains weaker, what is still non-goal, what next phase should do.
- Review includes a checklist against all tasks above.
- Any missed acceptance criteria are fixed before final commit.

---

## Progress Log

Use this section as the canonical checkpoint after every interruption.

- 2026-05-14: Plan created. Next task: Task 1 practitioner-first workflow surface.

- 2026-05-14: Implemented Tasks 1-10 in one practical beta pass: workflow surface, profile gate, CRM-lite workspace, daily workbench, client plan, Chinese talk tracks, referral ask, renewal cookbook, synthetic E2E, validators, and review. Next: run full verification, fix regressions, commit and push.
