# 保险代理人助手项目实施计划

> **For Hermes:** 后续如进入复杂功能开发，可使用 subagent-driven-development skill 按任务执行。

**Goal:** 构建一个面向保险代理人的 AI 助手，先完成可本地运行的 MVP：客户需求采集、产品匹配建议、异议处理话术、合规免责声明和知识库检索占位。

**Architecture:** 采用前后端分离。后端使用 FastAPI 暴露 `/api/chat`、`/api/needs/analyze`、`/api/products/recommend`、`/api/objections/respond` 等接口；前端使用 Vite + React + TypeScript 提供单页工作台。首版先用规则引擎和本地 JSON/Markdown 知识库，后续再接入真实 LLM、向量数据库、CRM 和保险产品库。

**Tech Stack:** Python 3.13, FastAPI, Pydantic, Uvicorn, Node 24, Vite, React, TypeScript。

---

## MVP 范围

### 1. 用户画像与需求采集
- 输入：年龄、家庭角色、预算、已有保障、关注点、风险偏好。
- 输出：保障缺口、优先级、建议提问。

### 2. 产品推荐草案
- 基于本地样例产品库进行规则匹配。
- 输出推荐理由、适配场景、不适配提醒。
- 明确合规边界：只做辅助建议，不承诺收益，不替代持牌人员判断。

### 3. 异议处理话术
- 输入客户异议：贵、没必要、先考虑、信不过、已有保险等。
- 输出：共情、澄清问题、价值重述、下一步动作。

### 4. 知识库占位
- 使用 `data/knowledge/*.md` 放监管合规、产品术语、销售 SOP。
- 首版简单关键词检索，后续升级 RAG。

### 5. 前端工作台
- 左侧输入客户情况和问题。
- 右侧显示助手回复、推荐产品、合规提醒。

---

## Task 1: 初始化项目文件

**Objective:** 创建后端、前端、文档和样例数据目录。

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/main.py`
- Create: `frontend/package.json`
- Create: `docs/plans/insurance-agent-assistant-mvp.md`

**Verification:**
- `search_files("*", target="files", path="/root/insurance-agent-assistant")` 能看到目录结构。

## Task 2: 实现后端领域模型

**Objective:** 定义客户画像、需求分析、产品、推荐和聊天请求/响应模型。

**Files:**
- Create: `backend/app/schemas/domain.py`

**Verification:**
- `python3 -m compileall backend/app` 通过。

## Task 3: 添加本地产品与知识库样例

**Objective:** 提供可演示的产品库和合规知识库内容。

**Files:**
- Create: `data/products.json`
- Create: `data/knowledge/compliance.md`
- Create: `data/knowledge/sales_sop.md`

**Verification:**
- 后端启动后能读取数据。

## Task 4: 实现规则推荐服务

**Objective:** 用可解释规则生成保障缺口、推荐产品和异议处理话术。

**Files:**
- Create: `backend/app/services/recommendation.py`
- Create: `backend/app/services/objection.py`
- Create: `backend/app/services/knowledge.py`

**Verification:**
- 单元测试覆盖主要分支。

## Task 5: 实现 FastAPI 路由

**Objective:** 暴露 health、需求分析、产品推荐、异议处理和聊天 API。

**Files:**
- Create: `backend/app/api/routes.py`
- Modify: `backend/app/main.py`

**Verification:**
- `curl http://127.0.0.1:8000/health` 返回 `{"status":"ok"}`。

## Task 6: 实现 React MVP 页面

**Objective:** 提供一个可以填写客户情况并调用后端的工作台。

**Files:**
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/styles.css`
- Create: `frontend/index.html`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`

**Verification:**
- `npm run build` 通过。

## Task 7: 添加 README 和运行说明

**Objective:** 让项目可以被新开发者快速启动。

**Files:**
- Create: `README.md`

**Verification:**
- README 包含后端、前端启动命令和合规声明。
