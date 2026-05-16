# Professional Review Gate Template / 专业复核关口模板

Use with `templates/professional-review-gate.md` whenever a workflow needs explicit review classification before customer-facing or external use. Source workflow reference: `references/professional-review-gate.md`.

默认使用中文输出；保留必要英文标签以便验证和审计。`[待核实]` / `[verify]` 表示来源、身份、保单、产品、付款、理赔、核保或合规事实尚未确认。含义：未复核前不能视为可发送、可提交、可变更或可作结论的事实。

## Professional Review Gate / 专业复核关口
- Workflow / 工作流:
- Action class / 动作类别:
- Review owner / 复核负责人:
- Source verification status / 来源核实状态:
- Customer-facing approval status / 客户发送状态：仅为草稿，需持牌/合规复核；尚未批准发送
- customer-facing approval status: draft for licensed/compliance review; not approved to send
- Side-effect status / 外部动作状态：未授权任何外部动作
- side-effect status: no external action is authorized
- Customer-first advocacy status / 客户利益支持状态:
- Escalation path / 升级路径:
- Minimum safe next step / 最小安全下一步:
- minimum safe next step:

## Side-Effect Prerequisites / 外部动作前置条件
Use only when the user requests sending, filing, submitting, CRM/calendar writing, policy change, cancellation, surrender, replacement, reinstatement, publication, or another external side effect.

- Exact target / system / recipient:
- Final content or data:
- Authority to act:
- Licensed/compliance review status:
- Confirmation phrase supplied by the user:

## Gate Checklist / 关口检查
- [ ] Action class is named.
- [ ] Review owner / 复核负责人 is named or marked `[待核实 review owner]` / `[verify review owner]`.
- [ ] Source verification status is explicit.
- [ ] customer-facing approval status says draft for licensed/compliance review unless actual review evidence is provided.
- [ ] Side-effect status says no external action is authorized unless exact side-effect prerequisites are satisfied.
- [ ] Customer-first advocacy did not stop at a neutral caveat.
- [ ] minimum safe next step / 最小安全下一步 is concrete and lawful.

## Forbidden Output States / 禁止输出状态
- Do not mark as approved to send by default.
- Do not omit the review owner.
- Do not omit source verification status.
- Do not omit side-effect status.
- Do not replace customer-first service with a disclaimer-only answer.
