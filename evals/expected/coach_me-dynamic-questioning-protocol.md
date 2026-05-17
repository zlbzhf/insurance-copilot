# Coach_me Dynamic Question Protocol — Expected Output

## Purpose

This expected output protects the **Coach_me Guided Reasoning Mode** behavior for a broad **product recommendation intent**, for example: “想给客户推荐保险产品，不知道怎么推荐.” The correct route is **Coach_me before Client Needs Intake** because the agent is asking how to think through a recommendation, not merely asking to format an intake form.

The runtime rule is gateway-agnostic: in any **interactive conversational gateway**, use the standalone **coach_me** skill to ask **one question at a time**. Coach_me is **not a fixed questionnaire**, **not a fixed question count**, and **not fixed categories**. Batch multiple questions only when the agent asks for an offline checklist.

## Runtime Contract

- Use the **source discovery order** before asking: current conversation, practice profile/defaults, workflow references, **public institution knowledge**, official supplied sources, **agent-private workspace**, **customer-specific materials**, then Q&A.
- Treat **Q&A intake is raw source input**; it does not override contracts, carrier status, compliance sources, or regulator guidance.
- Include **Source Grounding and Data Boundary Gate** when sources are mixed, citation-sensitive, public/private, connector-fed, or policy-document based.
- Include **Professional Review Gate** before any customer-facing, regulated, external-use, or side-effect-adjacent output.
- Preserve **no automatic persistence** unless the user approves destination and scope.

## Coach_me Working Document

### Why Coach_me Activated

- Workflow: **Coach_me Guided Reasoning Mode** using the **standalone Coach_me skill**.
- Trigger: product recommendation intent / 推荐保险产品, but customer facts, risk flags, sources, and immediate output goal are incomplete.
- Route: **Coach_me before Client Needs Intake**. After the direction is clear, Client Needs Intake can collect structured facts.

### Information Sufficiency

- Enough to proceed: partial.
- Source status: missing — no policy, product specification, approved script, or customer fact-find source has been reviewed.
- Safest next action: ask one focused dynamic question, then update the working document.

### Next Question If Continuing

你现在最需要我帮你形成哪一种输出？

A. 先判断“客户需求和缺口应该怎么梳理”  
B. 先准备一段客户沟通话术  
C. 先做产品匹配/不匹配的内部判断  
D. 先整理需要向客户补问的问题

- **Why this matters:** this decides whether the next step is needs intake, customer-safe language, product-fit review, or a review-ready packet.
- **Good answer format:** choose A/B/C/D, or describe the immediate meeting/task.
- **recommended default answer:** 如果你不确定，建议选 D；先补齐客户目标、家庭责任、预算、已有保障和健康/职业等核保相关事实，再进入产品匹配。

## Choice Point

Offer **answer now or continue questioning** after the answer. The assistant will **automatically stop questioning when information is sufficient**.

## Professional Review Gate

- Customer-facing approval status: draft for licensed/compliance review; not approved to send.
- Side-effect status: no external action is authorized.
- If the agent asks for an offline checklist, batching multiple questions is allowed; otherwise continue one question at a time.
