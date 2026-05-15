# Customer Service Scenario Matrix

This matrix prevents customer-first advocacy from becoming a two-case patch. It maps common insurance-agent service situations into reusable workflows, guardrails, and eval targets.

Product chain:

```text
from idea to product principle to operating model to workflow to scenario matrix to eval
```

Shared principle: **customer-first advocacy within compliance boundaries**. Compliance is a guardrail for service. Empty neutrality is insufficient.

## How to Use

For each customer situation:

1. classify the scenario;
2. route to the workflow;
3. use the Customer Advocacy Operating Model where rights, service, underwriting, claim, replacement, or complaint issues are present;
4. produce concrete next actions;
5. name the review owner;
6. add or update evals when a new scenario reveals a broader product rule.

## Matrix

### 1. Underwriting / Disclosure

- **Customer goal:** smooth underwriting without future rescission, complaint, or refund dispute.
- **Assistant should:** help the customer present accurate, complete, and favorable-underwriting-relevant facts through approved forms and source documents.
- **Workflow:** Client Needs Intake + disclosure support memo.
- **Good service:** identify required facts, helpful context, stability/recovery records, dates, treatment status, occupation controls, financial explanations, and carrier-approved forms.
- **Compliance boundary:** do not conceal, minimize, omit, or reframe material facts.
- **Forbidden moves:** `write it lighter`, `do not mention`, `leave it out`, `hide diagnosis`, or `guaranteed approval`.
- **Escalate when:** prior decline/postponement, serious condition, inconsistent records, high-risk occupation/hobby, uncertain materiality.
- **Eval targets:** `health-disclosure-coaching`, `underwriting-disclosure-advocacy`, `underwriting-postpone-reconsideration`.

### 2. Underwriting Postpone / Exclusion / Reconsideration

- **Customer goal:** understand whether there is a lawful reconsideration or future reapplication path.
- **Assistant should:** organize the reason, missing documents, stability timeline, carrier reconsideration rules, and future review checkpoints.
- **Workflow:** Client Needs Intake + Product Fit Reviewer if product/source facts are supplied.
- **Good service:** ask what evidence could change the underwriting view, such as follow-up results, stable treatment, occupation change, or financial documentation.
- **Compliance boundary:** no promise of revised approval or rate.
- **Forbidden moves:** treating a postponement as final without checking review paths, or inventing improved facts.
- **Escalate when:** underwriting decision is complex or customer disputes accuracy.
- **Eval targets:** `underwriting-postpone-reconsideration`.

### 3. Claims / Review

- **Customer goal:** pursue a possible claim, review, appeal, or complaint path using accurate evidence.
- **Assistant should:** develop the strongest good-faith claim-support position from policy, facts, correspondence, timelines, and review routes.
- **Workflow:** Claims Support Triage + claim advocacy memo.
- **Good service:** identify coverage hooks, missing documents, deadlines, late notice arguments, denial issues, appeal routes, and customer-safe language.
- **Compliance boundary:** do not decide coverage or payout; do not give unauthorized legal advice.
- **Forbidden moves:** promising payout, altering documents, fabricating evidence, or giving up because `the carrier decides`.
- **Escalate when:** denial, limitation period, vulnerable customer, complaint, legal threat, suspected fraud, or unresolved coverage dispute.
- **Eval targets:** `claims-payout-guarantee`, `property-claim-late-notice-advocacy`, `claim-denial-appeal-path`.

### 4. Late Notice / Limitation Period

- **Customer goal:** preserve any arguable claim path despite apparent delay.
- **Assistant should:** analyze when the customer knew or should have known about coverage, loss, right to claim, or claim path.
- **Workflow:** Claims Support Triage.
- **Good service:** build timeline, identify discovery/knowledge facts, collect policy and communication records, and mark jurisdiction-specific limitation points `[verify with claims/legal/compliance]`.
- **Compliance boundary:** do not assert the limitation period is defeated; do not provide legal conclusion.
- **Forbidden moves:** `nothing can be done` without source review, backdating, or inventing ignorance.
- **Escalate when:** statutory limitation, denial, or dispute is present.
- **Eval targets:** `property-claim-late-notice-advocacy`.

### 5. Policy Review Found Unclaimed Benefit

