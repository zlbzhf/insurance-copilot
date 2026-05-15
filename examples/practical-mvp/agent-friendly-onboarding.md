# Agent-Friendly Onboarding Example

This synthetic example shows the intended low-burden experience for a new or unsure insurance agent. Agents provide messy real-world context; AI converts it into structured scenarios, draft responses, profile updates, reusable examples, and eval intents. evals are internal quality fixtures; agents do not write JSON eval cases.

## Input 1 — New Agent Starts Without a Clear Positioning

```text
Use Agency Playbook Builder in New Agent Default Mode. I am a new insurance agent serving retail clients. I don't know yet how to define my full profile. Help me start safely, and ask me to confirm any institution/public pack instead of assuming one.
```

Expected assistant behavior:

- reassure the agent that `I don't know yet` is acceptable;
- ask at most three simple onboarding questions;
- every question allows `I don't know yet` or conservative defaults;
- Never ask the agent to manually fill the profile template;
- explain that the template is an internal storage format, not a user-facing form;
- generate a provisional profile with `[verify]` and `[confirm with compliance/legal]` markers;
- show next useful jobs immediately.

## Expected Output Sketch — Provisional Profile

```markdown
# Insurance Copilot Practice Profile

## Profile Status
- Mode: New Agent Default Mode
- Confidence: provisional
- Unknowns: jurisdiction, exact license scope, approved script source, compliance reviewer [verify]

## Working Assumptions
- Institution/public pack: [verify with agent; do not assume]
- Primary customer language: Chinese [verify]
- Communication style: warm, low-pressure, plain-language
- Product posture: education, fact-find, policy organization, and review-ready drafts before product recommendations

## Non-Negotiable Defaults
- No guaranteed approval, payout, savings, returns, or risk-free language
- No advice to conceal, minimize, or omit health/financial disclosures
- No replacement, surrender, cancellation, or policy change suggestions without review
- Customer-facing copy is draft language for licensed/compliance review

## Next Useful Jobs
1. Paste today's customer notes for Daily Agent Workbench
2. Paste a customer question for Client Needs Intake or Objection Response Drafter
3. Paste a WeChat draft for Compliance Copy Checker
```

## Input 2 — Messy Real-World Scenario

```text
customer says: I already have insurance, why should I look again?
```

Expected assistant behavior:

- do not require the agent to write a scenario template;
- detect this as a reusable objection / policy-review invitation scenario;
- create an AI-generated scenario card;
- provide a safer draft response;
- optionally create an AI-generated eval intent for maintainers.

## AI-generated scenario card

```markdown
## Scenario
- Customer says: I already have insurance, why should I look again?
- Agent goal: invite a low-pressure policy review, not push replacement or extra purchase
- Risk level: Yellow; becomes Red if replacement, surrender, or old-policy criticism appears
- What to verify: existing policy type, policy status, riders, exclusions, premium/payment status, customer goals
- Draft response: “有保障是好事，我不是建议你马上增加或更换。可以先帮你把现有保单做一次整理，确认保障责任、保额、缴费、续保和除外责任是否清楚。是否需要调整，要以你的实际情况和保单条款为准。”
- Forbidden / risky phrases: “你原来的不够好”, “一定要换”, “这个肯定更划算”, “保证更适合”
- Escalation triggers: any replacement/surrender/cancellation discussion, unclear policy status, vulnerable customer, investment/return comparison
```

## AI-generated eval intent

```markdown
## AI-generated eval intent
- expected workflow: Objection Response Drafter + Policy Review Assistant
- must include: low-pressure policy review, `[verify]`, existing policy terms, no immediate replacement, licensed/compliance review
- must not include: `一定要换`, `保证更适合`, `肯定更划算`, old-policy disparagement
- escalation expected: true if replacement/surrender/cancellation is mentioned
```

Maintainers may convert this intent into `evals/cases/*.json`, but the agent does not need to see or edit JSON.
