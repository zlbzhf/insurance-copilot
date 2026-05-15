# Insurance Copilot｜保险代理人工作流助手

> 面向持牌保险专业人士的 Hermes-first 保险代理人工作流 Copilot。

[English](README.md) · [英文更新日志](CHANGELOG.md) · [中文更新日志](CHANGELOG.zh-CN.md)

---

## 项目概览

Insurance Copilot 是一个 **独立的 Hermes 技能型产品仓库**，面向保险代理人的真实工作流。它的运行时入口是可安装的 `insurance-copilot` skill，并由工作流参考、输出模板、静态评测用例、确定性验证器、公共保险机构知识包和代理人私有工作区模板共同支撑。

它借鉴了 `claude-for-legal` 的专业工作流组织方式，但最终产品不是 Claude plugin、不是 Web App、不是 CRM，也不是部署平台。它首先要成为一个在 Hermes 中可直接使用的保险代理人助手：帮助持牌保险专业人士把零散客户信息、会议记录、保单资料、理赔/续保问题和客户话术需求，整理成结构化、可复核、可继续跟进的工作成果。

核心定位：

- **运行时形态：** 位于 `skills/insurance-copilot/` 的 Hermes skill package。
- **目标用户：** 持牌保险代理人、团队主管、培训人员，以及公共保险知识包维护者。
- **使用模式：** manual-first 的专业助手；自动化能力必须放在明确审阅和授权之后。
- **数据边界：** 公共知识与客户/代理人私有数据严格分层。
- **质量模型：** 产品原则必须通过 skill、references、templates、evals、tests、validators 转化为运行时约束，而不能只停留在文档里。

## 产品理念

Insurance Copilot 的核心理念是：**在合规边界内，以客户利益为先进行专业支持**。

这意味着，助手要帮助代理人尽最大合法努力服务客户，而不是用空泛免责声明或“以保险公司审核为准”来替代服务。合规是服务的护栏，不是停止服务的借口。

不可妥协的产品原则：

- **客户优先服务：** 主动识别客户目标、有利事实、缺失证据、复核渠道和下一步行动。
- **反对空洞中立：** `the carrier decides`、`以保险公司审核为准`、`subject to review`、`actual results may vary` 等表述如果没有配套证据清单、来源核查、客户安全话术和升级路径，就是不充分的。
- **只输出草稿：** 所有面向客户的内容都必须是供持牌人员/合规人员复核的草稿。
- **不得误导或隐瞒：** 不协助隐瞒、淡化、遗漏、编造或重新包装重要事实。
- **不作最终决定：** 不提供具有约束力的保险、法律、税务、投资、核保、理赔、精算或合规结论。
- **降低代理人负担：** 代理人输入自然语言、笔记、文件或场景；AI 负责转化为结构化 profile、工作流草稿、场景卡和评测意图。

系统性服务规则：

```text
from idea to product principle to operating model to workflow to scenario matrix to eval
```

也就是：从一个具体想法或案例出发，抽象成产品原则，再进入运营模型、工作流、场景矩阵和评测用例，而不是只修补单个案例。

相关文档：

- `docs/customer-first-service-philosophy.md`
- `docs/customer-advocacy-operating-model.md`
- `docs/customer-service-scenario-matrix.md`

涉及客户权益影响的 advocacy memo 使用运行时模板：

```text
skills/insurance-copilot/templates/customer-advocacy-memo.md
```

## Practical MVP：代理人如何使用

Insurance Copilot 是 **workflow router，不是 menu bot**。代理人应该直接描述要完成的工作，Hermes 应该路由到对应保险工作流。只有在缺少必要事实时，才追问关键信息。

当前 MVP 刻意采用 **manual-first** 路线：

```text
practice profile -> task-specific workflow -> source/private facts -> review-ready draft -> licensed/compliance review
```

优先支持真实代理人日常工作，而不是一开始就上自动化和部署：

