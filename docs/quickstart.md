# Quickstart

This guide shows a safe end-to-end Hermes workflow using synthetic data. Start with the practitioner workflow surface, not the standards pipeline.

## 1. Install and Load

Install the full skill directory:

```bash
mkdir -p ~/.hermes/skills/insurance/insurance-copilot
cp -R skills/insurance-copilot/* ~/.hermes/skills/insurance/insurance-copilot/
```

Start a new Hermes session and load:

```text
/skill insurance-copilot
```

## 2. Practice Profile Gate

Prompt:

```text
Use Agency Playbook Builder in Quick Start mode. Help me create an Insurance Copilot practice profile for a synthetic life/health insurance agency. Ask only the first essential questions and mark unknowns as [confirm with compliance/legal].
```

Expected behavior:

- asks about jurisdiction, license scope, product lines, carriers, approved script sources, compliance reviewer, escalation path, customer data policy, CRM/tool status, and output formats;
- does not invent agency rules;
- blocks specific product-fit conclusions, replacement suggestions, reusable customer scripts, and external-action drafts until adequate profile/context exists.

## 3. Daily Agent Workbench Loop

Prompt:

```text
Use Daily Agent Workbench for synthetic notes: one family-protection meeting today, one renewal due soon with carrier status unknown, one claim-support checklist, and one referral thank-you follow-up. Prioritize tasks and draft talk tracks, but do not send or write anything automatically.
```

Expected behavior:

- prioritizes high-risk renewal/lapse and claim items;
- marks policy/payment/claim facts `[verify]`;
- creates customer drafts only as licensed/compliance review drafts;
- creates a CRM/calendar task export draft without external writes.

## 4. Client Intake

Use the synthetic case:

```text
Use Client Needs Intake for this synthetic profile: Couple ages 35 and 34, two children, mortgage, employer health coverage, unknown life/disability coverage, wants family protection and education funding, budget unknown.
```

Expected behavior:

- returns known facts and missing facts;
- says product recommendation is premature;
- asks budget, income, existing coverage, jurisdiction, and approved health-disclosure questions.

## 5. Coverage Gap Drafter

Prompt:

```text
Use Coverage Gap Drafter. Based on the intake above, draft a coverage gap analysis. Do not recommend specific products.
```

Expected behavior:

- identifies possible life, income interruption/disability, critical illness/medical, accident, and education-funding needs where appropriate;
- separates facts from assumptions;
- uses possible solution categories, not product names.

## 6. Client Plan Draft

Prompt:

```text
Use Client Plan Draft. Combine the synthetic intake, coverage-gap notes, and only source-backed product/category facts into a review-ready client plan draft. Separate internal notes from customer-safe language, preserve [verify] markers, and avoid final advice or best/guaranteed wording.
```

Expected behavior:

- includes customer profile, confirmed needs, missing facts, current coverage, gap summary, candidate solution categories, product/source caveats, compliance flags, customer-safe summary, internal notes, and next questions;
- does not call any product best;
- does not guarantee approval, payout, returns, savings, or suitability.

## 7. Compliance Copy Checker

Prompt:

```text
Use Compliance Copy Checker. Check this draft ad: "Guaranteed approval and guaranteed payout. This is the best risk-free plan for every family."
```

Expected behavior:

- marks the risk Red;
- flags guaranteed approval, guaranteed payout, best, risk-free, and every family;
- provides safer draft language;
- requires compliance review.

## 8. Chinese Talk Track / Referral Draft

Prompt:

```text
Use Chinese Talk Tracks and Referral Ask Drafter. Draft a low-pressure WeChat policy-review invitation and a referral ask for synthetic customers. Include forbidden phrases, [verify] items, and escalation triggers.
```

Expected behavior:

- uses calm Chinese wording;
- includes opt-out language for referral ask;
- forbids promises, guarantees, pressure, unapproved incentives, and customer-list extraction;
- requires review before use.

## 9. Stakeholder Summary

Prompt:

```text
Use Stakeholder Summary Writer. Summarize the above for the agent and then provide a customer-safe version.
```

Expected behavior:

- keeps internal flags in the agent version;
- removes internal-only notes from customer version;
- preserves caveats and `[verify]` markers.

## Full Synthetic Demo

See `examples/end-to-end/family-protection-workflow.md` for the full synthetic loop.
