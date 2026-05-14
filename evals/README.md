# Evaluation Fixtures

These fixtures are synthetic, non-sensitive regression cases for the Insurance Copilot skill.

They test expected safety behavior for high-risk workflows. They are deterministic static evals, not full model-in-the-loop tests.

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
