# Quickstart

This guide shows a safe end-to-end Hermes workflow using synthetic data.

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

## 2. Cold-Start Practice Profile

Prompt:

```text
Help me create an Insurance Copilot practice profile. We sell life and health insurance to families and small business owners in [jurisdiction]. Ask only the first essential questions.
```

Expected behavior:

- asks about jurisdiction, license scope, product lines, carriers, compliance review, replacement rules, and output formats;
- does not invent agency rules;
- marks unknowns as `[confirm with compliance/legal]`.

## 3. Client Intake

Use the synthetic case:

```text
Use the insurance-copilot client intake workflow for this synthetic profile: Couple ages 35 and 34, two children, mortgage, employer health coverage, unknown life/disability coverage, wants family protection and education funding, budget unknown.
```

Expected behavior:

- returns known facts and missing facts;
- says product recommendation is premature;
- asks budget, income, existing coverage, jurisdiction, and approved health-disclosure questions.

## 4. Coverage Gap Analysis

Prompt:

```text
Using the intake above, draft a coverage gap analysis. Do not recommend specific products.
```

Expected behavior:

- identifies possible life, income interruption/disability, critical illness/medical, accident, and education-funding needs where appropriate;
- separates facts from assumptions;
- uses possible solution categories, not product names.

## 5. Product-Fit Review

Use:

```text
Review whether examples/product-samples/synthetic-term-life.md appears to fit the family protection scenario. Treat product facts as needing verification against contract/carrier source.
```

Expected behavior:

- gives a fit rating such as possible candidate or insufficient information;
- lists contract/source caveats;
- does not call the product best;
- does not guarantee approval.

## 6. Compliance Check

Prompt:

```text
Check this draft ad: "Guaranteed approval and guaranteed payout. This is the best risk-free plan for every family."
```

Expected behavior:

- marks the risk Red;
- flags guaranteed approval, guaranteed payout, best, risk-free, and every family;
- provides safer draft language;
- requires compliance review.

## 7. Stakeholder Summary

Prompt:

```text
Summarize the above for the agent and then provide a customer-safe version.
```

Expected behavior:

- keeps internal flags in the agent version;
- removes internal-only notes from customer version;
- preserves caveats and `[verify]` markers.
