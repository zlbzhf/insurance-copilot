# Practical MVP Example: First Agent Session

This example shows the intended first usable Insurance Copilot loop. It is synthetic and manual-first.

## Input 1 — Set the Practice Profile / 首次执业画像确认

```text
/skill insurance_copilot
使用 Agency Playbook Builder 的 Quick Start mode。请默认中文输出。我是持牌保险代理人，服务中文家庭客户，主要做寿险、医疗、重疾、储蓄/养老和保单检视。请先问最多三个必要问题：机构、角色、主要服务地区/客户/本周重点；不要默认机构或角色。如果我说“不确定”，用保守默认值并标记 `[待核实]`。然后生成层级清晰的临时执业画像。
```

Expected assistant behavior:

- default to Chinese for Chinese Telegram use and explain `[待核实]` / `[verify]` before relying on uncertain facts;
- actively confirm institution and role; never assume them from examples, memory, or an AIA seed pack;
- ask at most three onboarding questions before producing a provisional profile;
- if existing profile information is supplied, summarize existing facts first, ask the agent to confirm, mark gaps `[待核实]`, and then route to Daily Agent Workbench rather than restarting onboarding;
- avoid final product recommendations or reusable customer scripts until profile context is confirmed.

## Input 2 — Daily Workbench

```text
Use Daily Agent Workbench. Today I have: family-protection meeting at 2pm; renewal follow-up for a policy with payment status unknown; one claim-support question about required documents; one referral thank-you. Prioritize and draft internal next actions. Customer language must be review drafts only. Do not send automatically.
```

Expected output shape:

```text
## 今日优先级
1. 续保/缴费状态 `[待核实 carrier/payment status]`
2. 理赔资料清单 `[待核实 policy/carrier claim guide]`
3. 家庭保障面谈准备
4. 转介绍感谢话术草稿

## 内部行动项
- ...

## 客户话术草稿（仅供复核）
- ...

## 合规 / 升级提示
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
