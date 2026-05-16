# Cold-Start Interview

Use this workflow before substantive production use. The goal is to create or update the agency practice profile that all other Insurance Copilot workflows read.

## Product Principle

Never ask the agent to manually fill the profile template. The template is an internal storage format, not a user-facing form. The agent-facing experience is guided onboarding: short questions, safe defaults, choices, and a draft profile the agent can confirm or correct.

New or busy agents should be able to say `I don't know yet` and still get a useful conservative setup. Use conservative defaults when the agent is unsure.

## Chinese Interactive First Entry and Profile Confirmation / 中文交互首次入口与资料确认

- These defaults apply across any interactive conversational gateway and are not limited to any single platform. 默认使用中文 unless the agent explicitly asks for another language. Use bilingual terms only when a regulated English term avoids ambiguity.
- `[待核实]` is the Chinese-facing equivalent of `[verify]`. 含义：该事实目前没有足够来源支撑，必须向客户、保单、保险公司系统、主管、合规、核保、理赔或正式文件复核后才能用于客户发送或结论。
- If no usable profile exists, ask at most three onboarding questions and then create a provisional profile. The first-run questions must 主动询问机构 and 主动询问角色; 不得默认机构 and 不得默认角色 from examples, memories, seed packs, or inferred context.
- If 已有资料, an uploaded profile, or a private workspace summary exists, do not restart onboarding. 先展示摘要并请代理人确认, mark uncertain fields `[待核实]`, ask only the missing deltas, and then route into the daily work entry.
- Workspace path rule: only suggest a private workspace path after institution and role are confirmed. Use `~/.insurance_copilot/agents/<institution-role-agent-id>/` for the private workspace family; keep Hermes skill installation under `~/.hermes/skills/insurance/insurance_copilot`.

Recommended Chinese three-question Quick Start:

1. **机构 / institution:** 你目前主要代表或服务哪家机构？例如：友邦/AIA、平安、中国人寿、太保、多家机构、暂不确定。You may answer `I don't know yet`.
2. **角色 / role:** 你现在的角色和权限是什么？例如：新人代理人、资深代理人、主管、培训/运营、只做资料整理、暂不确定。You may answer `I don't know yet`.
3. **市场与本周工作重点 / market and focus:** 你主要服务的地区、客户类型、沟通渠道和本周最想解决的事是什么？If unsure, use New Agent Default Mode and mark unknowns `[待核实]`.

After the three questions, produce a visually clear Chinese profile draft using `templates/practice-profile.md`, then show 3–5 next useful jobs instead of a full catalog.


## Output Location

Write the resulting profile only to a user-approved practice profile path, commonly:

`profiles/insurance_copilot-practice-profile.md`

If file access is unavailable or the user has not approved a destination, output a complete profile draft the user can save.

## New Agent Default Mode

Use **New Agent Default Mode** when the agent is new, unsure, cannot clearly state positioning, or asks to start quickly.

Behavior:

1. Acknowledge uncertainty as normal; do not make the agent define a complete positioning statement.
2. Ask no more than three onboarding questions before producing a provisional profile.
3. Every question must allow `I don't know yet` or `use conservative default`.
4. Generate a provisional profile using conservative insurance-assistant defaults.
5. Immediately show how the profile enables the next useful job: daily workbench, client notes, customer message, policy review, or compliance copy check.

Operational rule: ask no more than three onboarding questions before producing a provisional profile.

Recommended three questions:

1. **Market / jurisdiction:** Where do you mainly serve customers? Options: Hong Kong, Mainland China, Singapore, other, `I don't know yet`.
2. **Current work focus:** What are you mostly handling now? Options: family protection, medical/critical illness, savings/retirement, policy review, referrals, service/renewal, `I don't know yet`.
3. **Customer communication:** Where do you usually talk to customers? Options: WeChat, WhatsApp, phone, in-person, email, mixed, `I don't know yet`.

If the agent gives only one sentence such as “I am a new AIA agent serving Chinese-speaking families,” produce a provisional profile instead of asking a long questionnaire.

Default assumptions for New Agent Default Mode:

- Agent stage: new or unspecified; use conservative guidance.
- Institution: AIA/友邦 only if the agent says so; otherwise `[verify carrier/institution]`.
- Customer segment: Chinese-speaking family clients only if stated; otherwise general retail clients `[verify]`.
- Product posture: education, intake, policy organization, and review-ready drafts before product recommendations.
- Communication style: warm, low-pressure, plain-language, no fear tactics.
- Product facts: mark product, underwriting, claims, renewal, and payment facts `[verify]` unless source documents are supplied.
- Prohibited certainty: no guaranteed approval, payout, returns, savings, best, risk-free, or “everyone should buy” claims.
- Escalation: replacement/surrender/cancellation, claims disputes, health disclosure, vulnerable customers, investment-linked/returns language, complaints, and external sending.
- Customer data: use minimum necessary data, prefer de-identified notes, do not persist sensitive customer data without explicit destination approval.

## Quick Start vs Full Setup

Use **Quick Start** when the user needs to begin practical work in the same session. Ask only:

1. jurisdiction(s) and license/product scope;
2. carrier/product lines in scope;
3. compliance reviewer or approval role;
4. source hierarchy for product/policy facts;
5. external-message restrictions and forbidden phrases;
6. where private customer data may be stored, if anywhere.

Use **Full Setup** before production rollout or reusable customer-facing workflows. Full Setup should cover every section below and mark unknowns as `[confirm with compliance/legal]`.

