# Optional MCP / Data Connectors

Hermes MCP servers should be configured through Hermes, not by relying on Claude `.mcp.json` files.

Potential connectors:

- CRM/customer fact source;
- policy document knowledge base;
- approved product specification library;
- compliance-approved script library;
- renewal register source.

Configure with Hermes commands such as:

```bash
hermes mcp add <name> --command '<server command>'
hermes mcp test <name>
hermes mcp list
```

## Production Preconditions

Do not connect production customer data until all are defined and approved:

- least-privilege access;
- read-only default mode;
- secrets storage outside the repo;
- audit logging;
- retention/deletion rules;
- compliance/legal approval;
- incident reporting path;
- clear source hierarchy and stale-data handling.

## Connector Contracts

Contract sketches live in `mcp/contracts/`:

- `crm-customer-facts.md`
- `policy-document-kb.md`
- `product-library.md`
- `compliance-script-library.md`
- `renewal-register.md`


## Local File Connector Bridge

Before production MCP/data connectors exist, use the read-only local-file connector slice:

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format markdown
```

This is not an MCP server and does not call external systems. It provides a safe bridge between private workspace files and the Daily Agent Workbench workflow while preserving the same safety posture expected from future production connectors: read-only by default, source-aware, `[verify]` on uncertain facts, and no external side effects.

## External Write Action Boundary Gate

MCP connector notes are **manual-first** and **dry-run/read-only** unless separately approved. Any **write-capable integrations** request involving **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, **publication**, webhook dispatch, or live scheduler creation must use **External Write Action Boundary Gate**: **design-only**, **out of scope unless explicitly approved**, **no write-capable integration is enabled**, **no external write tool is authorized**, and **Professional Review Gate** handoff before any customer-facing, regulated, external-use, or side-effect-adjacent output.
