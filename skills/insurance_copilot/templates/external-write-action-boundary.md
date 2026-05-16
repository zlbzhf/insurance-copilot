# External Write Action Boundary Template

Use with `references/external-write-action-boundary.md` and `templates/external-write-action-boundary.md` whenever a request involves **write-capable integrations**, **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, **publication**, webhook dispatch, live scheduler creation, or another external side effect.

## External Write Action Boundary Gate

- Workflow:
- Requested external action:
- Integration class: write-capable integrations
- Boundary disposition: design-only; out of scope unless explicitly approved; no write-capable integration is enabled
- Authorization status: no external write tool is authorized
- Allowed work now: manual-first dry-run/read-only design memo, manual checklist, task export draft, pseudocode, and review packet only
- Forbidden live actions: CRM writes; customer sending; claims filing; application submission; policy changes; quote generation; carrier contact; publication; webhook dispatch; live scheduler creation
- Public/private data status:
- Source verification status:
- Review owners required before any future live step:
- Professional Review Gate handoff: required before customer-facing, regulated, external-use, or side-effect-adjacent output
- Minimum safe next step:

## Approval Prerequisites for Any Future Live Step

> Do not complete this section as “approved” unless the user separately requests the exact live side effect and supplies review evidence.

- Exact target / system / recipient / endpoint:
- Exact action to perform:
- Final content or data:
- Authority to act:
- Licensed/compliance review status:
- Privacy/security approval:
- Operations/business owner:
- Audit logging / retention / rollback / reconciliation plan:
- Remaining `[verify]` items:
- User confirmation phrase for this exact side effect:

## Allowed Design-Only Output

- dry-run/read-only plan:
- Manual checklist:
- Task export draft marked `do not import automatically`:
- Pseudocode/contract without credentials or production endpoints:
- Risks and blockers:

## Forbidden Output States

- Do not say CRM writes are enabled.
- Do not say customer sending is approved.
- Do not say claims filing is complete.
- Do not say application submission is complete.
- Do not say policy changes are complete.
- Do not say quote generation produced a binding or approved quote.
- Do not say carrier contact or publication occurred.
- Do not create webhooks, live schedulers, cron jobs, production API clients, or write-capable MCP tools from this template.
- Do not bypass Professional Review Gate.
