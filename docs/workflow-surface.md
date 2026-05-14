# Practitioner Workflow Surface

Insurance Copilot should feel like a daily insurance practice assistant first and a knowledge-standard project second. Use this surface to route user requests into safe, reviewable job-style workflows.

All public examples must be synthetic or de-identified. Every customer-facing output is a draft for licensed/compliance review. Never send messages, submit applications, file claims, change policies, or write to CRM systems automatically.

## How to Use This Surface

1. Confirm a practice profile exists or run **Agency Playbook Builder** in Quick Start mode.
2. Choose the job-style workflow that matches the user's immediate task.
3. Ask only for missing facts needed for that workflow.
4. Produce a review-ready draft with `[verify]` markers where source facts are incomplete.
5. Name the human review owner before any customer-facing or external-use draft.

## Workflow 1: Agency Playbook Builder

- **When to use:** The agency/practice context is unknown, outdated, or too thin to support customer-facing work.
- **Required inputs:** Role/license scope, jurisdictions, carrier/product lines, approved script sources, compliance reviewer, escalation path, customer data policy, CRM/tool status, AIA/public pack preference, output style.
- **Output:** Practice profile draft or update using `skills/insurance-copilot/templates/practice-profile.md`.
- **Review owner:** Agency principal, licensed supervisor, compliance reviewer, or legal/compliance contact named in the profile.
- **Forbidden actions:** Inventing agency rules, storing sensitive customer data in the profile, treating starter language as jurisdiction-specific legal advice.
- **Standard prompt:**

```text
Use the Agency Playbook Builder. Help me create or update an Insurance Copilot practice profile. Start in Quick Start mode unless I ask for Full Setup. Ask only the essential missing questions first, mark unknowns as [confirm with compliance/legal], and do not draft customer-facing scripts yet.
```

## Workflow 2: Daily Agent Workbench

- **When to use:** The agent wants a daily operating plan across meetings, follow-ups, renewal/lapse risks, claims support, referrals, and compliance-sensitive drafts.
- **Required inputs:** Practice profile status, today's meetings, open follow-ups, renewal/lapse register or due-date notes, claim/support items, pending referrals, draft messages, source timestamps.
- **Output:** Prioritized daily workbench with high-risk items, customer follow-up drafts, verification checklist, and CRM/calendar task export draft.
- **Review owner:** Assigned agent for daily priorities; compliance reviewer for customer-facing drafts or high-risk items.
- **Forbidden actions:** Automatically sending outreach, making CRM/calendar writes, representing coverage status without carrier verification, bypassing escalation for lapse/replacement/claim issues.
- **Standard prompt:**

```text
Use the Daily Agent Workbench workflow for these synthetic daily notes. Separate today's priorities, high-risk items, customer follow-ups, draft talk tracks, verify-before-action items, and CRM/calendar task export drafts. Do not send or write anything automatically.
```

## Workflow 3: Client Needs Intake

- **When to use:** The user has messy notes, a transcript, a call summary, or a new client scenario and needs a structured fact-find before analysis.
- **Required inputs:** Customer/de-identified label, jurisdiction, age band, household/business obligations, income/budget, existing coverage, goals, communication channel, approved health-disclosure boundaries.
- **Output:** Intake summary with known facts, missing facts, completeness score, preliminary need areas, sensitivity flags, and next questions.
- **Review owner:** Licensed agent or supervisor responsible for fact-find quality.
- **Forbidden actions:** Recommending products from incomplete facts, collecting unnecessary sensitive data, coaching omission or softening of required disclosures.
- **Standard prompt:**

```text
Use Client Needs Intake. Turn these notes into a structured fact-find. Score completeness, separate known facts from missing facts, identify preliminary need areas, and say if product discussion is premature.
```

## Workflow 4: Coverage Gap Drafter

- **When to use:** Intake facts are sufficient to map risks and responsibilities to possible coverage gaps without selecting products.
- **Required inputs:** Completed or partial intake, existing policy/group benefit notes, household/business obligations, goals, budget range, jurisdiction/license scope.
- **Output:** Coverage gap analysis with priorities, assumptions, existing coverage notes, possible solution categories, and questions before recommendation.
- **Review owner:** Licensed agent; supervisor/compliance reviewer if vulnerable customer, complex product, or replacement risk appears.
- **Forbidden actions:** Naming specific products unless a separate product-fit workflow with sources is requested, using scare tactics, quantifying coverage amounts without methodology and facts.
- **Standard prompt:**

```text
Use Coverage Gap Drafter. Based on the intake, draft a coverage gap analysis. Use possible solution categories only, mark assumptions as [verify], and do not recommend a specific product.
```

## Workflow 5: Client Plan Draft

- **When to use:** The agent needs a review-ready proposal structure that combines intake, gap analysis, product/source facts, and compliance caveats.
- **Required inputs:** Practice profile or provisional assumptions, intake summary, gap analysis, candidate product categories or source-backed product facts, current coverage, budget/goals, jurisdiction, source hierarchy.
- **Output:** Client plan draft with customer profile, confirmed needs, missing facts, current coverage, gap summary, candidate solution categories, product/source caveats, compliance flags, customer-safe summary, internal notes, and next questions.
- **Review owner:** Licensed agent plus compliance reviewer before customer use.
- **Forbidden actions:** Final recommendations, unsupported product superiority, guarantee language, hiding internal risk flags from the agent copy, using unverified product facts without `[verify]`.
- **Standard prompt:**

