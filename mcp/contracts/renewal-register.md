# Renewal Register Connector Contract

This is a contract sketch for future MCP integration. It is not an implementation.

External Write Action Boundary: read-only by default; future write-capable integrations are design-only, no external write tool is authorized, and any live mutation is out of scope unless explicitly approved.

## Default Access

- Read-only by default.
- Least privilege.
- Audit every access.
- Do not expose secrets or unnecessary PII.

## Minimum Fields

- customer/policy reference
- carrier
- policy type
- premium due date
- grace period end
- renewal/review date
- status source
- assigned agent
- last contact date

## Failure Handling

- If source is unavailable, mark facts `[verify]`.
- If data is stale, include source timestamp and ask for updated source.
- If permissions are insufficient, do not work around access controls.

## Production Approval

Requires privacy, compliance, security, and business-owner approval before production use.

## External Write Action Boundary

- Read-only by default.
- Any future **write-capable integrations** use is **design-only** and **out of scope unless explicitly approved**.
- Default authorization: **no external write tool is authorized** and no production mutation is available from this contract.
- Live writes require separate privacy/security/compliance approval, exact target/action/data, audit/retention/rollback planning, and human confirmation.
