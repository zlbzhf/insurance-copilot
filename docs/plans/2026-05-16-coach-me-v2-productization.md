# Coach_me v2 Productized Workflow Optimization Plan

> **Goal:** upgrade Coach_me from a follow-up-question feature into a productized insurance-agent workflow center.

## Product Thesis

**Coach_me v2 Productized Workflow** moves Insurance Copilot **from questioning feature to agent workbench center**. The point is not to ask more questions; the point is to convert a messy agent question into a reusable work item with source status, risk status, next action, review status, and a proposed knowledge-base backfeed.

The key design correction is: **limitations become product states**. Boundaries such as draft-only output, no automatic persistence, no customer sending, and no external writes should not feel like dead ends. They become explicit states in the workflow that tell the agent what can safely happen next.

This remains a **manual-first practitioner workflow** for licensed insurance professionals.

## Product Principle

Coach_me v2 treats uncertainty as workflow state, not failure.

The runtime rule is:

```text
messy question -> source discovery -> information sufficiency score -> three-question decision algorithm -> review-ready packet -> Backfeed Decision Packet
```

Core contract phrases that must remain runtime-effective:

- **Coach_me v2 Productized Workflow**
- **from questioning feature to agent workbench center**
- **capability ladder**
- **default safe draft mode**
- **review-ready packet**
- **confirmed persistence packet**
- **external action handoff packet**
- **information sufficiency score**
- **Direction / Risk / Source / Action**
- **three-question decision algorithm**
- **one direction question, one risk question, one action/source question**
- **limitations become product states**
- **Backfeed Decision Packet**
- **no automatic persistence is a product boundary, not a dead end**
- **manual-first practitioner workflow**

## Capability Ladder

The **capability ladder** replaces a flat “cannot do that” answer with a product state model:

1. **default safe draft mode**
   - Use when facts are incomplete or review has not happened.
   - Output: provisional working document, `[待核实]` facts, customer-safe draft only if needed.
   - Allowed: reasoning, checklist, source request, next action.
   - Not allowed: persistence, sending, filing, submission, CRM write, policy change.

2. **review-ready packet**
   - Use when the agent has enough facts for a licensed/supervisor/compliance review.
   - Output: source ledger, risk ledger, final answer document, customer-safe draft, professional review gate.
   - Allowed: handoff to human review.
   - Not allowed: treating the draft as approved to send.

3. **confirmed persistence packet**
   - Use when the user explicitly asks to update a private workspace, customer page, practice profile, or query page and confirms the destination/scope.
   - Output: exact proposed fields/pages, old/new facts, source status, redaction/privacy check.
   - Allowed: prepare or perform a local/private update only after explicit approval and destination confirmation.
   - Not allowed: public-pack updates containing customer/private facts.

4. **external action handoff packet**
   - Use when the next step may involve customer sending, CRM writes, claims filing, application submission, policy changes, quote generation, carrier contact, or publication.
   - Output: External Write Action Boundary Gate plus Side-Effect Prerequisites.
   - Allowed: manual handoff packet and exact prerequisites.
   - Not allowed: live external action unless all action-safety requirements are explicitly satisfied.

## Information Sufficiency Score

The **information sufficiency score** is a lightweight runtime assessment, not a mathematical guarantee.

Score dimensions:

- **Direction:** Do we know what decision/workflow is needed?
- **Risk:** Do we know whether replacement, claim, disclosure, vulnerable customer, complaint, investment-linked, deadline, or side-effect risk exists?
- **Source:** Do we know which sources support the material facts, or which facts remain `[待核实]`?
- **Action:** Do we know the next safe step for the agent?

Display shape:

```markdown
## Information Sufficiency Score
- Direction: sufficient / partial / missing — reason
- Risk: sufficient / partial / missing — reason
- Source: sufficient / partial / missing — reason
- Action: sufficient / partial / missing — reason
- Stop-or-ask decision: stop and draft / ask one more round / escalate
```

## Three-Question Decision Algorithm

The **three-question decision algorithm** makes each round practical. By default, ask **one direction question, one risk question, one action/source question**.

Use the **Direction / Risk / Source / Action** frame:

1. Direction question — identifies the workflow and the agent’s immediate decision.
2. Risk question — identifies compliance, customer-impacting, timing, replacement, claim, disclosure, or side-effect risk.
3. Action/source question — identifies the missing source, customer material, private workspace path, or next human action needed.

This preserves the earlier rule to **ask exactly three most precise and relevant questions**, but makes the three questions productized and repeatable.

## Working Output

Coach_me v2 should always produce or maintain a working artifact:

- Coach_me Working Document
- Source Ledger / Citation Ledger when applicable
- Information Sufficiency Score
- Question Round using Direction / Risk / Source / Action
- Capability Ladder State
- Final Answer Document when ready
- Backfeed Decision Packet
- Review Gates

## Backfeed Decision Packet

The **Backfeed Decision Packet** replaces vague “maybe update the knowledge base” language.

It must say:

- Candidate destination: practice profile / customer page / policy summary / claim tracker / renewal register / private institution note / query page / public-pack schema gap.
- Proposed update: exact short fact, note, or page title.
- Source basis: verified citation, Q&A raw input, or `[待核实]`.
- Privacy boundary: public / private / customer-specific / do not persist.
- Approval needed: user, workspace owner, supervisor/compliance, pack maintainer.
- Persistence status: **no automatic persistence is a product boundary, not a dead end**.

## Runtime Changes to Implement

1. Update `skills/insurance_copilot/references/coach-me.md` so Coach_me v2 is the runtime method, not only a question rule.
2. Update `skills/insurance_copilot/templates/coach-me.md` so outputs contain capability ladder, information sufficiency score, Direction / Risk / Source / Action questions, review-ready packet, and Backfeed Decision Packet.
3. Update `SKILL.md`, README surfaces, workflow surface, quality gates, product spec, eval README, and changelogs.
4. Add an eval case and expected output for Coach_me v2.
5. Add deterministic tests and validator coverage so v2 cannot regress into a passive questionnaire or disclaimer-only boundary.

## Acceptance Criteria

- Existing Coach_me v1 guarantees remain: one workflow, not two skills; source discovery order; exactly three focused questions; answer now or continue questioning; stop when sufficient; Q&A intake is raw source input; Karpathy-style backfeed; no automatic persistence.
- v2 adds product states, not just more caveats.
- Outputs tell the agent exactly what to do next.
- Customer-facing or regulated outputs remain draft for licensed/compliance review.
- The project validates through pytest, static evals, repository validator, package check, and knowledge/workspace validators.
