# Insurance Copilot Practice Profile / 保险执业画像

## Internal Storage Note

Never ask the agent to manually fill the profile template. The template is an internal storage format, not a user-facing form. Use Agency Playbook Builder, New Agent Default Mode, Quick Start, or Full Setup to generate this file from guided questions, defaults, and agent confirmation.

默认使用中文输出；专业术语可保留必要英文。`[待核实]` / `[verify]` 表示该事实尚未被当前保单、保险公司系统、核保/理赔/合规来源、主管或客户材料确认。含义：在客户发送、提交、变更、报价、理赔、替换或形成结论前必须复核，不能把它当成已确认事实。

## 1. 资料状态
- Profile Status / 资料状态:
- Mode: New Agent Default / Quick Start / Full Setup
- Confidence: provisional / reviewed / production-ready
- Last updated:
- Existing profile / 已有资料:
- Summary shown and confirmed? 先展示摘要并请代理人确认:
- Unknowns / [待核实] items:
- Minimum safe next step:

## 2. 执业身份确认
- Agency / 机构:
- Role / 角色:
- Role / license owner:
- Jurisdictions / 执业或服务地区:
- License scope / 牌照与产品权限:
- Institution/public pack preference:
- Agent-private workspace path, only after institution and role are confirmed: `~/.insurance-copilot/agents/<institution-role-agent-id>/`
- Identity notes: 不得默认机构；不得默认角色；如缺失，主动询问机构、主动询问角色，并标记 `[待核实]`。

## 3. 业务边界与产品范围
- Carriers / 保险公司或机构:
- Product lines / 产品线:
- Excluded products / 不处理或需人工接管的产品:
- High-risk product lines / 高风险表达或高风险产品:
- Source hierarchy / 来源优先级:
- Minimum facts before recommendation / 推荐前最低事实:
- Replacement/surrender rules / 替换、退保、减额、断缴规则:

## 4. 客户与服务场景
- Primary segments / 主要客户:
- Vulnerable customer rules / 易受影响客户规则:
- Channels / 沟通渠道:
- Languages/tone / 语言与语气:
- Daily jobs / 日常入口: Daily Agent Workbench, Client Needs Intake, Policy Review Assistant, customer-message drafting, Compliance Copy Checker, Replacement/Renewal/Claims triage, Referral Ask Drafter.
- Channel restrictions / 渠道限制:

## 5. 合规与升级规则
- Approved script sources / 已批准话术来源:
- Forbidden claims / 禁止说法:
- Required disclaimers / 必要提示:
- Approval workflow / 发送前审批流程:
- Escalation triggers / 升级触发:
- Required forms / 必要表单:
- Record retention / 留痕要求:
- Reviewer roles / 复核负责人:
- Claims-handling boundaries / 理赔边界:
- Customer data policy / 客户资料处理:

## 6. 输出偏好与下一步
- Intake / 客户需求收集:
- Coverage gap analysis / 缺口分析:
- Product-fit review / 产品匹配复核:
- Customer script / 客户话术:
- Compliance check / 合规检查:
- Stakeholder summary / 给主管或合规的摘要:
- Citation style / 引用方式:
- Next Useful Jobs / 下一步可做事项:
  1. Daily Agent Workbench / 今日工作台
  2. Client Needs Intake / 客户需求收集
  3. Policy Review Assistant / 保单检视
  4. Compliance Copy Checker / 话术合规检查
  5. Customer-safe draft language / 客户安全话术草稿

## Practice Profile Gate
- Allowed before profile exists: generic education, intake, missing-fact checklists, neutral source organization, provisional internal drafts.
- Block before profile/context exists: specific product-fit conclusions, replacement suggestions, reusable customer scripts, external-action drafts, jurisdiction-specific compliance conclusions.
- Default label for incomplete context: provisional draft for licensed/compliance review; not approved to send.
- If profile exists: 已有资料 must be summarized first, then 先展示摘要并请代理人确认 before reuse.
