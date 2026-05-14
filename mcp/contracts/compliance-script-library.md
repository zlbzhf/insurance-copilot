# Compliance Script Library Connector Contract

This is a contract sketch for future MCP integration. It is not an implementation.

## Default Access

- Read-only by default.
- Least privilege.
- Audit every access.
- Do not expose secrets or unnecessary PII.

## Minimum Fields

- script id
- channel
- jurisdiction/product scope
- approved text
- required disclaimers
- forbidden modifications
- approval date
- review owner

## Failure Handling

- If source is unavailable, mark facts `[verify]`.
- If data is stale, include source timestamp and ask for updated source.
- If permissions are insufficient, do not work around access controls.

## Production Approval

Requires privacy, compliance, security, and business-owner approval before production use.
