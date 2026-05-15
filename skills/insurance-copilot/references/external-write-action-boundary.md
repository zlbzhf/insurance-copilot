# External Write Action Boundary

Use this reference whenever a user asks to design, enable, test, or execute **write-capable integrations**: **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, **publication**, webhook dispatch, live scheduler creation, or any tool that could change an external system.

Runtime files: `references/external-write-action-boundary.md` and `templates/external-write-action-boundary.md`.

## Product Posture

Insurance Copilot remains a **manual-first** Hermes skill. Write-capable production integrations are **design-only** and **out of scope unless explicitly approved**. In the default beta posture, **no write-capable integration is enabled** and **no external write tool is authorized**.

This gate translates reference-landscape connector and claims-workflow patterns into an insurance-agent action boundary without copying a CRM, claim-filing platform, quote engine, carrier portal robot, publication system, or live automation stack.

## When to Use

Apply the **External Write Action Boundary Gate** before or instead of any work that asks for:

- **CRM writes** or CRM/contact/opportunity/task/calendar updates;
- **customer sending** through email, SMS, WeChat, WhatsApp, social DM, mail merge, or platform posting;
- **claims filing**, claim appeal filing, carrier upload, or claim-status mutation;
- **application submission**, underwriting form submission, e-signature routing, or payment setup;
- **policy changes**, cancellation, surrender, replacement, reinstatement, beneficiary/owner/rider/premium/payment-method updates;
- **quote generation**, illustration generation, premium binding, or rate/benefit representations from a live engine;
- **carrier contact**, producer portal messaging, support-ticket creation, or regulator/ombudsman submission;
- **publication** of ads, social posts, seminar materials, websites, knowledge pages treated as approved public communications;
- any webhook, API token, browser automation, MCP server, scheduled watcher, or script that can write externally.

## Output Format

Use `templates/external-write-action-boundary.md` and include the **External Write Action Boundary Gate** before any design memo, checklist, task export draft, pseudocode, or review packet. The output must name the requested external action, classify it as **write-capable integrations**, state **design-only**, state **out of scope unless explicitly approved**, state **no write-capable integration is enabled**, state **no external write tool is authorized**, list the forbidden live action classes (**CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, and **publication**), keep allowed work **manual-first** and **dry-run/read-only**, and hand off to **Professional Review Gate**.

## Default Decision

If explicit approval is missing, output the gate and continue only with safe planning:

```markdown
## External Write Action Boundary Gate
- Requested external action:
- Integration class: write-capable integrations
- Boundary disposition: design-only; out of scope unless explicitly approved; no write-capable integration is enabled
- Authorization status: no external write tool is authorized
- Allowed work now: dry-run/read-only design memo, manual checklist, task export draft, pseudocode, and review packet only
- Forbidden live actions: CRM writes, customer sending, claims filing, application submission, policy changes, quote generation, carrier contact, publication, webhook dispatch, live scheduler creation
- Required review before future live step: licensed/compliance review, privacy/security approval, operations owner, business owner, audit/retention/rollback plan, exact target/action/data, and user confirmation
- Professional Review Gate handoff: required before any customer-facing, regulated, external-use, or side-effect-adjacent output
- Minimum safe next step:
```

## Allowed Outputs Without Separate Explicit Approval

- **dry-run/read-only** design memo that names systems, data classes, boundary assumptions, and reviewers.
- Manual checklist for a human agent to perform in approved systems.
- Draft task-export table or CRM/calendar update draft marked `do not import automatically`.
- Pseudocode or interface contract with fake endpoints, no credentials, no production tokens, no webhook secrets, and no live scheduler.
- Read-only connector/readiness review that also uses Private Workspace Trace and Readiness Gate when private data is involved.
- Source/citation review that also uses Source Grounding and Data Boundary Gate when source material is involved.

## Not Allowed Without Separate Explicit Approval

Do not:

- run tools that send, submit, file, write, update, publish, bind, quote, contact, mutate, or schedule live external work;
- create production credentials, API clients, webhooks, cron jobs, CI deployments, browser robots, or MCP servers that write;
- mark customer communications approved to send;
- treat a dry-run, readiness report, Professional Review Gate, or user enthusiasm as live-action authorization;
- transform manual-first drafts into live automation because a template exists.

## Guardrails

- Treat all **write-capable integrations** as **design-only** and **out of scope unless explicitly approved**.
- State **no write-capable integration is enabled** and **no external write tool is authorized** before any design details.
- Keep allowed work **manual-first** and **dry-run/read-only**.
- Refuse or redirect live **CRM writes**, **customer sending**, **claims filing**, **application submission**, **policy changes**, **quote generation**, **carrier contact**, **publication**, webhook dispatch, live scheduler creation, and write-capable MCP/API execution.
- Require **Professional Review Gate** for customer-facing, regulated, external-use, or side-effect-adjacent output.
- Do not treat source grounding, private workspace readiness, successful tests, or a design document as authorization for an external write.

## Future Approval Prerequisites

A future live write-capable integration requires a separate request and all of the following evidence before the assistant may even discuss execution steps:

1. Exact system, recipient, endpoint, environment, account, and action.
2. Final content/data to write, send, submit, file, quote, publish, or change.
3. Authority to act and licensed/compliance review status.
4. Privacy/security approval, least-privilege scope, secrets handling, audit logging, retention/deletion, reconciliation, rollback, and incident path.
5. Source status for customer, policy, claim, product, carrier, and compliance facts; unresolved items stay `[verify]`.
6. Human confirmation phrased for the exact side effect, not a generic “continue”.

## Relationship to Other Gates

- **Professional Review Gate** remains mandatory for customer-facing, regulated, external-use, or side-effect-adjacent outputs.
- **Source Grounding and Data Boundary Gate** applies when source material, citations, prompt-injection, public/private separation, or PII minimization are involved.
- **Private Workspace Trace and Readiness Gate** applies to read-only local/private workspace connectors, readiness gate dry-run reports, and audit-style trace review.
- This gate is stricter for external side effects: even if another gate passes, **no external write tool is authorized** unless a separate explicit approval process is satisfied.

## Minimum Safe Next Step Examples

- “I can prepare a design-only integration boundary memo and manual checklist; I will not enable CRM writes.”
- “I can draft the customer message for licensed/compliance review; I will not perform customer sending.”
- “I can organize the claim packet and source checklist; I will not perform claims filing.”
- “I can outline fields for an application submission review packet; I will not submit the application.”
- “I can draft a policy-change request checklist; I will not make policy changes.”
- “I can list quote assumptions and `[verify]` items; I will not perform quote generation or present it as binding.”
- “I can draft a carrier contact script; I will not contact the carrier.”
- “I can review publication copy; I will not publish it.”
