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
