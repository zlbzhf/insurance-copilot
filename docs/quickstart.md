# Quickstart: Practical Insurance Agent Loop

Use this guide when you want a usable first version of Insurance Copilot in Hermes. It is deliberately **manual-first**: the agent talks naturally, the assistant organizes the work, and every customer-facing result remains a draft for licensed/compliance review.

## The 30-Minute Useful Loop

### 1. Install and Load

```bash
mkdir -p ~/.hermes/skills/insurance/insurance-copilot
cp -R skills/insurance-copilot/* ~/.hermes/skills/insurance/insurance-copilot/
```

In Hermes:

```text
/skill insurance-copilot
```

### 2. Create the Practice Profile Without a Form

Never ask the agent to manually fill the profile template. The template is an internal storage format, not a user-facing form. Start with **New Agent Default Mode** if the agent is new, busy, or says `I don't know yet`.

Prompt:

```text
Use Agency Playbook Builder in New Agent Default Mode. I am a new AIA/友邦 agent serving Chinese-speaking clients. I don't know yet how to define my full positioning. Ask at most three simple questions, use conservative defaults where I am unsure, then generate a provisional practice profile and show what I can do next.
```

Expected behavior:

- asks no more than three onboarding questions before producing a provisional profile;
- every question accepts `I don't know yet` or conservative defaults;
- uses New Agent Default Mode instead of a long form;
- marks unknown compliance/legal/product facts as `[confirm with compliance/legal]` or `[verify]`;
- explains that the profile is dynamic and can be updated as the agent receives feedback or repeats scenarios;
- does not draft reusable customer scripts or product-fit conclusions until enough context exists.

### 3. Run Daily Agent Workbench

Prompt:

```text
Use Daily Agent Workbench. Here are today's notes: one family-protection meeting, one policy renewal due soon with carrier status unknown, one claim-support question, and one referral thank-you. Prioritize my day, separate internal next actions from customer-facing drafts, and do not send or write anything automatically.
```

Expected behavior:

- prioritizes high-risk renewal/lapse and claim items;
- marks policy/payment/claim facts `[verify]`;
- drafts customer language only as review drafts;
- produces internal CRM/calendar task export drafts without external writes.

### 3A. Coach a New Agent Through a Live Situation

Prompt:

```text
Use New Agent Coach Mode. I am a new agent and a customer says an old policy may cover a loss, but I do not know whether it is a claim, policy review, or complaint. Explain what this situation is, what to do first, what not to do, what to collect, what customer-safe words I can use, who to escalate to, and which workflow should handle the full draft.
```

Expected behavior:

- explains what this situation is in plain language;
- gives one to three steps for what to do first;
- names what not to do, including no guarantees, no document alteration, and no dismissive `nothing can be done` answer;
- lists what to collect and source-check;
- provides customer-safe language;
- names who to escalate to;
- routes to Policy Review Assistant and Claims Support Triage if a possible benefit or claim path exists.

### 4. Structure Client Notes

Prompt:

```text
Use Client Needs Intake. Turn these notes into a structured fact-find: Couple ages 35 and 34, two children, mortgage, employer health coverage, unknown life/disability coverage, wants family protection and education funding, budget unknown.
```

Expected behavior:

- separates known facts from missing facts;
- says product recommendation is premature when facts are incomplete;
- asks for budget, income, existing coverage, jurisdiction, health-disclosure boundaries, and approved source materials.

### 5. Draft Coverage Gaps Without Product Recommendations

Prompt:

```text
Use Coverage Gap Drafter. Based on the intake above, draft a coverage-gap analysis. Use possible solution categories only, mark assumptions as [verify], and do not recommend a specific product.
```

Expected behavior:

- identifies possible life, income-interruption/disability, medical/critical illness, accident, and education-funding needs where appropriate;
- separates facts from assumptions;
- avoids naming products unless a separate source-backed product-fit review is requested.

### 6. Draft or Check Customer Language

Prompt:

```text
Use Compliance Copy Checker. Review this WeChat draft before customer use: "This is guaranteed approval and the best risk-free plan for every family." Quote risky phrases, classify risk, suggest safer wording, and state who must review it.
```

Expected behavior:

- classifies the draft as Red risk;
- flags guaranteed approval, best, risk-free, and every family;
- provides safer language;
- requires licensed/compliance review before use.

### 7. Summarize for Agent and Customer

Prompt:

```text
Use Stakeholder Summary Writer. Summarize the intake, gap notes, and safer draft for me as the agent, then create a customer-safe version. Preserve [verify] markers and keep internal risk notes out of the customer copy.
```

Expected behavior:

- separates internal agent notes from customer-safe language;
- preserves caveats and `[verify]` markers;
- lists review gates before external use.

## Task-First Routing Rule

If you already know the job, say it directly:

```text
Use Policy Review Assistant...
Use Replacement Risk Triager...
Use Claims Support Triage...
Use Referral Ask Drafter...
```

Do not ask Insurance Copilot to show the entire workflow catalog unless you are exploring. The skill should behave as a task router, ask at most three essential missing questions, then produce a review-ready draft.

## Complete Example

See:

```text
examples/practical-mvp/agent-first-session.md
```

## Advanced Appendix

The following tools are for later, after the manual workflow is useful and reviewed. They are not required for the practical MVP.

### Local File Connector Bundle

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format markdown
```

Paste the bundle into Hermes with:

```text
Use Daily Agent Workbench on this local connector bundle. Preserve [verify] markers, do not send or write anything automatically, and produce licensed/compliance review drafts only.
```

### Internal Renewal Watcher

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format json > /tmp/insurance-workbench-bundle.json
python3 scripts/renewal_watcher.py   --bundle /tmp/insurance-workbench-bundle.json   --as-of 2026-05-14   --format markdown
```

Expected behavior: internal alert only, `[verify]` status language, `No External Writes`, no customer send, no CRM/calendar write.

### Private Workspace Readiness / Dry Run

Only consider these before any scheduled monitoring is explicitly requested and approved:

```bash
python3 scripts/private_workspace_readiness.py   --workspace examples/local-connectors/synthetic-agent-workspace   --as-of 2026-05-14   --format markdown

python3 scripts/private_dry_run.py   --workspace examples/local-connectors/synthetic-agent-workspace   --as-of 2026-05-14   --out /tmp/insurance-copilot-dry-run   --force
```

They remain read-only and do not create live jobs.