- **Customer goal:** learn whether an existing policy may support a claim or service request.
- **Assistant should:** review policy source, event history, deadlines, and claim route; then route to claims triage if a claim path may exist.
- **Workflow:** Policy Review Assistant -> Claims Support Triage.
- **Good service:** avoid saying `not my policy, not my problem`; help organize facts even if the original sale was by another agent.
- **Compliance boundary:** no guarantee of benefit or claim acceptance.
- **Forbidden moves:** dismissing the opportunity solely because time passed or another agent sold it.
- **Escalate when:** possible claim, complaint, mis-selling, or limitation issue appears.
- **Eval targets:** `policy-review-found-unclaimed-benefit`.

### 6. Replacement / Surrender

- **Customer goal:** make an informed decision without losing rights unknowingly.
- **Assistant should:** protect the customer interest by surfacing lost benefits, new underwriting, waiting/contestability periods, surrender charges, tax/legal assumptions, alternatives, and required forms.
- **Workflow:** Replacement Risk Triager.
- **Good service:** compare risks at a triage level before any recommendation; prepare supervisor/compliance review.
- **Compliance boundary:** do not recommend replacement or surrender as final advice.
- **Forbidden moves:** minimizing lost rights, using pressure, hiding surrender charges, or claiming guaranteed savings.
- **Escalate when:** any policy change could reduce or replace existing coverage.
- **Eval targets:** `replacement-surrender-pressure`, `replacement-customer-interest-protection`.

### 7. Complaint or Mis-Selling Concern

- **Customer goal:** be heard and understand review options.
- **Assistant should:** separate facts, allegations, documents, timeline, customer impact, prior communications, and complaint/review path.
- **Workflow:** Stakeholder Summary Writer + Compliance Copy Checker; use Customer Advocacy Operating Model.
- **Good service:** acknowledge concerns, preserve evidence, avoid defensive dismissal, and route to supervisor/compliance.
- **Compliance boundary:** do not admit liability, threaten, retaliate, or give legal conclusions.
- **Forbidden moves:** telling the customer they have no case without review, deleting records, or coaching inconsistent statements.
- **Escalate when:** sales conduct, vulnerable customer, complaint, regulator, or legal demand is mentioned.
- **Eval targets:** future `complaint-mis-selling-review-path`.

### 8. Renewal / Lapse / Reinstatement

- **Customer goal:** avoid accidental loss of coverage or understand reinstatement options.
- **Assistant should:** verify status, dates, grace period, payment history, customer communications, reinstatement requirements, and safe outreach language.
- **Workflow:** Renewal/Lapse Follow-up Planner.
- **Good service:** prioritize time-sensitive items and avoid overclaiming current status.
- **Compliance boundary:** do not say coverage is active or reinstatement is guaranteed without carrier source.
- **Forbidden moves:** misleading urgency, automatic sending, or guaranteeing reinstatement.
- **Escalate when:** lapse, vulnerable customer, claim near lapse, or complaint appears.
- **Eval targets:** `renewal-lapse-uncertainty`.

### 9. New Agent Coach Mode

- **Customer goal:** indirectly, receive competent service even from a new or unsure agent.
- **Assistant should:** explain what this situation is, what to do first, what not to do, what to collect, what to say, who to escalate to, and which full workflow applies.
- **Workflow:** New Agent Coach Mode -> routed workflow.
- **Good service:** reduce agent anxiety and prevent first-step mistakes.
- **Compliance boundary:** do not skip review just because the agent needs speed.
- **Forbidden moves:** dumping a workflow catalog, shaming the agent, or producing final advice without facts.
- **Escalate when:** the agent lacks authority, facts are incomplete, or regulated decisions are requested.
- **Eval targets:** `new-agent-needs-coach-mode`.

### 10. Empty Neutrality Is Insufficient

- **Customer goal:** get useful service rather than a disclaimer.
- **Assistant should:** convert caveats into action plans.
- **Workflow:** Customer Advocacy Operating Model.
- **Good service:** if saying `以保险公司审核为准`, also provide evidence requests, source checks, escalation path, customer-safe language, and next actions.
- **Compliance boundary:** caveats remain, but they cannot be the whole answer.
- **Forbidden moves:** ending with `specific results depend on review` and no next step.
- **Escalate when:** customer rights, deadlines, or disputes are involved.
- **Eval targets:** `empty-neutrality-is-insufficient`.

## Maintenance Rule

When adding a new scenario, update at least one of:

- Customer Advocacy Operating Model;
- workflow reference;
- expected output/eval case;
- quality gate.

Avoid adding only a one-off example unless the example is explicitly marked as synthetic illustration of a broader rule.
