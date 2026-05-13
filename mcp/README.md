# Optional MCP / Data Connectors

Hermes MCP servers should be configured through Hermes, not by relying on Claude `.mcp.json` files.

Potential future connectors:

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

Never connect production customer data until privacy, access control, audit logging, and compliance review are in place.
