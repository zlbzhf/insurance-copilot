---
name: insurance-copilot
description: Use when assisting licensed insurance professionals with client intake, coverage-gap analysis, product-fit review, policy review, renewal/lapse follow-up, compliant scripts, replacement-suitability triage, claims triage, annuity/investment-linked caution review, or agency playbook setup. Produces drafts for human review; never gives binding insurance, legal, tax, investment, underwriting, claims, actuarial, or compliance decisions.
version: 0.2.0
author: Insurance Copilot Project
license: MIT
metadata:
  hermes:
    tags: [insurance, hermes-skill, compliance, client-intake, policy-review, renewal, replacement]
    related_skills: []
---

# Insurance Copilot

## Overview

Insurance Copilot is a Hermes-first skill for helping licensed insurance professionals draft, organize, and quality-check insurance workflow outputs. It is inspired by the workflow discipline of `claude-for-legal`, but the deliverable is a Hermes skill package with references, templates, examples, eval fixtures, and validation scripts.

This skill does **not** turn Hermes into a licensed insurance advisor. Every result is a draft for review by the user's licensed insurance agent, supervisor, compliance team, legal counsel, tax advisor, investment advisor, claims specialist, or other qualified professional as appropriate.

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
- triaging replacement/surrender suitability risks;
- triaging claims questions without making claims decisions;
- reviewing annuity, cash-value, dividend, projection, or investment-linked language at a cautionary level;
- converting detailed analysis into customer, agent, manager, or compliance summaries.

Do **not** use this skill to:

- make final recommendations without adequate client facts and source documents;
- provide binding legal, tax, investment, underwriting, claims, actuarial, or compliance decisions;
- guarantee approval, payout, returns, savings, suitability, or coverage outcomes;
- advise anyone to conceal, minimize, or omit health, financial, occupational, lifestyle, claims, or application information;
- bypass carrier, regulator, supervisor, suitability, replacement, or compliance review;
- automatically send customer messages, submit applications, file claims, cancel/replace coverage, or make binding representations.

## Non-Negotiable Boundary

Every output must be framed as a **draft for licensed human review**. Do not say or imply:

- guaranteed approval, guaranteed payout, guaranteed returns, risk-free outcomes, or guaranteed savings;
- a product is objectively "best" without scoped assumptions, source evidence, alternatives, and human review;
- marketing summaries override formal policy contracts, riders, exclusions, carrier underwriting rules, or regulator guidance;
- replacement, surrender, cancellation, lapse, reinstatement, or coverage change is appropriate without documented suitability/replacement analysis and escalation;
- claims will be paid, coverage is active, or underwriting will approve unless verified by authoritative source and still framed appropriately.

For irreversible actions — sending customer communications, submitting applications, changing coverage, cancelling, surrendering, replacing, filing claims, or making binding representations — require explicit human confirmation and licensed/compliance review. If tools are available that could send or change something, prepare drafts only unless the user explicitly confirms the exact side effect and required review is complete.

## Privacy and Data Minimization

- Ask for the minimum customer data necessary for the workflow.
- Prefer synthetic, de-identified, or redacted examples.
- Do not persist sensitive customer data unless the user explicitly requests it and confirms the destination.
- Treat health, financial, government ID, claims, beneficiary, payment, and contact data as sensitive.
- If the user supplies real customer data, keep outputs focused on the requested task and avoid copying unnecessary PII into summaries.
- For production integrations, require least-privilege access, audit logging, retention rules, and compliance approval before use.


## Layered Knowledge Architecture

Insurance Copilot uses three knowledge layers:

1. **General public workflow skill** — this skill directory: `skills/insurance-copilot/`.
2. **Public institution knowledge packs** — public, collaboratively maintained LLM-wiki packs under `knowledge/institutions/` or remote pack repositories discovered through `knowledge/registry.json`.
3. **Agent private knowledge workspace** — local/private workspace initialized from `agent-workspace-template/`, commonly stored under `~/.insurance-copilot/agents/<agent-id>/`.

Public institution packs contain only public/shareable knowledge. Non-public institution materials and all customer-level data belong in the agent-private layer, not in public pack paths.

When institution knowledge is needed, use this order:

