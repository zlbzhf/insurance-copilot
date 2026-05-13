# 保险代理人助手

面向保险代理人的 AI 工作台 MVP，帮助完成客户需求采集、保障缺口分析、产品推荐草案、异议处理话术和合规提醒。

## 合规边界

- 本项目只提供销售辅助和信息整理，不构成保险、投资、法律或税务建议。
- 输出内容必须由持牌保险从业人员复核后才能用于客户沟通。
- 不承诺收益，不夸大保障，不替代正式产品条款、费率表和投保规则。
- 真实部署前需要接入公司合规审查、日志审计、权限控制和敏感信息保护。

## 本地启动

### 后端

```bash
cd /root/insurance-agent-assistant/backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

健康检查：

```bash
curl http://127.0.0.1:8000/health
```

### 前端

```bash
cd /root/insurance-agent-assistant/frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

打开：`http://127.0.0.1:5173`

## API

- `GET /health`：健康检查
- `POST /api/needs/analyze`：客户保障缺口分析
- `POST /api/products/recommend`：产品推荐草案
- `POST /api/objections/respond`：异议处理话术
- `POST /api/chat`：综合助手回复

## 下一步

1. 接入真实保险产品库和条款结构化解析。
2. 增加向量知识库/RAG，沉淀合规、条款、销售 SOP。
3. 加入客户资料脱敏、权限、审计日志。
4. 接入 LLM，并为每类输出增加合规 guardrail。
5. 加入 CRM/企微/飞书等渠道集成。
