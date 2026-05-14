# Synthetic End-to-End Demo: Family Protection Workflow

This demo uses synthetic data only. It shows the practical loop Insurance Copilot should support before any real customer or insurer source is introduced.

## 1. Cold-Start Assumptions

- Practice profile: provisional conservative defaults.
- Jurisdiction/license scope: `[verify]`.
- Review owner: licensed agent plus compliance reviewer before customer-facing use.
- Forbidden actions: no automatic sending, CRM writes, applications, policy changes, or claims filing.

## 2. Client Needs Intake

Synthetic notes: couple ages 35/34, two children, mortgage, employer health coverage, unknown life/disability coverage, budget unknown, wants family protection and education funding.

Output expected:
- known facts separated from missing facts;
- product recommendation is premature;
- ask budget, income, existing coverage, beneficiary goals, and approved health-disclosure questions.

## 3. Coverage Gap Drafter

Possible categories:
- life/family protection;
- income interruption/disability;
- medical/critical illness out-of-pocket exposure;
- accident/emergency reserve;
- education funding discussion.

All amounts and product categories are `[verify]` until facts and methodology are supplied.

## 4. Client Plan Draft

Use `skills/insurance-copilot/templates/client-plan-draft.md` to create:
- customer profile snapshot;
- confirmed needs;
- missing facts;
- current coverage snapshot;
- candidate solution categories;
- source caveats;
- customer-safe summary;
- internal agent notes.

No specific product is recommended without source-backed product facts and licensed review.

## 5. Compliance Copy Checker

Unsafe draft to test:

> Guaranteed approval and guaranteed payout. This is the best risk-free plan for every family.

Expected result:
- Red risk;
- flags guaranteed approval, guaranteed payout, best, risk-free, every family;
- provides safer draft language;
- requires compliance review.

## 6. Stakeholder Summary

Create two versions:
- agent/internal version with missing facts, risks, and review gates;
- customer-safe version with caveats and no internal-only risk flags.

## 7. Daily Agent Workbench Next Actions

- Verify jurisdiction/license/profile assumptions.
- Ask missing facts before product discussion.
- Prepare customer-safe follow-up draft for review.
- Create internal task to verify existing coverage.
- Do not send or write to CRM/calendar automatically.
