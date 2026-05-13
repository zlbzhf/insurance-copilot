# Evaluation Fixtures

These fixtures are synthetic, non-sensitive cases for regression testing the Insurance Copilot skill.

They are not automated model evaluations yet. They define expected safety behaviors that future eval runners should assert.

Each case should include:

- `id`
- `workflow`
- `input_summary`
- `must_include`
- `must_not_include`
- `escalation_expected`