1. **建立 practice profile** — 通过少量引导问题或 New Agent Default Mode 生成初版 profile，再由代理人确认/修正。
2. **安排今日工作** — 整理会议、续保、理赔支持、转介绍、异议处理和跟进消息。
3. **整理客户笔记** — 把零散 notes、聊天记录或面谈内容转成结构化 fact-find 和缺失问题清单。
4. **审阅保单或保障场景** — 总结已知事实、潜在缺口、替换/断缴/理赔风险和需要核查的资料。
5. **起草客户消息** — 生成低压力、合规敏感的微信/邮件/话术草稿。
6. **检查高风险文案** — 标记保证性、最优性、零风险、施压、替换、理赔或投资相关风险语言。
7. **整理公共保险公司知识** — 将公开的 AIA/友邦或其他保险机构资料纳入公共知识包流程。

如果用户已经说明任务，助手不应该列出全部工作流，而应该直接路由，最多追问三个必要问题，并输出清晰标注的草稿。

不要要求代理人手动填写 profile 模板。模板是内部存储格式，不是用户表单。Agents provide messy real-world context; AI converts it into structured scenarios, profile updates, reusable examples, and eval intents. evals are internal quality fixtures; agents do not write JSON eval cases.

## 适用对象

Insurance Copilot 适用于：

- 需要整理客户工作的持牌保险代理人；
- 希望沉淀可复制服务流程的团队主管；
- 支持新人或忙碌代理人的培训人员；
- 需要更安全客户沟通草稿的合规敏感团队；
- 维护公共保险机构知识包的贡献者；
- 想把 Hermes-first domain copilot 产品化的开发者。

它不是面向消费者的直接保险建议产品，也不能替代持牌专业判断。

## 它能做什么

Insurance Copilot 可以帮助持牌保险专业人士生成结构化草稿，用于：

- agency playbook / practice profile setup；
- daily agent workbench planning；
- client needs intake；
- coverage-gap drafting；
- Client Plan Draft / client plan drafting；
- product-fit review from source-backed facts；
- customer message、objection、referral 草稿；
- compliance language screening；
- existing policy review；
- replacement/surrender suitability triage；
- claims support triage；
- renewal/lapse follow-up planning；
- Chinese talk tracks；
- stakeholder summaries；
- public institution knowledge-pack organization。

## 它不做什么

Insurance Copilot 不会：

- 提供具有约束力的保险、法律、税务、投资、核保、理赔、精算或合规决定；
- 保证核保、理赔、收益、节省、适配性或保障结果；
- 自动发送客户消息；
- 提交投保申请；
- 提交理赔；
- 取消、退保、替换、复效或变更保障；
- 在未经明确授权和审阅前创建 live scheduled jobs；
- 把客户私有数据写入公共仓库路径；
- 绕过保险公司、监管、主管、适当性、替换或合规审查。

所有客户可见输出都必须是供持牌/合规复核的草稿。

## 三层架构

Insurance Copilot 使用三层架构：

```text
Layer 1: General Public Workflow Skill
Layer 2: Public Institution Knowledge Packs
Layer 3: Agent Private Knowledge Workspace
```

### Layer 1 — 通用公共工作流 Skill

路径：

```text
skills/insurance-copilot/
```

用途：

- Hermes umbrella skill；
- 工作流路由器；
- 安全、隐私、操作边界；
- 可复用 references 和 templates；
- 面向保险代理人实际工作的运行时指令。

### Layer 2 — 公共保险机构知识包

路径：

```text
knowledge/institutions/
```

用途：

- 公开、可协作维护的保险公司/机构知识包；
- 公开来源记录和有来源支撑的摘要；
- Karpathy-style LLM wiki 页面；
- AIA/友邦 seed pack 和模板 pack；
- 通过 `knowledge/registry.json` 建立公共 registry。

公共知识包不得包含客户数据、非公开机构材料、代理人私有 notes、密钥或生产导出数据。

### Layer 3 — 代理人私有知识工作区

