# Insurance Copilot

Hermes-first insurance workflow copilot for licensed insurance professionals. It is inspired by the workflow discipline of `claude-for-legal`, but the usable surface is a **Hermes skill** for practical insurance-agent work, not a Claude plugin, web app, or deployment platform.

## Practical MVP: How an Agent Uses It

Insurance Copilot is a **workflow router, not a menu bot**. The agent should describe the job they want done, and Hermes should route directly to the right insurance workflow. Only ask follow-up questions when facts are needed to produce a safe draft.

Product posture: **customer-first advocacy within compliance boundaries**. The assistant should provide maximum lawful support, build client-interest action plans and advocacy memos, and not use neutral caveats as a substitute for service. It still must refuse concealment, misrepresentation, fabricated evidence, unauthorized legal advice, or outcome guarantees.

manual-first MVP loop:

```text
practice profile -> task-specific workflow -> source/private facts -> review-ready draft -> licensed/compliance review
```

Start with these practical jobs:

1. **Set my practice profile** — answer a few guided questions or use New Agent Default Mode; the assistant generates the profile, the agent confirms/corrects it.
2. **Plan my day** — meetings, renewals, claim-support items, referrals, objections, and follow-up messages.
3. **Organize client notes** — turn messy notes or transcripts into a structured fact-find and missing-question list.
4. **Review a policy or coverage situation** — summarize known facts, likely gap areas, replacement/lapse/claim risks, and verification needs.
5. **Draft a customer message** — create a low-pressure WeChat/email/talk-track draft with compliance flags.
6. **Check risky copy** — flag guarantee, best, risk-free, pressure, replacement, claim, or investment-language risks.
7. **Organize public insurer knowledge** — route public AIA/友邦 or other insurer sources into the public knowledge-pack process.

If the user already states a job, do **not** list all workflows. Route directly, ask at most three essential missing questions, and produce a clearly labeled draft.

## Recommended First Session

After installing the skill, use this prompt:

```text
/skill insurance-copilot
Use Agency Playbook Builder in New Agent Default Mode. I am a new or busy insurance agent and I don't know yet how to define my full profile. Ask at most three simple questions, allow conservative defaults, generate a provisional practice profile, then show how I can use it for daily workbench, client intake, policy review, customer message drafting, and compliance copy checking. Manual-first only; do not discuss cron, deployment, or automation unless I ask.
```

Never ask the agent to manually fill the profile template. The template is an internal storage format, not a user-facing form. Agents provide messy real-world context; AI converts it into structured scenarios, profile updates, reusable examples, and eval intents. evals are internal quality fixtures; agents do not write JSON eval cases.

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

See `docs/quickstart.md`, `docs/workflow-surface.md`, `examples/practical-mvp/agent-first-session.md`, `examples/practical-mvp/agent-friendly-onboarding.md`, and `examples/practical-mvp/customer-first-advocacy.md` for the complete workflow surface, practical loop, low-burden new-agent onboarding example, and customer-first advocacy examples.

## What It Does

Insurance Copilot helps licensed insurance professionals create structured drafts for:

- agency playbook / practice profile setup;
- daily agent workbench planning;
- client needs intake;
- coverage-gap drafting;
- Client Plan Draft / client plan drafting;
- product-fit review from source-backed facts;
- customer message / objection / referral drafts;
- compliance language screening;
- existing policy review;
- replacement/surrender suitability triage;
- claims support triage;
- renewal/lapse follow-up planning;
- stakeholder summaries;
- public institution knowledge-pack organization.

## What It Does Not Do

It does not provide binding insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decisions. It does not automatically send customer messages, submit applications, file claims, cancel/replace coverage, create live scheduled jobs, or make binding representations.

Every customer-facing output is a draft for licensed/compliance review.

## Architecture

Insurance Copilot has three layers:

1. **General public workflow skill** — `skills/insurance-copilot/`
2. **Public institution knowledge packs** — `knowledge/institutions/`
3. **Agent private knowledge workspace** — initialize from `agent-workspace-template/`, store privately outside this repo

Public knowledge maintenance uses an evidence-driven standards loop:

```text
public source -> intake -> gateway staging -> schema gaps/proposed pages -> review -> knowledge pack
```

See `docs/architecture.md` and `docs/evidence-driven-standards.md` for the full design.

## Install into Hermes

Install the **full skill directory** so linked `references/` and `templates/` are available:

```bash
mkdir -p ~/.hermes/skills/insurance/insurance-copilot
cp -R skills/insurance-copilot/* ~/.hermes/skills/insurance/insurance-copilot/
```

Then start a new Hermes session and load:

```text
/skill insurance-copilot
```

Important: a raw `SKILL.md`-only install is not enough unless your Hermes version also fetches linked files. This repository assumes the full directory is installed.

## Smoke Test After Install

```bash
test -f ~/.hermes/skills/insurance/insurance-copilot/SKILL.md
test -f ~/.hermes/skills/insurance/insurance-copilot/references/client-needs-intake.md
test -f ~/.hermes/skills/insurance/insurance-copilot/templates/practice-profile.md
```

In Hermes, try:

