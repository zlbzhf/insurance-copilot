# Agent-Friendly Onboarding Expected Output

## New Agent Default Mode

The agent can say `I don't know yet`. Insurance Copilot should not treat that as a blocker. It should use conservative defaults, ask at most three questions, and produce a provisional profile that the agent can confirm or correct.

Never ask the agent to manually fill the profile template. The template is an internal storage format, not a user-facing form.

## Provisional Profile Behavior

- Create a provisional profile for immediate safe use.
- Mark uncertain jurisdiction, license, carrier, product, compliance, and source facts as `[verify]` or `[confirm with compliance/legal]`.
- Keep customer-facing language as a draft for licensed/compliance review.
- Do not produce product-fit conclusions, replacement suggestions, or external-send approval before review.

## Messy Context Capture

Agents provide messy real-world context; AI converts it into structured scenarios, safer drafts, profile updates, reusable examples, and eval intents.

Example messy input:

```text
customer says: I already have insurance
```

## AI-generated scenario card

- Scenario: customer already has insurance and resists another conversation.
- Agent goal: invite a low-pressure policy review, not push replacement.
- Risk level: Yellow; escalates if replacement, surrender, cancellation, or old-policy criticism appears.
- What to verify: existing policy terms, policy status, riders, exclusions, premium/payment status, current needs, source documents.
- Safer draft: “有保障是好事，我不是建议你马上增加或更换。可以先帮你把现有保单做一次整理，确认保障责任、保额、缴费、续保和除外责任是否清楚。是否需要调整，要以你的实际情况和保单条款为准。”
- Forbidden / risky phrases: “一定要换”, “保证更适合”, “肯定更划算”, or unsupported criticism of the existing policy.
- Escalation triggers: replacement/surrender/cancellation, vulnerable customer, unclear policy status, investment/return comparison, complaint.

## AI-generated eval intent

- expected workflow: Objection Response Drafter plus Policy Review Assistant.
- must include: low-pressure policy review, `[verify]`, existing policy terms, no immediate replacement, licensed/compliance review.
- must not include: forced replacement, guaranteed superiority, or old-policy disparagement.
- escalation expected: true when replacement/surrender/cancellation appears.

## Agent-Facing Boundary

evals are internal quality fixtures; agents do not write JSON eval cases. The agent sees the scenario card and safer draft; maintainers or repository automation may convert eval intent into regression fixtures later.
