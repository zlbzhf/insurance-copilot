# Professional Review Gate

Use this reference when any Insurance Copilot workflow produces customer-facing language, regulated analysis, an external-use draft, a CRM/calendar/task export draft, or a user request that could create a side effect. It translates the `claude-for-legal` professional workflow/profile/review-gate discipline into insurance-agent work without copying source-product form.

This gate is a runtime workflow, not a legal disclaimer. It makes every review boundary explicit before the agent relies on an output.

Runtime files:

- `references/professional-review-gate.md`
- `templates/professional-review-gate.md`

## When to Use

Use the **Professional Review Gate**:

- before any customer-facing or external-use draft is treated as usable;
- at the end of Daily Agent Workbench, Client Plan Draft, Product Fit Reviewer, Policy Review Assistant, Replacement Risk Triager, Claims Support Triage, Renewal/Lapse Follow-up Planner, Referral Ask Drafter, Chinese Talk Tracks, and Stakeholder Summary Writer;
- whenever an output mentions underwriting, disclosure, claims, complaints, lapse, reinstatement, replacement, surrender, cancellation, investment-linked/annuity content, vulnerable customers, or public institution facts;
- whenever the user asks Hermes to send, file, submit, write to CRM/calendar, change a policy, or make a final decision.

Do not use it as a blocker for harmless internal brainstorming. For internal-only notes, give a lightweight gate row so the agent knows the output is not approved for customer use.

## Action Classes

Classify the output before finalizing it:

1. **Class 0 — Internal organization only.** Scheduling, note cleanup, learning, or internal prioritization. No customer-facing approval status is granted.
2. **Class 1 — Customer-facing draft.** WeChat/email/talk-track/customer summary. Must be labeled **draft for licensed/compliance review** and **not approved to send**.
3. **Class 2 — Regulated decision-support / customer-impacting advocacy.** Underwriting/disclosure, claim/review, complaint, lapse/reinstatement, replacement/surrender/cancellation, vulnerable customer, or investment-linked/annuity matter. Requires named review owner plus source verification status and often a customer advocacy memo.
4. **Class 3 — External side effect requested.** Sending, CRM/calendar write, application submission, claims filing, policy change, cancellation, surrender, replacement, reinstatement, publication, or binding representation. Default: **no external action is authorized**; prepare drafts and list prerequisites only.
5. **Class 4 — Prohibited final conclusion or misrepresentation.** Guarantee, final coverage/payout/approval/suitability/compliance/legal/tax/investment conclusion, or request to conceal/omit/reframe material facts. Refuse that part and provide the minimum safe next step.

## Method

1. Identify the workflow and action class.
2. State the **review owner** by role, or mark `[verify review owner]` if unknown.
3. State **source verification status**: verified source cited, partially verified, or `[verify]` missing source.
4. State **customer-facing approval status**: internal only, draft for licensed/compliance review, not approved to send, or explicitly approved by user-provided review evidence.
5. State **side-effect status**: no external action is authorized, draft-only, exact confirmed side effect pending review, or out-of-scope.
6. If the matter is customer-impacting, preserve customer-first advocacy: favorable facts, evidence checklist, good-faith arguments, compliance boundary, escalation path, and customer-safe language.
7. End with the **minimum safe next step** that advances service without unauthorized action.

## Output Format

Use this exact review block when the workflow has customer-facing, external-use, or regulated content:

```markdown
## Professional Review Gate
- Workflow:
- Action class:
- Review owner:
- Source verification status:
- Customer-facing approval status: draft for licensed/compliance review; not approved to send
- Side-effect status: no external action is authorized
- Customer-first advocacy status:
- Escalation path:
- Minimum safe next step:
```

For Class 3 side effects, include these additional prerequisites before any tool or integration action:

```markdown
## Side-Effect Prerequisites
- Exact target / system / recipient:
- Final content or data:
- Authority to act:
- Licensed/compliance review status:
- Confirmation phrase supplied by the user:
```

If any prerequisite is missing, do not perform the action.

## Integration with Existing Workflows

- **Daily Agent Workbench:** every customer follow-up and CRM/calendar task export draft ends with the gate.
- **Client Needs Intake / Client Plan Draft:** product discussion remains provisional until profile, facts, sources, and review owner are named.
- **Policy Review / Replacement / Renewal:** replacement, lapse, reinstatement, cancellation, surrender, or uncertain status defaults to Class 2 or Class 3.
- **Claims Support Triage:** develop customer-first advocacy and review routes without deciding coverage or payout.
- **Compliance Copy Checker / Chinese Talk Tracks / Referral Ask:** drafts are not approved to send unless a human review process is provided.
- **Institution Knowledge Organizer:** canonical pack updates require public-source evidence, validator pass, and pack maintainer review.

## Guardrails

- Do not collapse the gate into a generic disclaimer. It must name action class, review owner, source verification status, customer-facing approval status, side-effect status, and minimum safe next step.
- Do not say or imply the draft is approved to send.
- Do not say or imply a CRM/calendar/policy/claim/application action has happened unless the user explicitly authorized the exact side effect and tools actually performed it.
- Do not use review language to abandon the customer. Even when no external action is authorized, provide concrete evidence requests, source checks, escalation path, and customer-safe language.
- Do not copy source-product mechanics; the insurance implementation is a Hermes skill reference/template/eval/validator gate.