```text
/skill insurance-copilot
Use Agency Playbook Builder in New Agent Default Mode. Ask no more than three onboarding questions needed to create a practical provisional profile. If I answer `I don't know yet`, use conservative defaults.
```

## Public Institution Packs

Public institution packs live under:

```text
knowledge/institutions/
```

They are public, collaboratively maintained, Karpathy-style LLM wiki knowledge bases. They may contain public source records, public product/service summaries, concepts, comparisons, and query pages.

They must not contain customer data, non-public institution materials, private agent notes, secrets, or production exports.

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

Suggested private location:

```bash
mkdir -p ~/.insurance-copilot/agents/<agent-id>
cp -R agent-workspace-template/* ~/.insurance-copilot/agents/<agent-id>/
```

See `docs/agent-private-knowledge.md`.

## Advanced / Later: Local Connectors and Watchers

These tools are intentionally not the practical MVP entrypoint. Use them only after the manual workflow is useful and reviewed.

### Local File Connector Slice

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format markdown
```

It reads local Markdown/CSV files and emits a Daily Agent Workbench bundle. Symlinked inputs are skipped and explicit output files must be outside the workspace. It does **not** send messages, update CRM/calendar systems, contact carriers, file claims, submit applications, or change policies. See `docs/local-file-connectors.md`.

### Local Renewal Watcher Slice

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format json > /tmp/insurance-workbench-bundle.json
python3 scripts/renewal_watcher.py   --bundle /tmp/insurance-workbench-bundle.json   --as-of 2026-05-14   --format markdown
```

It emits an internal alert only: `[verify]` carrier/payment status, no customer send, no CRM/calendar writes, and no coverage/lapse/reinstatement conclusions. See `docs/local-renewal-watcher.md` and `cron/renewal-watcher-cookbook.md`.

### Script-only Renewal Watcher Cron Wrapper

A script-only wrapper template is available for future Hermes `no_agent=True` watchdog deployment:

```bash
bash cron/scripts/renewal_watcher.sh   --workspace examples/local-connectors/synthetic-agent-workspace   --as-of 2026-05-14   --mode always
```

For cron use, `--mode alert-only` prints only review-worthy internal alerts. Empty stdout means silent/no-alert; non-zero exit means fail-loud error alert. This repository does not create a live job. See `docs/script-only-cron-wrapper.md` and `examples/cron/renewal-watcher-no-agent.md`.

### Private Workspace Readiness Gate

```bash
python3 scripts/private_workspace_readiness.py   --workspace examples/local-connectors/synthetic-agent-workspace   --as-of 2026-05-14   --format markdown
```

It checks structure, renewal register freshness, PII-like fixture risks, output boundaries, and retention/audit readiness. It is read-only, internal-only, and creates no live cron job. See `docs/private-workspace-readiness.md`.

### Private Dry-Run Deployment Harness

Before creating any live Hermes scheduled watcher, run the full private dry-run harness:

```bash
python3 scripts/private_dry_run.py   --workspace examples/local-connectors/synthetic-agent-workspace   --as-of 2026-05-14   --out /tmp/insurance-copilot-dry-run
```

It chains readiness, connector bundle generation, renewal watcher output, and script-only cron wrapper simulation into one diagnostic output directory with `manifest.json` and `deployment-checklist.md`. It remains read-only, reports `ready_for_scheduled_watcher`, records `live_cron_created: false`, and performs No External Writes. See `docs/private-dry-run-harness.md` and `examples/private-dry-run/`.

## Repository Layout

```text
skills/insurance-copilot/     Umbrella Hermes skill package
standards/                     Versioned public-knowledge standard and schema evolution policy
schemas/                       Machine-readable schemas for intake/classification/extraction/gaps
prompts/                       Prompt contracts for future controlled LLM gateway runs
intake/                        Source package templates before canonical processing
staging/                       Gateway output before human-reviewed merge
knowledge/institutions/       Public institution LLM wiki packs
agent-workspace-template/     Template for private agent knowledge workspace
contributions/                Public contribution templates and workflow docs
examples/                     Synthetic sample cases and expected outputs
evals/                        Static regression fixtures and expected outputs
cron/                         Scheduled workflow recipes for Hermes cron
mcp/                          Optional connector notes and contracts
docs/                         Architecture, privacy, action safety, quality gates
scripts/                      Repo validation, packaging, eval, connector, watcher helpers
AGENTS.md                     Hermes project instructions
ROADMAP.md                    Durable project direction
```

## Developer Validation

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
python3 scripts/private_dry_run.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --out /tmp/insurance-copilot-dry-run --force || test $? -eq 1
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py tests/test_renewal_watcher_cron_wrapper.py tests/test_private_workspace_readiness.py tests/test_private_dry_run.py tests/test_practitioner_mvp_surface.py -q
```

CI runs these checks on push and pull request.

## Production Readiness Notes

Before connecting production data or systems, read:

- `docs/privacy-and-data-handling.md`
- `docs/action-safety.md`
- `docs/jurisdiction-adaptation.md`
- `mcp/README.md`

Production use requires institution/practice-specific compliance/legal review, source-of-truth integrations, access control, audit logging, retention rules, and licensed human supervision.