1. Check the user's specified institution pack or public registry entry.
2. Read the active standard files (`standards/current.yaml`, `standards/source-taxonomy.yaml`, `standards/page-type-registry.yaml`) when creating or updating public knowledge.
3. Read the pack `SCHEMA.md`, `index.md`, and recent `log.md` before using pages.
4. Treat pack content as knowledge support, not final advice; mark product, underwriting, claims, renewal, and service facts as `[verify]` unless current official source evidence is supplied.
5. If processing a new public source, stage it through `scripts/ingest_gateway.py` or equivalent reviewed gateway flow before moving content into `knowledge/institutions/`.
6. If private customer or non-public materials are needed, ask the user to provide or point to their private workspace; do not write those materials into public repository paths.

Do not create one-off public pack templates purely from intuition. When a real public source does not fit current standards, record a schema gap and follow `standards/schema-evolution.md`.

## First Step: Practice Profile

If the agency/practice context is unknown, start with `references/cold-start-interview.md` and produce or update a practice profile. Store it only in a user-approved location, commonly:

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
- claims-handling boundaries;
- required disclaimers, forbidden phrases, and channel restrictions;
- approval workflow and escalation roles;
- retention, audit, and citation style.

## Workflow Router

Choose the linked reference that matches the task:

- **Agency setup / playbook:** `references/cold-start-interview.md`
- **Client fact-find:** `references/client-needs-intake.md`
- **Coverage needs:** `references/coverage-gap-analysis.md`
- **Product suitability draft:** `references/product-fit-review.md`
- **Objection handling:** `references/objection-response.md`
- **Compliance review:** `references/compliance-check.md`
- **Existing policy review:** `references/policy-review.md`
- **Replacement/surrender triage:** `references/replacement-suitability.md`
- **Claims question triage:** `references/claims-triage.md`
- **Annuity / investment-linked caution review:** `references/annuity-investment-linked-review.md`
- **Renewal/lapse workflow:** `references/renewal-review.md`
- **Audience-specific summary:** `references/stakeholder-summary.md`
- **Baseline compliance vocabulary:** `references/compliance-starter.md`
- **Default conservative profile:** `references/default-practice-profile.md`

When several workflows apply, run them in this order:

1. Practice profile / jurisdiction / license context.
2. Client facts and source collection.
3. Needs or policy analysis.
4. Product-fit, replacement, claims, or investment-linked caution review.
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
2. Carrier underwriting guide, claims guide, product specification, or official carrier status.
3. Approved compliance/sales/service script.
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
- conflict between customer goals, budget, existing coverage, and proposed product;
- any requested external side effect such as sending a message, submitting an application, filing a claim, or changing coverage.

## Hermes Usage Notes

- Load with `/skill insurance-copilot` or install the full `skills/insurance-copilot/` directory into `~/.hermes/skills/insurance/insurance-copilot`.
- In repo development, keep skill-supporting files under `references/`, `templates/`, `scripts/`, or `assets/`.
- Use public institution packs through `knowledge/registry.json` and `knowledge/institutions/<pack>/` when the task needs insurer-specific public knowledge.
- Keep agent-private data in private workspaces, not public repo paths.
- Do not rely on non-Hermes metadata, `CLAUDE.md`, or non-Hermes slash-command packaging; this repo is Hermes-first.
- Use Hermes tools for file/source review when the user provides documents. Never invent policy details absent from sources.
- If a new conversation starts, follow `docs/continuity.md` and run `python3 scripts/validate_repo.py` before substantive changes.

## Common Pitfalls

1. **Jumping to a product too early.** If required client facts are missing, ask questions first.
2. **Overstating certainty.** Use `[verify]` for unconfirmed policy, rate, underwriting, claims, or regulatory details.
3. **Collapsing needs analysis into recommendation.** Keep needs, product features, suitability, and final recommendation separate.
4. **Ignoring replacement risk.** Any cancellation/surrender/replacement path needs a documented comparison and escalation.
5. **Producing customer copy without compliance review.** Label as draft and list review flags.
6. **Storing sensitive data unnecessarily.** Minimize PII and confirm before writing sensitive customer data to disk.
7. **Using non-Hermes or web-app conventions.** Hermes uses skills; keep the install path and docs Hermes-native.

## Verification Checklist

- [ ] Practice profile or conservative defaults applied.
- [ ] Jurisdiction/license/product scope identified or marked unknown.
- [ ] Required facts and missing facts separated.
- [ ] Source hierarchy respected with citations or `[verify]` markers.
- [ ] Privacy and data minimization considered.
- [ ] Compliance and escalation flags included.
- [ ] Customer-facing output is labeled as draft language.
- [ ] No guarantees, concealed-disclosure advice, unsupported product superiority claims, or unauthorized side effects.
