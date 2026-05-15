# Practical MVP Example: First Agent Session

This example shows the intended first usable Insurance Copilot loop. It is synthetic and manual-first.

## Input 1 — Set the Practice Profile

```text
Use Agency Playbook Builder in Quick Start mode. I am a licensed insurance agent serving Chinese-speaking family clients. Main work: life, health, critical illness, savings/retirement, and policy review. Help me create a practical profile. Ask only essential questions first.
```

Expected assistant behavior:

- ask for jurisdiction/market, license scope, carriers/product lines, compliance reviewer, escalation rules, approved scripts/source hierarchy, client data policy, communication channels, and tone;
- mark unknowns `[confirm with compliance/legal]`;
- avoid final product recommendations or reusable customer scripts until profile context is confirmed.

## Input 2 — Daily Workbench

```text
Use Daily Agent Workbench. Today I have: family-protection meeting at 2pm; renewal follow-up for a policy with payment status unknown; one claim-support question about required documents; one referral thank-you. Prioritize and draft internal next actions. Customer language must be review drafts only. Do not send automatically.
```

Expected output shape:

```text
## Today's Priority Order
1. Renewal/payment status [verify carrier/payment status]
2. Claim-support document checklist [verify policy/carrier claim guide]
3. Family-protection meeting prep
4. Referral thank-you draft

## Internal Next Actions
- ...

## Customer Drafts for Review
- ...

## Compliance / Escalation Flags
- ...
```

## Input 3 — Client Intake

```text
Use Client Needs Intake. Notes: Couple ages 35/34, two children, mortgage, employer health coverage, unknown life/disability coverage, wants family protection and education funding, budget unknown.
```

Expected assistant behavior:

- separate known facts from missing facts;
- identify preliminary need areas only;
- state product discussion is premature until budget, income, existing coverage, jurisdiction, health-disclosure boundaries, and source materials are confirmed.

## Input 4 — Safer WeChat Draft

```text
Use Compliance Copy Checker. Rewrite this before customer use: "This plan is guaranteed approval and the best risk-free protection for every family."
```

Expected assistant behavior:

- classify risk as Red;
- quote risky phrases: `guaranteed approval`, `best`, `risk-free`, `every family`;
- suggest safer wording;
- state licensed/compliance review owner;
- preserve `[verify]` markers for product and underwriting facts.

## Practical Boundary
- Manual-first.
- Do not send automatically.
- Do not write CRM/calendar records automatically.
- Do not submit applications, file claims, change policies, or make binding representations.
- Customer-facing drafts remain drafts for licensed/compliance review.

## Product Principle
- Never ask the agent to manually fill the profile template; the template is an internal storage format, not a user-facing form.
- Use New Agent Default Mode when the agent says `I don't know yet` or cannot define a mature positioning statement.
- Agents provide messy real-world context; AI converts it into structured scenarios, safer drafts, profile updates, reusable examples, and eval intents.
- evals are internal quality fixtures; agents do not write JSON eval cases.
