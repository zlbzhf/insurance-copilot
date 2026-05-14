# Jurisdiction and Agency Adaptation

The default Insurance Copilot skill is conservative and generic. It is not jurisdiction-specific legal or regulatory advice. Agencies should adapt it using approved sources.

## Source Inputs

Use agency-approved and jurisdiction-specific sources such as:

- regulator guidance;
- carrier compliance bulletins;
- approved sales scripts;
- replacement disclosure forms;
- advertising review rules;
- record-retention policies;
- complaint handling procedures;
- product-specific training material.

## Adaptation Procedure

1. Run `references/cold-start-interview.md`.
2. Create a practice profile from `templates/practice-profile.md`.
3. Fill in required disclaimers, forbidden phrases, approval workflow, required forms, and escalation roles.
4. Have compliance/legal review the profile.
5. Store the approved profile in a user-approved location.
6. Update examples/evals if new jurisdiction-specific red flags are introduced.

## What to Customize

- License/product scope.
- Required forms and disclosures.
- Replacement/surrender rules.
- Advertising and social media restrictions.
- Record retention and audit expectations.
- Approved customer communication channels.
- Vulnerable-customer rules.
- Claims-handling boundaries.

## What Not to Do

- Do not treat this repository's starter text as legal advice.
- Do not remove conservative guardrails without compliance approval.
- Do not encode rules from memory when source documents are available.