```text
Use Client Plan Draft. Combine the intake, coverage-gap notes, and provided product/source facts into a review-ready client plan draft. Separate internal notes from customer-safe language, preserve [verify] markers, and avoid final advice or best/guaranteed wording.
```

## Workflow 6: Product Fit Reviewer

- **When to use:** The user provides product source material and asks whether it appears to fit documented customer needs.
- **Required inputs:** Customer intake or gap analysis, product source documents/facts, carrier/product version, jurisdiction/license scope, transaction type, budget, affected existing policies.
- **Output:** Product-fit review with rating, source caveats, need-feature mapping, cautions, replacement issues, questions before presenting, draft agent explanation, compliance flags.
- **Review owner:** Licensed agent; compliance/supervisor if product is complex, replacement-adjacent, investment-linked, or customer-facing.
- **Forbidden actions:** Calling a product best, guaranteeing approval/benefits/returns, relying on marketing facts as contract facts, ignoring replacement or surrender concerns.
- **Standard prompt:**

```text
Use Product Fit Reviewer. Review the provided product source against the documented customer needs. Use the source hierarchy, mark unverified product facts [verify against contract/carrier source], and produce draft support only, not final advice.
```

## Workflow 7: Compliance Copy Checker

- **When to use:** Any customer-facing message, script, ad, post, seminar line, renewal notice, objection response, or plan summary needs risk review.
- **Required inputs:** Draft copy, intended audience, channel, jurisdiction/product line if known, source facts, approved script source if available.
- **Output:** Green/Yellow/Red risk check, risky phrases, required fixes, safer replacement language, missing disclosures, escalation decision, clean draft if appropriate.
- **Review owner:** Compliance reviewer, supervisor, or licensed principal named in the practice profile.
- **Forbidden actions:** Marking content approved, removing necessary caveats, creating high-pressure or misleading urgency, treating output as legal/regulatory advice.
- **Standard prompt:**

```text
Use Compliance Copy Checker. Review this draft before customer use. Quote risky phrases, classify risk, suggest safer wording, list missing disclosures/source checks, and state who must review before use.
```

## Workflow 8: Policy Review Assistant

- **When to use:** The agent needs to summarize an existing policy before renewal, cross-sell, upsell, cancellation, surrender, replacement, reinstatement, or coverage discussion.
- **Required inputs:** Policy contract/schedule, riders, premium/payment history if available, in-force values where applicable, current customer needs, proposed new product if any.
- **Output:** Existing policy review with policy snapshot, benefits, limitations/exclusions, value/renewal details, fit against current needs, replacement cautions, missing documents, draft customer-friendly summary.
- **Review owner:** Licensed agent; supervisor/compliance for replacement/surrender/cancellation or unclear status.
- **Forbidden actions:** Stating coverage is active without current carrier verification, recommending cancellation/replacement without full comparison and escalation, final tax/legal conclusions.
- **Standard prompt:**

```text
Use Policy Review Assistant. Summarize this existing policy from the provided sources, mark missing pages or status as [verify], and include replacement/surrender cautions if any change is being considered.
```

## Workflow 9: Replacement Risk Triager

- **When to use:** Any conversation involves replacing, surrendering, cancelling, reducing, exchanging, or materially changing existing coverage.
- **Required inputs:** Existing policy review, proposed action/product, customer rationale, premiums, benefits/rights potentially lost, new underwriting/waiting/contestability risks, charges/loans/tax assumptions, jurisdiction forms.
- **Output:** Replacement/surrender triage memo with proposed action, rationale, lost benefits/rights, new risks, alternatives, required disclosures/forms/review, neutral customer explanation.
- **Review owner:** Licensed supervisor and compliance reviewer; legal/tax/investment professional when applicable.
- **Forbidden actions:** Recommending replacement or surrender, guaranteeing savings, minimizing lost rights or charges, proceeding without required disclosures and review.
- **Standard prompt:**

```text
Use Replacement Risk Triager. Treat this as high risk. Compare the existing and proposed coverage only at a triage level, list lost benefits and new risks, identify alternatives, and require licensed/compliance review before any recommendation.
```

## Workflow 10: Renewal/Lapse Follow-up Planner

- **When to use:** The agent needs follow-up planning for premium due dates, renewal windows, grace periods, lapse risk, reinstatement, or routine policy review scheduling.
- **Required inputs:** Renewal register/policy list, due dates, grace/lapse dates, carrier status source and timestamp, customer notes, communication history, approved outreach templates.
- **Output:** Urgent actions, upcoming reviews, verification checklist, internal next actions, draft customer outreach, escalation flags.
- **Review owner:** Assigned servicing agent; compliance/supervisor for lapse/reinstatement, vulnerable customer, complaint, or ambiguous status.
- **Forbidden actions:** Saying coverage is active without carrier verification, automatically sending outreach, using misleading urgency, promising reinstatement or claim outcomes.
- **Standard prompt:**

