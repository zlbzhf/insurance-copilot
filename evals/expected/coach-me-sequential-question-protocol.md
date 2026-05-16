# Coach_me Sequential Question Protocol — Expected Output

## Purpose

This expected output protects the **Coach_me Guided Reasoning Mode** behavior for a broad product recommendation intent, for example: “想给客户推荐保险产品，不知道怎么推荐.” The correct route is **Coach_me before Client Needs Intake** because the agent is asking how to think through a recommendation, not merely asking to format an intake form.

The runtime rule is gateway-agnostic: in any **interactive conversational gateway**, use the **sequential question protocol**. Ask **one question at a time**, **send only the active question** in the **current turn**, and wait for the user answer before `Question 2/3` or `Question 3/3`. **Do not batch all three questions** unless the agent asks for an **offline checklist**.

## Runtime Contract

- Coach_me is **one workflow, not two skills**.
- Use the **source discovery order** before asking: current conversation, practice profile/defaults, workflow references, **public institution knowledge**, official supplied sources, **agent-private workspace**, **customer-specific materials**, then Q&A.
- Treat **Q&A intake is raw source input**; it does not override contracts, carrier status, compliance sources, or regulator guidance.
- Compute an **information sufficiency score** across Direction, Risk, Source, and Action before deciding whether to ask or draft.
- Include **Source Grounding and Data Boundary Gate** when sources are mixed, citation-sensitive, public/private, connector-fed, or policy-document based.
- Include **Professional Review Gate** before any customer-facing, regulated, external-use, or side-effect-adjacent output.
- End with a **Karpathy-style LLM wiki backfeed proposal** and **no automatic persistence** unless the user approves destination and scope.

## Coach_me Working Document

### Why Coach_me Activated

- Workflow: **Coach_me Guided Reasoning Mode**.
- Trigger: product recommendation intent / 推荐保险产品, but customer facts, risk flags, sources, and immediate output goal are incomplete.
- Route: **Coach_me before Client Needs Intake**. After the direction is clear, Client Needs Intake can collect structured facts.

### Information Sufficiency Score

- Direction: partial — the agent wants help recommending, but the intended output is unknown.
- Risk: missing — replacement, disclosure, vulnerable customer, budget pressure, and side-effect risk are `[待核实]`.
- Source: missing — no policy, product specification, approved script, or customer fact-find source has been reviewed.
- Action: partial — safe next action is one focused direction question, then continue the three-question round.

### Question Round — Direction / Risk / Source / Action

Protocol: **interactive conversational gateway** + **sequential question protocol**. The assistant should ask exactly three most precise and relevant questions across the round, but only one is active now.

### Question 1/3 — Direction question

你现在最需要我帮你形成哪一种输出？

A. 先判断“客户需求和缺口应该怎么梳理”  
B. 先准备一段客户沟通话术  
C. 先做产品匹配/不匹配的内部判断  
D. 先整理需要向客户补问的问题

- Why this matters: this decides whether the next step is needs intake, customer-safe language, product-fit review, or a review-ready packet.
- Good answer format: choose A/B/C/D, or describe the immediate meeting/task.
- recommended default answer: 如果你不确定，建议选 D；先补齐客户目标、家庭责任、预算、已有保障和健康/职业等核保相关事实，再进入产品匹配。

### Later questions, not sent in the current turn

- `Question 2/3` will be the Risk question after the agent answers Question 1/3.
- `Question 3/3` will be the Action/source question after the agent answers Question 2/3.

## Choice Point

After `Question 3/3`, offer **answer now or continue questioning**. The assistant will **automatically stop questioning when information is sufficient**.

## Professional Review Gate

- Customer-facing approval status: draft for licensed/compliance review; not approved to send.
- Side-effect status: no external action is authorized.
- If the agent asks for an offline checklist, batching the three questions is allowed; otherwise continue one question at a time.
