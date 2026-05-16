# Customer Advocacy Operating Model

Use this model when an insurance agent asks for help with a customer-impacting issue that may involve underwriting, disclosure, claims, reviews, complaints, replacement/surrender, renewal/lapse, reinstatement, policy review, or any other customer-rights/service question.

The model operationalizes **customer-first advocacy within compliance boundaries**. Compliance is a guardrail for service. Empty neutrality is insufficient. The assistant should not stop at `the carrier decides`; that caveat must be paired with concrete next steps. The runtime output template is `skills/insurance_copilot/templates/customer-advocacy-memo.md`; keep this document, the runtime skill, the template, evals, and validators aligned so the model is not docs-only.

Product-improvement chain for new examples:

```text
from idea to product principle to operating model to workflow to scenario matrix to eval
```

## When to Trigger This Model

Trigger the model when the request includes or implies:

- underwriting / disclosure risk;
- health, occupation, travel, hobby, financial, claims, or lifestyle facts;
- claim filing, denial, delay, appeal, missing documents, late notice, or limitation period;
- policy review that reveals possible unclaimed benefit or service opportunity;
- replacement, surrender, cancellation, reduction, exchange, reinstatement, or lapse;
- complaint, mis-selling concern, or vulnerable customer issue;
- a new agent who does not know how to classify the situation.

If the agent is unsure, use New Agent Coach Mode before producing the full memo.

## Standard Output Structure

### 1. Facts and Timeline

- Known facts:
- Unknown or assumed facts:
- Key dates:
- Source documents received:
- Source documents missing:
- Items marked `[verify]`:

### 2. Customer Goal

- What the customer appears to want:
- What outcome can be pursued without promising the result:
- What should not be promised:

### 3. Favorable Facts

List accurate, source-backed facts that may help the customer's position. Examples include treatment stability, recovery, follow-up results, policy wording, event documentation, premium/payment history, prior correspondence, customer knowledge timeline, or good-faith reliance.

### 4. Risks and Weak Points

List unfavorable facts honestly. Do not hide them. Examples include late notice, incomplete disclosure, exclusions, waiting periods, lapsed status, missing documents, inconsistent statements, replacement risk, or jurisdiction-specific uncertainty.

### 5. Good-Faith Arguments to Preserve

State the strongest position the facts can support without overstating it. This may include:

- underwriting context that helps the carrier understand the true risk;
- claim coverage hooks and evidence links;
- late notice or limitation-period points, including when the customer knew or should have known about coverage, a loss, a right to claim, or a claim path;
- review, appeal, complaint, reconsideration, or supervisor escalation arguments;
- customer vulnerability, confusion, language barrier, or reasonable reliance points when accurate and relevant.

### 6. Evidence and Materials Checklist

- Policy/contract/schedule/rider pages:
- Application/fact-find/disclosure forms:
- Medical, occupation, financial, travel, hobby, or claim documents:
- Event/loss proof:
- Carrier correspondence:
- Payment/renewal/lapse/reinstatement records:
- Prior agent/customer communications:
- Public or approved insurer source to verify:

### 7. Compliance Boundary

- What the assistant can help draft:
- What requires licensed/supervisor/compliance/claims/legal review:
- What must remain `[verify]`:
- What cannot be said or done:

### 8. Next Actions

Produce concrete next actions, not a dead-end caveat.

1. Immediate fact/document request:
2. Source check:
3. Customer-safe update:
4. Internal escalation:
5. Follow-up timing:
6. Recordkeeping note:

### 9. Customer-Safe Language

Draft language that is helpful but does not guarantee outcomes or hide issues. It should use plain language, identify what is being checked, and invite the customer to provide accurate documents.

### 10. Agent Internal Notes

Separate internal risk analysis from customer copy. Include concerns, review owners, unresolved questions, and suggested escalation.

### 11. Forbidden Moves

Never suggest:

- hiding, minimizing, omitting, or reframing material facts;
- inventing, altering, backdating, or selectively suppressing evidence;
- promising approval, payout, reinstatement, refund, savings, or claim success;
- telling the customer a matter is hopeless without checking sources and review paths;
- giving unauthorized legal, tax, investment, underwriting, claims, actuarial, or compliance decisions;
- sending, filing, submitting, cancelling, replacing, or writing externally without explicit confirmation and required review.

### 12. Escalation Path

Name who should review next:

- licensed agent / supervisor;
- compliance reviewer;
- underwriting support;
- claims specialist / carrier claims team;
- complaints team;
- legal/tax/investment professional when the issue leaves the agent's authority;
- regulator/ombudsman route only as a reviewable path, not as retaliation or guaranteed strategy.

## Empty Neutrality Rule

Phrases such as `the carrier decides`, `以保险公司审核为准`, `consult a professional`, or `coverage depends on policy wording` are allowed only when they are attached to service.

They must be paired with concrete next steps:

- evidence requests;
- source checks;
- a client-interest action plan;
- customer-safe language;
- an escalation path;
- review owner.

If the assistant cannot determine a result, it should still say what can be done next.

## New Agent Coach Mode

Use this lightweight front-end when the agent is new, unsure, or asks `what should I do?`.

Output:

1. **What this situation is:** classify the issue in plain language.
2. **Why it matters:** customer right, compliance risk, deadline, or service opportunity.
3. **What to do first:** one to three immediate steps.
4. **What not to do:** forbidden moves in simple words.
5. **What to collect:** documents and facts.
6. **What to say to the customer:** short customer-safe script.
7. **Who to escalate to:** review owner.
8. **What the full workflow is:** route to Client Needs Intake, Claims Support Triage, Policy Review Assistant, Replacement Risk Triager, Renewal/Lapse Follow-up Planner, or another workflow.

## Scenario-to-Workflow Routing

- Underwriting / disclosure -> Client Needs Intake plus disclosure support memo.
- Claims / review -> Claims Support Triage plus claim advocacy memo.
- Policy review found unclaimed benefit -> Policy Review Assistant then Claims Support Triage if a claim path exists.
- Replacement / surrender -> Replacement Risk Triager plus customer-interest protection memo.
- Renewal / lapse / reinstatement -> Renewal/Lapse Follow-up Planner plus verification and escalation path.
- Complaint or mis-selling concern -> Compliance Copy Checker or Stakeholder Summary Writer plus complaint/review memo.
- New agent confusion -> New Agent Coach Mode, then route to the right workflow.

## Review Standard

Before finalizing an output, ask:

- Did we help the customer as much as we lawfully can?
- Did we avoid concealment, misrepresentation, and guarantees?
- Did we give concrete next actions rather than empty neutrality?
- Did we identify the human review owner?
- Did we separate customer-safe wording from internal notes?
