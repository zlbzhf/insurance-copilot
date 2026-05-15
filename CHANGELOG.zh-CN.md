# 更新日志

[English](CHANGELOG.md) · [README 中文版](README.zh-CN.md)

本文件记录 Insurance Copilot 项目的重要变更。

项目目前处于 pre-1.0 阶段，采用 milestone-based 版本记录方式。本文风格参考 [Keep a Changelog](https://keepachangelog.com/)，并在适合时使用语义化版本风格的里程碑。

## [未发布]

### 新增

- 预留给下一个版本的新功能。
- 新增 `docs/product-development-spec.md`，作为持久的产品开发事实来源和可用状态定义。
- 新增 `docs/reference-landscape.md`，用于把外部/参考项目映射到 project significance、implementation form、non-goals 和 priority。
- 新增 Professional Review Gate 工作流 reference、template、eval、example 和 validator 覆盖，使客户可见、受监管、外部使用或接近副作用的输出必须标明 action class、review owner、source verification status、customer-facing approval status、side-effect status、draft for licensed/compliance review、not approved to send、no external action is authorized 和 minimum safe next step。

### 变更

- 预留给 `0.1.0` 之后的变更。
- 明确 Insurance Copilot 目前已经可作为 manual-first Hermes skill beta 使用，但还不是可直接用于 live automation、客户发送、CRM 写入、投保提交、理赔提交、保单变更、报价引擎或最终监管建议的生产系统。

### 修复

- 预留给 `0.1.0` 之后的修复。

### 安全与合规

- 预留给 `0.1.0` 之后的隐私、操作安全或合规边界变更。

## [0.1.0] - 2026-05-15

### 新增

- 新增面向持牌保险专业人士的 Hermes-first `insurance-copilot` skill package。
- 新增核心 umbrella skill：`skills/insurance-copilot/SKILL.md`，包含任务优先路由、安全边界、隐私规则、New Agent Default Mode、New Agent Coach Mode、客户优先倡导，以及 draft-only 操作安全规则。
- 新增工作流 references，覆盖 agency playbook setup、daily workbench、client needs intake、coverage-gap drafting、client plan drafting、product-fit review、compliance copy checking、existing policy review、replacement/surrender suitability triage、claims support triage、renewal/lapse follow-up、objection response、referral asks、Chinese talk tracks、annuity/investment-linked caution review、stakeholder summaries 和 baseline compliance vocabulary。
- 新增输出 templates，覆盖 practice profiles、client intake、coverage-gap analysis、product-fit review、compliance checks、policy review、replacement/surrender triage、claims triage、renewal review、stakeholder summaries、objection responses、daily workbench output、client plan drafts、Chinese talk tracks、referral asks 和 customer advocacy memos。
- 新增 practical MVP 示例，包括首次会话 onboarding、agent-friendly New Agent Default Mode 和 customer-first advocacy 示例。
- 新增静态 eval fixtures 和 expected outputs，用于覆盖实际工作流行为、合规边界、客户安全草稿和系统性客户倡导场景。
- 新增确定性质量门：`scripts/validate_repo.py`、`scripts/package_skill.py --check`、`scripts/run_evals.py`、pytest 覆盖和 GitHub Actions validation。
- 新增连续性和治理文档：`AGENTS.md`、`ROADMAP.md`、`docs/continuity.md`、`docs/quality-gates.md` 和 `docs/release-checklist.md`。
- 新增 `docs/documentation-map.md`，用于区分用户文档、运行时 skill 文件、工作流 references、输出 templates、维护者治理、可执行 gates、知识包和可选自动化。
- 新增三层知识架构：公共通用工作流 skill、公共保险机构知识包、代理人私有知识工作区模板。
- 新增公共保险机构知识包基础设施，包括 `knowledge/registry.json`、公开 AIA/友邦 seed pack、`_template` pack、source-record templates、contribution templates、validation hooks 和公共知识治理文档。
- 新增证据驱动的公共知识维护标准，包括 source taxonomy、page type registry、quality policy、schema evolution governance、machine-readable schemas 和 prompt contracts。
- 新增确定性 ingestion gateway prototype，用于 staging classification、extraction、schema gaps、proposed pages、provenance 和 validation reports，并且不会自动合并生成内容。
- 新增代理人私有工作区模板，包括 workspace schema、index/log 结构、示例目录、验证脚本和隐私导向文档。
- 新增 read-only local connector slices，可从本地 Markdown/CSV workspace 生成 daily workbench。
- 新增 local renewal watcher 脚本、示例和 cron wrapper templates，用于未来内部提醒工作流。
- 新增 private workspace readiness checks 和 private dry-run deployment harness，保持只读并执行 No External Writes。
- 新增双语项目门面文件：`README.md`、`README.zh-CN.md`、`CHANGELOG.md` 和 `CHANGELOG.zh-CN.md`。

### 变更

- 将项目从 Claude-style/plugin-inspired prototype 重新定位为 Hermes-first standalone skill repository。
- 将用户入口从 schema、gateway、deployment 或 automation 关注点，重新聚焦到保险代理人的实际工作流。
- 将 **customer-first advocacy within compliance boundaries** 提升为核心产品原则。
- 强化“空洞中立不足以服务客户”的规则：中立表述必须配套证据请求、来源核查、下一步行动、客户安全话术和升级路径。
- 明确 `docs/` 本身不是运行时来源；行为改变必须通过 `SKILL.md`、references、templates、evals、tests 或 validators 变成 runtime-effective constraints。
- 明确 templates 和 eval JSON 是内部维护/运行时 artifacts，不是要求代理人手动填写的表单。
- 明确公共/私有数据边界：公共保险机构知识进入 `knowledge/institutions/`；客户数据和非公开材料应保存在公共仓库之外的私有工作区。
- 将可选 connector、watcher、cron 和 private dry-run flows 放在 Advanced / Later 定位之后，确保 manual-first MVP 仍是默认用户路径。

### 修复

- 修复项目主定位向 Claude plugin、slash-command plugin、web app 或 deployment platform 漂移的问题。
- 强化验证，防止 docs-only 退化、workflow references 缺失、templates 缺失、过时平台语言残留、安全短语缺失和 skill bundle 不完整。
- 增加回归覆盖，保护 practical onboarding、customer-first advocacy、New Agent Coach Mode 和 runtime-effective documentation gates。

### 安全与合规

- 新增针对健康、财务、理赔、受益人、缴费、联系方式和身份信息等敏感数据的隐私与数据最小化 guidance。
- 新增操作安全 guidance，要求客户可见草稿、不可逆操作、提交、保单变更、理赔提交、取消、退保、替换和具有约束力的陈述都必须接受持牌/合规复核。
- 新增公共/私有知识分离规则，避免客户数据或非公开机构材料进入公共仓库路径。
- 新增针对 examples、evals、public knowledge packs 和 workspace templates 的 PII-like fixture 扫描。
- 新增 local connector、renewal watcher、readiness 和 dry-run harness flows 的 read-only / No External Writes 约束。
- 新增 jurisdiction adaptation guidance，要求生产使用前进行机构/团队级合规和法律复核。
