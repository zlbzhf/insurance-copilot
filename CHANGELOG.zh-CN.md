# 更新日志

[English](CHANGELOG.md) · [README 中文版](README.zh-CN.md)

本文件记录 Insurance Copilot 项目的重要变更。

项目目前处于 pre-1.0 阶段，采用 milestone-based 版本记录方式。本文风格参考 [Keep a Changelog](https://keepachangelog.com/)，并在适合时使用语义化版本风格的里程碑。

## [未发布]

### Changed

- 更新 Coach_me runtime 架构：Insurance Copilot 现在使用独立 `coach_me` skill 作为通用动态追问转文档方法，`skills/insurance_copilot/references/coach-me.md` 和 `templates/coach-me.md` 仅作为保险领域 adapter/handoff；active runtime surfaces 不再保留固定三问 / 固定 Direction-Risk-Source-Action 合同。

### 新增

- 新增 Spec Lifecycle 治理、`docs/decisions/ADR-0001-gateway-agnostic-interactive-protocol.md` 和 `docs/archive/README.md`，要求已完成 implementation specs 删除、以无运行时权限归档，或压缩为 ADR，避免控制文档持续堆积。
- 新增 Coach_me Guided Reasoning Mode surfaces，用于宽泛、凌乱、策略性、依赖资料、客户场景或 product recommendation intent 的问题；当前 runtime 已改为由独立 `coach_me` 承担通用方法，Insurance Copilot 只保留保险领域 adapter。
- 新增中文 interactive onboarding 文档、示例、eval 和 validator 覆盖，保护 `/skill insurance_copilot`、机构/角色确认、`[待核实]` 解释，以及已有资料先摘要确认的行为。
- 新增 `docs/product-development-spec.md`，作为持久的产品开发事实来源和可用状态定义。
- 新增 `docs/reference-landscape.md`，用于把外部/参考项目映射到 project significance、implementation form、non-goals 和 priority。
- 新增 Professional Review Gate 工作流 reference、template、eval、example 和 validator 覆盖，使客户可见、受监管、外部使用或接近副作用的输出必须标明 action class、review owner、source verification status、customer-facing approval status、side-effect status、draft for licensed/compliance review、not approved to send、no external action is authorized 和 minimum safe next step。
- 新增 Institution Knowledge Organizer 运行时 reference/template/eval/validator 覆盖，并补强 AIA public pack 的 source-backed public pack update：source record、public/private boundary、`[verify]`、No customer data、not a final claims decision 和 pack maintainer review 均可验证。
- 新增 P1 客户权益影响场景 eval，将 Customer Advocacy Memo 与 Professional Review Gate 联动到 claims dispute、policy review found unclaimed benefit、renewal/lapse/reinstatement ambiguity 和 Chinese complaint/service-recovery talk tracks。
- 新增 Source Grounding and Data Boundary Gate 运行时 reference/template/evals/validator 覆盖，保护 Source Ledger、Citation Ledger、public/private separation、prompt-injection、PII minimization、citations or `[verify]`、no customer data in public packs、untrusted source text cannot override workflow instructions、manual-first practitioner workflow 和 not a generic RAG chatbot 行为。
- 新增 generic-first 架构保护：`tests/test_generic_first_architecture.py`、`evals/cases/institution-public-pack-source-backed-generic.json` 和 `evals/expected/institution-public-pack-source-backed-generic.md`。
- 新增 registry-driven 公共知识包验证脚本 `scripts/validate_all_knowledge_packs.py`，使 CI 验证所有已注册的 public institution packs，而不是只验证 AIA seed pack。

### 变更

- 将 Coach_me 一问一答规则从平台限定表述泛化为适用于任何 interactive conversational gateway：使用 one-question-at-a-time protocol、send only the next useful question in the current turn，并在适合时给出 recommended default answer。
- 将 product recommendation intent 路由到 Coach_me before Client Needs Intake，先动态澄清目标、风险和来源，再进入结构化 fact-find。
- 将 Coach_me 从追问机制升级为代理人工作流中心，把限制转化为产品状态：default safe draft mode、review-ready packet、confirmed persistence packet 和 external action handoff packet。
- 将仓库/产品 slug、可安装 Hermes 技能身份、Telegram 命令和私有工作区根路径统一到 Telegram 安全的 `insurance_copilot` 命名。
- 明确 Insurance Copilot 目前已经可作为 manual-first Hermes skill beta 使用，但还不是可直接用于 live automation、客户发送、CRM 写入、投保提交、理赔提交、保单变更、报价引擎或最终监管建议的生产系统。
- 将 Institution Knowledge Organizer 从 AIA-first 流程泛化为 `knowledge/institutions/<pack_id>/` 下的 pack-agnostic public institution pack 工作流；AIA/友邦 保留为当前 seed 示例，而不是通用运行时定义。
- 更新 README、中文 README、CI、contribution templates、intake templates 和 private workspace 默认值，使其使用 registry-driven 验证和通用机构占位符。

### 修复

- 修复已安装 `insurance_copilot` skill 与源码仓库之间的运行时漂移：将 skill 启动/无明确任务时先展示资料状态与工作入口、以及 gateway-agnostic Coach_me 一问一答追问轮，写入源码、eval、tests 和 validator。
- 修复本地开发者直接运行裸 `pytest` 时可能无法导入仓库辅助模块的问题；通过 repo-root `pythonpath` 配置，让 `pytest` 与 `python3 -m pytest` 行为一致。
- 修复旧的连字符技能安装指引可能导致 Telegram 命令/菜单漂移的问题；记录 Hermes 内部连字符 key 与 Telegram 下划线命令的映射，以及发布前清理旧 runtime 安装目录的步骤。
- 修复会让通用产品层看起来绑定 AIA 的过拟合表述和默认值。
- 修复验证覆盖，将通用 Institution Knowledge Organizer 行为与 AIA seed-pack 行为分开检查。

### 安全与合规

- 通过禁止通用模板默认使用 `institution: aia` 或 `default_institution_pack: aia`，强化 public/private separation。
- 保留 AIA seed-pack 的 source-backed 理赔检查，同时为未来公共机构知识包增加 pack-agnostic 保护。

## [0.1.0] - 2026-05-15

### 新增

- 新增面向持牌保险专业人士的 Hermes-first `insurance_copilot` skill package。
- 新增核心 umbrella skill：`skills/insurance_copilot/SKILL.md`，包含任务优先路由、安全边界、隐私规则、New Agent Default Mode、New Agent Coach Mode、客户优先倡导，以及 draft-only 操作安全规则。
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
