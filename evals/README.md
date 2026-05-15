# Evaluation Fixtures

These fixtures are synthetic, non-sensitive regression cases for the Insurance Copilot skill.

They test expected safety behavior for high-risk workflows. They are deterministic static evals, not full model-in-the-loop tests.

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
