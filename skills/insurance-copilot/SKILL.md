---
name: insurance-copilot
description: Use when assisting licensed insurance professionals with client intake, coverage-gap analysis, product-fit review, policy review, renewal follow-up, compliant sales scripts, or agency playbook setup. Produces drafts for human review; never gives binding insurance, legal, tax, investment, underwriting, claims, or compliance decisions.
version: 0.1.0
author: Insurance Copilot Project
license: MIT
metadata:
  hermes:
    tags: [insurance, sales-assistant, compliance, client-intake, policy-review]
    related_skills: []
---

# Insurance Copilot

## Overview

Insurance Copilot is a Hermes-first skill for helping licensed insurance professionals draft, organize, and quality-check insurance workflow outputs. It is inspired by the workflow discipline of `claude-for-legal`, but it is packaged for Hermes as one umbrella skill with linked references, templates, and validation scripts.

This skill does **not** turn Hermes into a licensed insurance advisor. Every result is a draft for review by the user's licensed insurance agent, supervisor, compliance team, legal counsel, tax advisor, or other qualified professional as appropriate.

## When to Use

Use this skill when the user asks for help with:

- learning or documenting an insurance agency playbook;
- structuring a client fact-find or needs intake;
- identifying possible coverage gaps from known facts;
- comparing a product to known customer needs;
- drafting compliant responses to customer objections;
- checking customer-facing language for risky insurance claims;
- summarizing existing policies before cross-sell, upsell, renewal, cancellation, surrender, or replacement;
- reviewing renewal/lapse/payment follow-up windows;
- converting detailed analysis into customer, agent, manager, or compliance summaries.

Do **not** use this skill to:

- make final recommendations without adequate client facts and source documents;
- provide binding legal, tax, investment, underwriting, claims, actuarial, or compliance decisions;
- guarantee approval, payout, returns, savings, or coverage outcomes;
- advise anyone to conceal, minimize, or omit health, financial, occupational, lifestyle, or claims information;
- bypass required carrier, regulator, supervisor, or compliance review.

## Non-Negotiable Boundary

Every output must be framed as a draft for licensed human review. Do not say or imply:

- guaranteed approval, guaranteed payout, guaranteed returns, or risk-free outcomes;
- a product is objectively "best" without scoped assumptions and alternatives;
- marketing summaries override formal policy contracts, riders, exclusions, carrier underwriting rules, or regulator guidance;
- replacement, surrender, cancellation, or coverage change is appropriate without a documented suitability/replacement analysis.

For irreversible actions — sending customer communications, submitting applications, changing coverage, cancelling, surrendering, replacing, filing claims, or making binding representations — ask for explicit human confirmation and remind the user that licensed/compliance review is required.

## First Step: Practice Profile

If the agency/practice context is unknown, start with `references/cold-start-interview.md` and produce or update a practice profile. Store it in the current project or user-provided location, commonly:

```text
profiles/insurance-copilot-practice-profile.md
```

If file writing is not appropriate, output the complete profile draft for the user to save.

The practice profile should define:

- jurisdictions served;
- license scope and product lines;
- carrier/product source hierarchy;
- customer segments and vulnerable-customer rules;
- minimum facts before recommendation;
- replacement/surrender rules;
- required disclaimers and forbidden phrases;
- approval workflow and escalation roles;
- preferred output formats and citation style.

## Workflow Router

Choose the linked reference that matches the user's task:

- **Agency setup / playbook:** `references/cold-start-interview.md`
- **Client fact-find:** `references/client-needs-intake.md`
- **Coverage needs:** `references/coverage-gap-analysis.md`
- **Product suitability draft:** `references/product-fit-review.md`
- **Objection handling:** `references/objection-response.md`
- **Compliance review:** `references/compliance-check.md`
- **Existing policy review:** `references/policy-review.md`
- **Renewal/lapse workflow:** `references/renewal-review.md`
- **Audience-specific summary:** `references/stakeholder-summary.md`
- **Baseline compliance vocabulary:** `references/compliance-starter.md`
- **Default conservative profile:** `references/default-practice-profile.md`

When several workflows apply, run them in this order:

1. Practice profile / jurisdiction / license context.
2. Client facts and source collection.
3. Needs or policy analysis.
4. Product-fit or replacement review.
5. Compliance check.
6. Stakeholder/customer summary.

## Required Output Style

For customer-facing drafts include:

```markdown
## Purpose
- ...

## Known Facts
- ...

## Assumptions / Verify
- ...

## Draft Language
...

## Compliance Flags
- ...

## Next Questions
1. ...
```

For analytical work include:

```markdown
## Scope
- Task:
- Jurisdiction/license context:
- Sources reviewed:

## Findings
- ...

## Gaps / Missing Sources
- ...

## Draft Recommendation Support, Not Final Advice
- ...

## Compliance / Escalation Flags
- ...

## Next Actions
1. ...
```

Use source file names, section/page references, or `[verify]` markers whenever live source verification is missing.

## Source Hierarchy

When sources conflict, prefer in this order:

1. Current policy contract and rider/endorsement language.
2. Carrier underwriting guide and product specification.
3. Approved compliance/sales script.
4. Official regulator guidance.
5. Internal SOP / practice profile.
6. Marketing brochure, illustration, seminar material, or informal note.

If only lower-tier sources are available, explicitly mark product facts as `[verify against contract/carrier source]`.

## Escalation Triggers

Escalate or require licensed/compliance review when any of these appear:

- replacement, surrender, cancellation, rebating, twisting/churning, or high-pressure sales risk;
- elderly, vulnerable, low-literacy, distressed, or unusually dependent customer;
- tax, legal, investment, estate, or claims advice request;
- investment-linked, market-sensitive, cash-value, annuity, dividend, or projection language;
- health disclosures, underwriting exceptions, complaints, claims, exclusions, or cancellation deadlines;
- absolute claims, unapproved performance claims, or missing material limitations;
- conflict between customer goals, budget, existing coverage, and proposed product.

## Hermes Usage Notes

- Load with `/skill insurance-copilot` or install this repository's skill into `~/.hermes/skills/insurance/insurance-copilot`.
- In repo development, keep skill-supporting files under `references/`, `templates/`, `scripts/`, or `assets/`.
- Do not rely on Claude plugin metadata, `CLAUDE.md`, or Claude slash command packaging; this repo is Hermes-first.
- Use Hermes tools for file/source review when the user provides documents. Never invent policy details absent from sources.

## Common Pitfalls

1. **Jumping to a product too early.** If required client facts are missing, ask questions first.
2. **Overstating certainty.** Use `[verify]` for unconfirmed policy, rate, underwriting, or regulatory details.
3. **Collapsing needs analysis into recommendation.** Keep needs, product features, suitability, and final recommendation separate.
4. **Ignoring replacement risk.** Any cancellation/surrender/replacement path needs a documented comparison and escalation.
5. **Producing customer copy without compliance review.** Label as draft and list review flags.
6. **Using Claude plugin conventions.** Hermes uses skills; keep the install path and docs Hermes-native.

## Verification Checklist

- [ ] Practice profile or conservative defaults applied.
- [ ] Jurisdiction/license/product scope identified or marked unknown.
- [ ] Required facts and missing facts separated.
- [ ] Source hierarchy respected with citations or `[verify]` markers.
- [ ] Compliance and escalation flags included.
- [ ] Customer-facing output is labeled as draft language.
- [ ] No guarantees, concealed-disclosure advice, or unsupported product superiority claims.