```text
Use Renewal/Lapse Follow-up Planner. Review this synthetic renewal register or due-date list, sort by deadline, mark carrier status [verify] where needed, draft internal next actions first, and provide customer outreach drafts only after review gates.
```

## Workflow 11: Claims Support Triage

- **When to use:** The agent is helping organize a possible claim, claim status question, document request, denial, appeal, or coverage question.
- **Required inputs:** Policy source, event/loss date, high-level event description, claim status, carrier claim instructions/correspondence, deadlines, required documents, jurisdiction if relevant.
- **Output:** Claims triage checklist with known facts, missing documents/deadlines, policy/carrier source points to verify, neutral customer service language, escalation flags.
- **Review owner:** Claims specialist/carrier claims team; licensed agent for service support; legal/compliance for disputes or complaints.
- **Forbidden actions:** Deciding coverage or payout, guaranteeing claim outcome, advising alteration of facts/documents, giving legal advice about disputes.
- **Standard prompt:**

```text
Use Claims Support Triage. Organize the claim-support information into known facts, missing documents/deadlines, source points to verify, neutral customer service language, and escalation flags. Do not decide coverage or payout.
```

## Workflow 12: Objection Response Drafter

- **When to use:** The agent needs a compliant, non-pressure response to a customer concern about price, need, timing, trust, underwriting, policy terms, or alternatives.
- **Required inputs:** Objection text, customer context, product/need context, channel, jurisdiction/product line if known, approved script source if available.
- **Output:** Empathetic objection response draft, facts to verify, forbidden phrases, escalation flags, optional follow-up questions.
- **Review owner:** Licensed agent; compliance reviewer for customer-facing reuse, complex products, replacement pressure, or vulnerable-customer concerns.
- **Forbidden actions:** High-pressure tactics, fear-based claims, guarantees, unapproved savings/performance claims, minimizing exclusions or underwriting disclosures.
- **Standard prompt:**

```text
Use Objection Response Drafter. Draft a respectful, low-pressure response to this customer objection. Keep it factual, include [verify] items, avoid guarantees or pressure, and flag anything needing compliance review.
```

## Workflow 13: Referral Ask Drafter

- **When to use:** The agent wants a low-pressure referral request, thank-you, or follow-up message that avoids misleading promises or exploiting vulnerable customers.
- **Required inputs:** Relationship context, channel, language/tone, whether the customer has an open claim/complaint/financial distress, approved script source if available, jurisdiction/channel restrictions.
- **Output:** Referral ask draft with soft opt-out language, no promised outcomes, no inducement language unless approved, verification items, escalation triggers.
- **Review owner:** Licensed agent; compliance reviewer if referral incentives, regulated marketing, vulnerable customer, or mass outreach is involved.
- **Forbidden actions:** Promising approval/savings/results, pressuring customers, using referral incentives not approved by compliance, exploiting claim/health/financial distress.
- **Standard prompt:**

```text
Use Referral Ask Drafter. Create a short, low-pressure referral request for this context. Include an easy opt-out, avoid promised outcomes or inducements, and list compliance checks before use.
```

## Workflow 14: Stakeholder Summary Writer

- **When to use:** The agent needs separate summaries for customer, agent, manager, compliance, or another stakeholder after analysis.
- **Required inputs:** Source analysis, intended audience, internal-only flags, customer-safe constraints, jurisdiction/product line if known, review status.
- **Output:** Audience-specific summary with internal notes separated from customer-safe wording, caveats, `[verify]` markers, next actions, escalation items.
- **Review owner:** The stakeholder owner for internal use; licensed/compliance reviewer for customer-facing versions.
- **Forbidden actions:** Leaking internal-only flags into customer copy, stripping required caveats, presenting draft analysis as approved final advice.
- **Standard prompt:**

```text
Use Stakeholder Summary Writer. Summarize this analysis for the specified audience. Separate internal and customer-safe versions, preserve [verify] markers, and list review gates before external use.
```

## Workflow 15: Institution Knowledge Organizer

- **When to use:** The user wants to organize public insurer/institution knowledge, create contribution bundles, or route a public source through the evidence-driven knowledge process.
- **Required inputs:** Public source metadata/URL or source package, institution/pack ID, source type if known, source date/version, allowed excerpts, target page or schema gap question.
- **Output:** Source-first contribution plan, staging checklist, possible page type, schema-gap note if needed, and reminders for public-only content and human review.
- **Review owner:** Pack maintainer or public knowledge reviewer; compliance/legal reviewer if source rights or regulated language are unclear.
- **Forbidden actions:** Adding non-public/customer/confidential materials to public packs, inventing schema fields from intuition, treating draft gateway output as canonical without validation and human review.
- **Standard prompt:**

```text
Use Institution Knowledge Organizer. Help me organize this public insurance source for a public institution knowledge pack. Keep it source-first, identify the source type/page type, note schema gaps instead of inventing fields, and do not include customer or non-public material.
```