Before the profile exists, downstream workflows must remain generic/provisional: education, intake, missing-fact checklists, neutral source organization, and internal drafts only.

## Interview Method

Ask only the questions needed for the user's situation. Do not interrogate unnecessarily. Start broad, then ask follow-ups for product lines or channels the agency actually uses.

Good onboarding questions:

- “Which market should I assume for now? You can say `I don't know yet` and I will mark it `[verify]`.”
- “Which customer conversations do you most want help with this week?”
- “Should I use a new-agent conservative mode where every customer-facing line is a draft for review?”

Avoid questions that require the agent to already know their mature positioning, such as:

- “Describe your full value proposition.”
- “Write your complete compliance policy.”
- “List every approved sales script and product boundary before we start.”

## Interview Sections

### 1. Agency Context

- Agency name and team structure.
- Jurisdictions served.
- License scope: life, health, P&C, annuity, investment-linked, group benefits, other.
- Distribution channel: in-person, phone, WeChat/WhatsApp, email, web leads, workplace seminars.
- CRM/tool status and where private agent workspace data may live.
- Languages used with customers.

### 2. Product Universe

- Carriers represented, including which public institution pack, if any, is relevant.
- Institution/public pack preference and whether public-only source use is required.
- Product lines in scope.
- Products excluded from AI assistance.
- Source hierarchy for product facts: policy contracts, rider docs, carrier portal, approved brochure, internal SOP.
- Whether cash-value, annuity, dividend, market-linked, or investment-oriented products are in scope.

### 3. Customer Segments

- Primary customer types: families, young professionals, retirees, business owners, high-net-worth, group clients.
- Vulnerable-customer rules.
- Languages and tone preferences.
- Channel restrictions and approval requirements.

### 4. Suitability Playbook

- Minimum facts required before recommendation.
- Budget rules.
- Replacement/surrender review rules.
- Health disclosure and underwriting rules.
- Claims-handling boundaries.
- Required comparison format.

### 5. Compliance Rules

- Approved script sources.
- Forbidden phrases.
- Required disclaimers.
- Approval workflow before sending externally.
- Escalation contacts or roles.
- Required forms and record-retention expectations.

### 6. Outputs

- Preferred formats for intake notes, product comparisons, customer scripts, manager summaries, and compliance flags.
- Required citation style.
- Where practice profiles and approved scripts should be stored.

## Output Format

```markdown
# Insurance Copilot Practice Profile

## Profile Status
- Mode: New Agent Default / Quick Start / Full Setup
- Confidence: provisional / reviewed / production-ready
- Last updated:
- Unknowns: [verify] items

## Agency Context
- Agency:
- Jurisdictions:
- License scope:
- Channels:
- Languages:

## Product Universe
- Carriers:
- Product lines:
- Excluded products:
- Source hierarchy:
- High-risk product lines:

## Customer Segments
- Primary segments:
- Vulnerable customer rules:
- Languages/tone:
- Channel restrictions:

## Suitability Playbook
- Minimum customer facts:
- Budget rules:
- Replacement/surrender rules:
- Health disclosure rules:
- Claims-handling boundaries:
- Comparison requirements:

## Compliance Rules
- Forbidden claims:
- Required disclaimers:
- Approval workflow:
- Escalation triggers:
- Required forms:
- Record retention:

## Output Formats
- Intake:
- Product-fit review:
- Customer script:
- Compliance check:
- Stakeholder summary:

## Next Useful Jobs
1. Daily Agent Workbench
2. Client Needs Intake
3. Compliance Copy Checker
```

## Profile Update Behavior

Treat the profile as dynamic. Update it when the agent corrects a default, adopts a new workflow, receives compliance feedback, or repeatedly uses the same scenario.

Examples:

- Agent says: “不要用太销售的语气。” → propose profile update: “Customer messages should be warm, low-pressure, and friend-like.”
- Agent says: “主管说不能说锁定收益。” → propose forbidden phrase update: “锁定收益,” with safer alternatives.
- Agent says: “我主要服务刚成家的家庭。” → propose customer-segment update.

Ask before persisting updates. If not persisting, include the update as a copyable patch in the response.

## Scenario and Eval Capture

Agents provide messy real-world context; AI converts it into structured scenarios. When an agent shares a recurring customer question, customer objection, unsafe draft, or compliance correction, offer to turn it into a scenario card.

The agent should not write tests or JSON. evals are internal quality fixtures; agents do not write JSON eval cases.

Agent-facing scenario card format:

```markdown
## Scenario
- Customer says:
- Agent goal:
- Risk level:
- What to verify:
- Draft response:
- Forbidden / risky phrases:
- Escalation triggers:
```

Maintainer-facing eval intent, if useful:

```markdown
## AI-generated eval intent
- must include:
- must not include:
- escalation expected:
- expected workflow:
```

Only maintainers or the repository automation convert eval intent into `evals/cases/*.json`.

## Completion Criteria

- The profile clearly says what the assistant may and may not do.
- It lists required facts before recommendations.
- It defines escalation gates and side-effect boundaries.
- It includes source hierarchy, citation expectations, privacy/data-handling expectations, and approval workflow.
- A new or unsure agent can start from New Agent Default Mode without manually filling a template.
- The output includes `Next Useful Jobs` so onboarding leads directly into daily work.

## Guardrails

- Do not invent agency rules; mark unknowns.
- Do not treat starter compliance text as jurisdiction-specific legal advice.
- Do not write sensitive customer data into the practice profile.
- If the user cannot answer compliance questions, create a draft profile with `[confirm with compliance/legal]` markers.
- Do not require full setup before providing safe internal drafts.