模板路径：

```text
agent-workspace-template/
```

建议私有位置：

```text
~/.insurance-copilot/agents/<agent-id>/
```

用途：

- 客户资料；
- 代理人私有 notes；
- 代理人持有的非公开机构材料；
- 续保登记表；
- 私有跟进计划；
- 本地只读 readiness 检查。

私有工作区内容应保留在本地/私有环境中，不应提交到公共仓库。

公共知识维护遵循证据驱动流程：

```text
public source -> intake -> gateway staging -> schema gaps/proposed pages -> review -> knowledge pack
```

完整设计见：

- `docs/architecture.md`
- `docs/evidence-driven-standards.md`

## 运行时约束链

本项目明确避免“只写文档但不影响助手行为”。

`docs/` 用于解释和维护，但 `docs/` 本身不是运行时来源。真正能约束助手行为的内容必须进入至少一个运行时或可执行检查面：

1. `skills/insurance-copilot/SKILL.md` — Hermes 加载的核心运行时 skill。
2. `skills/insurance-copilot/references/*.md` — 具体工作流开始前读取的 playbooks。
3. `skills/insurance-copilot/templates/*.md` — 直接塑造输出结构的模板。
4. `evals/cases/*.json` 和 `evals/expected/*.md` — 静态回归评测。
5. `scripts/validate_repo.py` 和 `tests/*.py` — 退化时会失败的可执行质量门。

文档用途地图位于：

```text
docs/documentation-map.md
```

它说明哪些文件是用户阅读、哪些是运行时约束、哪些是维护者治理、哪些是可执行 gate。

## 安装到 Hermes

请安装 **完整 skill 目录**，确保 `references/` 和 `templates/` 可用：

```bash
mkdir -p ~/.hermes/skills/insurance/insurance-copilot
cp -R skills/insurance-copilot/* ~/.hermes/skills/insurance/insurance-copilot/
```

然后开启新的 Hermes 会话并加载：

```text
/skill insurance-copilot
```

注意：如果只安装单个 `SKILL.md`，而 Hermes 版本没有自动获取 linked files，则 references/templates 不会可用。本项目默认安装完整目录。

## 安装后 Smoke Test

```bash
test -f ~/.hermes/skills/insurance/insurance-copilot/SKILL.md
test -f ~/.hermes/skills/insurance/insurance-copilot/references/client-needs-intake.md
test -f ~/.hermes/skills/insurance/insurance-copilot/templates/practice-profile.md
```

在 Hermes 中测试：

```text
/skill insurance-copilot
Use Agency Playbook Builder in New Agent Default Mode. Ask no more than three onboarding questions needed to create a practical provisional profile. If I answer `I don't know yet`, use conservative defaults.
```

## 推荐首次会话

安装 skill 后，建议使用：

```text
/skill insurance-copilot
Use Agency Playbook Builder in New Agent Default Mode. I am a new or busy insurance agent and I don't know yet how to define my full profile. Ask at most three simple questions, allow conservative defaults, generate a provisional practice profile, then show how I can use it for daily workbench, client intake, policy review, customer message drafting, and compliance copy checking. Manual-first only; do not discuss cron, deployment, or automation unless I ask.
```

然后使用任务优先的 prompts：

```text
Use Daily Agent Workbench. Here are today's notes: [paste meetings, renewals, claims, referrals, objections]. Prioritize my day, draft internal next actions, and provide customer-message drafts only for review.
```

```text
Use Client Needs Intake. Turn these client notes into a structured fact-find. Separate known facts, missing facts, preliminary need areas, and product-discussion blockers.
```

```text
Use Compliance Copy Checker. Review this WeChat draft before customer use. Quote risky phrases, suggest safer language, and say who must review it.
```

建议阅读：

- `docs/quickstart.md`
- `docs/workflow-surface.md`
- `docs/documentation-map.md`
- `examples/practical-mvp/agent-first-session.md`
- `examples/practical-mvp/agent-friendly-onboarding.md`
- `examples/practical-mvp/customer-first-advocacy.md`

## 示例工作流

### New Agent Default Mode

适用于新代理人、忙碌代理人或尚不确定自身定位的代理人。助手最多追问少量关键问题，允许回答 `I don't know yet`，使用保守默认值，用 `[verify]` 标记不确定信息，并生成临时 practice profile。

