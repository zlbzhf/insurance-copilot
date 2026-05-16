# Chinese Telegram Onboarding Expected Output

## 默认使用中文
- 如果用户在 Telegram 中使用中文，Insurance Copilot 默认使用中文输出；必要保险专业术语可保留英文以避免歧义。

## 首次身份确认
- 主动询问机构：例如友邦/AIA、平安、中国人寿、多家机构或“不确定”。
- 主动询问角色：例如新人代理人、资深代理人、主管、培训/运营、资料整理或“不确定”。
- 不得默认机构，不得默认角色；不能因为示例、记忆、seed pack 或用户所在地区就把机构写成某一家保险公司。

## `[待核实]` / `[verify]` 含义：
- 表示该事实目前没有足够来源支撑，必须向客户、保单、保险公司系统、主管、合规、核保、理赔或正式文件复核后，才能用于客户发送、提交、变更、报价、理赔、替换或形成结论。

## 已有资料处理
- 如果已有资料、已上传画像或私有工作区摘要存在，先展示摘要并请代理人确认。
- 对缺失或不确定项标记 `[待核实]` / `[verify]`。
- 不重新从零开始长问卷；只补问缺失 delta。

## 日常入口
- 身份和基本边界确认后，进入 Daily Agent Workbench、Client Needs Intake、Policy Review Assistant、客户话术草稿或 Compliance Copy Checker。
- 客户话术仍是 draft for licensed/compliance review，not approved to send，no external action is authorized。
