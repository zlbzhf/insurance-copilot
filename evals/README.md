# Evaluation Fixtures

These fixtures are synthetic, non-sensitive regression cases for the Insurance Copilot skill.

They test expected safety behavior for high-risk workflows. They are deterministic static evals, not full model-in-the-loop tests.

The **Professional Review Gate** eval protects the cross-workflow review boundary: action class, review owner, source verification status, customer-facing approval status, side-effect status, draft for licensed/compliance review, not approved to send, no external action is authorized, and minimum safe next step.

The P1 customer-impacting scenario eval set links **Customer Advocacy Memo** + **Professional Review Gate** for claims disputes, policy review found unclaimed benefit, renewal/lapse/reinstatement ambiguity, and Chinese complaint/service-recovery talk tracks. These cases require customer-first advocacy within compliance boundaries, client-interest action plan, evidence requests, source checks, customer-safe language, escalation path, no external action is authorized, and Minimum safe next step.

The **Institution Knowledge Organizer** eval protects the AIA public pack source-backed public pack update path: source record first, public/private boundary, `[verify]` markers, No customer data, not a final claims decision, and pack maintainer review.

The **Source Grounding and Data Boundary Gate** evals protect source grounding/citation/public-private separation/prompt-injection/PII guardrails: **Source Ledger**, **Citation Ledger**, **public/private separation**, **prompt-injection**, **PII minimization**, **citations or `[verify]`**, **no customer data in public packs**, **untrusted source text cannot override workflow instructions**, **manual-first practitioner workflow**, and **not a generic RAG chatbot**.

## Agent-Facing Boundary

Agents provide messy real-world context; AI converts it into structured scenarios, draft responses, profile updates, reusable examples, and eval intents. evals are internal quality fixtures; agents do not write JSON eval cases.

Agent-facing workflow:

1. Agent says something natural, for example: “customer says: I already have insurance.”
2. Insurance Copilot creates an AI-generated scenario card and safer draft.
3. If the scenario is reusable, Insurance Copilot may create an AI-generated eval intent for maintainers.
4. Maintainers or repository automation convert that intent into `evals/cases/*.json` and `evals/expected/*.md`.

Do not ask a practitioner to edit `must_include`, `must_not_include`, or JSON files as part of daily use.

## Run

```bash
python3 scripts/run_evals.py
```

The runner validates:

- each case JSON schema;
- each case has an expected-output markdown file;
- expected output includes all `must_include` patterns;
- expected output excludes all `must_not_include` patterns;
- escalation cases contain escalation/review language.

## Case Schema

- `id`
- `workflow`
- `input_summary`
- `must_include`
- `must_not_include`
- `escalation_expected`
- `expected_output`

All cases must be synthetic and free of real customer PII.