### Daily Agent Workbench

适用于代理人需要安排会议、续保、异议处理、转介绍或理赔支持工作。输出应区分内部行动项和客户安全话术。

### Client Needs Intake

适用于把客户笔记、聊天记录或面谈记录整理为结构化 fact-find。输出应区分已知事实、缺失事实、初步需求领域、产品讨论阻碍和下一步问题。

### Client Plan Draft

适用于已经有 intake 和来源支撑的产品事实后，生成可复核客户方案草稿。它不是最终推荐。

### Customer Advocacy Memo

适用于核保/告知、理赔/复核、服务、投诉、替换、断缴等客户权益相关场景，特别是空洞中立不足以服务客户时。运行时模板是 `skills/insurance-copilot/templates/customer-advocacy-memo.md`。

### Compliance Copy Checker

适用于客户文案发送前检查。它应引用风险短语、解释风险、给出更安全表达，并指出需要谁复核。

## 公共保险机构知识包

公共知识包路径：

```text
knowledge/institutions/
```

它们是公开、可协作维护的 Karpathy-style LLM wiki 知识库，可以包含公开来源记录、公开产品/服务摘要、概念、对比和查询页面。

不得包含客户数据、非公开机构材料、代理人私有 notes、密钥或生产导出。

参考：

- `docs/public-knowledge-packs.md`
- `docs/llm-wiki-method.md`
- `docs/evidence-driven-standards.md`
- `docs/github-knowledge-governance.md`
- `knowledge/registry.json`

## 代理人私有工作区

客户私有知识和非公开机构材料应放在公共仓库之外。可从以下模板开始：

```text
agent-workspace-template/
```

建议初始化：

```bash
mkdir -p ~/.insurance-copilot/agents/<agent-id>
cp -R agent-workspace-template/* ~/.insurance-copilot/agents/<agent-id>/
```

见 `docs/agent-private-knowledge.md`。

## Advanced / Later：本地连接器与 Watchers

这些工具不是 practical MVP 的入口。只有在 manual workflow 已经有价值并完成审阅后，才应使用它们。

### Local File Connector Slice

```bash
python3 scripts/local_file_connectors.py daily-workbench \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --format markdown
```

它读取本地 Markdown/CSV 文件并输出 Daily Agent Workbench bundle。会跳过 symlink 输入，显式输出文件必须位于 workspace 外部。它不会发送消息、更新 CRM/日历、联系保险公司、提交理赔、提交申请或变更保单。见 `docs/local-file-connectors.md`。

### Local Renewal Watcher Slice

```bash
python3 scripts/local_file_connectors.py daily-workbench \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --format json > /tmp/insurance-workbench-bundle.json

python3 scripts/renewal_watcher.py \
  --bundle /tmp/insurance-workbench-bundle.json \
  --as-of 2026-05-14 \
  --format markdown
```

它只输出内部提醒：`[verify]` carrier/payment 状态，不发送客户消息，不写入 CRM/日历，不得下保障、断缴、复效结论。见 `docs/local-renewal-watcher.md` 和 `cron/renewal-watcher-cookbook.md`。

### Script-only Renewal Watcher Cron Wrapper

