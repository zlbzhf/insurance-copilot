# ADR-0001: Gateway-Agnostic Interactive Protocol

Status: accepted
Date: 2026-05-17
Runtime authority: decision record only; current behavior lives in runtime surfaces and executable gates

## Context

Insurance Copilot originally used several Chinese Telegram onboarding phrases because the first real runtime channel was Telegram. That created an accidental product constraint: the actual behavior should apply to any interactive conversational gateway, not only one platform.

The project also added Coach_me v2 as a productized workflow. Its one-question-at-a-time behavior is a conversational protocol, not a Telegram-specific behavior.

## Decision

Use `interactive conversational gateway` as the generic runtime concept for chat-like channels. Keep actual Telegram-specific wording only where the document discusses Hermes gateway commands, bot menus, or real platform limits.

The protocol decisions are:

- Coach_me uses an interactive conversational gateway sequential question protocol.
- In conversational use, Coach_me asks one question at a time and sends only the active question in the current turn.
- The three-question round remains `Question 1/3`, `Question 2/3`, and `Question 3/3`; all three questions are batched only for an offline checklist request.
- Product recommendation intent routes Coach_me before Client Needs Intake or product-fit drafting.
- Chinese interactive onboarding defaults apply across interactive conversational gateways and are not limited to any single platform.

## Runtime Surfaces

Current behavior lives in:

- `skills/insurance_copilot/SKILL.md`
- `skills/insurance_copilot/references/coach-me.md`
- `skills/insurance_copilot/templates/coach-me.md`
- `skills/insurance_copilot/references/cold-start-interview.md`
- `skills/insurance_copilot/references/client-needs-intake.md`
- `docs/workflow-surface.md`
- `docs/quickstart.md`
- `README.md`
- `README.zh-CN.md`

## Executable Gates

Regression protection lives in:

- `tests/test_practitioner_mvp_surface.py`
- `scripts/validate_repo.py`
- `evals/cases/coach-me-sequential-question-protocol.json`
- `evals/expected/coach-me-sequential-question-protocol.md`
- `evals/cases/coach-me-v2-productized-workflow.json`
- `evals/expected/coach-me-v2-productized-workflow.md`
- `evals/cases/chinese-interactive-onboarding.json`
- `evals/expected/chinese-interactive-onboarding.md`

## Consequences

- Future gateway integrations inherit the same Chinese onboarding and Coach_me interaction logic without rewriting the insurance workflow.
- Telegram remains a supported delivery channel, not a product identity boundary.
- New platform-specific language should be isolated to gateway implementation or menu documentation.
- If this decision changes, update runtime surfaces and executable gates first; this ADR is not the runtime authority by itself.