为未来 Hermes `no_agent=True` watchdog 部署提供脚本包装模板：

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --mode always
```

cron 使用时，`--mode alert-only` 只打印需要审阅的内部提醒。空 stdout 表示静默/无提醒；非零退出表示 fail-loud 错误提醒。本仓库不会创建 live job。见 `docs/script-only-cron-wrapper.md` 和 `examples/cron/renewal-watcher-no-agent.md`。

### Private Workspace Readiness Gate

```bash
python3 scripts/private_workspace_readiness.py \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --format markdown
```

它检查结构、续保登记表新鲜度、PII-like fixture 风险、输出边界、留存/审计准备度。它只读、仅内部使用，并且不会创建 live cron job。见 `docs/private-workspace-readiness.md`。

### Private Dry-Run Deployment Harness

创建任何 live Hermes scheduled watcher 之前，应先运行完整 private dry-run harness：

```bash
python3 scripts/private_dry_run.py \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --out /tmp/insurance-copilot-dry-run
```

它把 readiness、connector bundle、renewal watcher output 和 script-only cron wrapper simulation 串联成一个诊断输出目录，包含 `manifest.json` 和 `deployment-checklist.md`。它保持只读，报告 `ready_for_scheduled_watcher`，记录 `live_cron_created: false`，并执行 No External Writes。见 `docs/private-dry-run-harness.md` 和 `examples/private-dry-run/`。

## 仓库结构

```text
skills/insurance-copilot/     Umbrella Hermes skill package
standards/                    公共知识标准和 schema evolution policy
schemas/                      intake/classification/extraction/gaps 机器可读 schemas
prompts/                      未来受控 LLM gateway 的 prompt contracts
intake/                       canonical processing 前的来源包模板
staging/                      人工审核合并前的 gateway 输出
knowledge/institutions/       公共保险机构 LLM wiki packs
agent-workspace-template/     代理人私有知识工作区模板
contributions/                公共贡献模板和流程文档
examples/                     合成样例和期望输出
evals/                        静态回归 fixtures 和 expected outputs
cron/                         Hermes cron 的计划工作流 recipes
mcp/                          可选 connector notes 和 contracts
docs/                         架构、隐私、操作安全、质量门
scripts/                      仓库验证、打包、评测、连接器、watcher helpers
AGENTS.md                     Hermes 项目指令
ROADMAP.md                    持久项目方向
README.md                     英文 README
CHANGELOG.md                  英文更新日志
```

## 开发验证

提交前运行完整本地质量门：

```bash
python3 scripts/validate_repo.py
python3 scripts/package_skill.py --check
python3 scripts/run_evals.py
python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia
python3 scripts/validate_agent_workspace.py agent-workspace-template --template
python3 scripts/ingest_gateway.py --help
python3 scripts/private_dry_run.py --workspace examples/local-connectors/synthetic-agent-workspace --as-of 2026-05-14 --out /tmp/insurance-copilot-dry-run --force || test $? -eq 1
python3 -m pytest tests/test_ingest_gateway.py tests/test_local_file_connectors.py tests/test_renewal_watcher.py tests/test_renewal_watcher_cron_wrapper.py tests/test_private_workspace_readiness.py tests/test_private_dry_run.py tests/test_practitioner_mvp_surface.py -q
```

CI 会在 push 和 pull request 上运行这些检查。

## 生产准备说明

连接生产数据或系统前，请先阅读：

- `docs/privacy-and-data-handling.md`
- `docs/action-safety.md`
- `docs/jurisdiction-adaptation.md`
- `mcp/README.md`

生产使用需要机构/团队级合规和法律复核、权威来源系统集成、访问控制、审计日志、留存规则和持牌人员监督。

## 贡献规范

贡献应保持 Hermes-first 架构和实用代理人工作流入口。

提交变更前：

- 不要把客户私有资料或非公开机构资料放入仓库；
- 行为改变不能只写在 docs 中，必须进入运行时约束或可执行质量门；
- 同步更新相关 references、templates、evals、tests、validators；
- 除非明确要求自动化，否则保持 manual-first MVP；
- 运行开发验证命令。

见 `CONTRIBUTING.md`、`SECURITY.md`、`docs/quality-gates.md` 和 `docs/release-checklist.md`。

## 许可证

MIT。见 `LICENSE`。
