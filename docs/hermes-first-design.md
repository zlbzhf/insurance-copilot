# Hermes-First Design

This repository intentionally packages Insurance Copilot as a Hermes skill.

## Why not Claude plugin layout?

`claude-for-legal` is useful as a reference for domain-specific workflows, guardrails, examples, and managed-agent ideas. Hermes consumes reusable procedures primarily through skills, project context files, toolsets, cron jobs, MCP configuration, and memory.

Therefore the canonical artifact is:

```text
skills/insurance_copilot/SKILL.md
```

The previous `legacy Claude plugin metadata`, `.mcp.json`, and `CLAUDE.md` layout has been replaced by Hermes-native docs, references, and recipes.

## Telegram Command Identity and Runtime Limit

Keep three identities separate:

1. **Hermes skill command/install identity:** `insurance_copilot`.
   - Source path: `skills/insurance_copilot/`.
   - Installed path: `~/.hermes/skills/insurance/insurance_copilot/`.
   - User-facing load command: `/skill insurance_copilot`.
   - Telegram-safe direct command/menu name: `/insurance_copilot`.
2. **Repository/product slug:** `insurance-copilot`.
   - Example: `https://github.com/zlbzhf/insurance-copilot`.
   - Do not rename this to `insurance_copilot` just to satisfy Telegram command syntax.
3. **Agent-private workspace root:** `~/.insurance-copilot/agents/<agent-id>/`.
   - This is durable private data layout, not a Telegram command.
   - Do not rename it to `~/.insurance_copilot` unless doing a deliberate data migration.

Current Hermes core behavior normalizes skill slash-command keys internally to hyphenated slugs. A skill with `name: insurance_copilot` is stored internally as `/insurance-copilot`, while Telegram menu rendering sanitizes hyphens back to underscores because Telegram commands allow underscores but not hyphens. Gateway matching treats underscore and hyphen command input as aliases, so `/insurance_copilot` resolves to the internal `/insurance-copilot` key.

Repository-level mitigation: make the installable skill and all user-facing Telegram examples underscore-safe, keep repo/private slugs hyphenated, add tests/validators for both invariants, and clean stale installed runtime copies that still live under `~/.hermes/skills/insurance/insurance-copilot/`.

Known Hermes core limitation: `/skill insurance_copilot` or `/insurance_copilot` loads the skill content and forwards it into the normal agent turn; Hermes core does not provide a per-skill `on_load` hook that can execute deterministic onboarding before the model responds. Therefore the first-use Practice Profile behavior must be encoded in `SKILL.md`, `references/cold-start-interview.md`, examples, evals, tests, and validators. If stronger behavior is needed upstream, propose a Hermes core enhancement for skill activation hooks or a frontmatter field such as `on_empty_invocation_prompt`.

Telegram allows up to 100 bot menu commands. Hermes builds the menu as core commands first, then plugin commands, then local skill commands until the cap is reached. If the menu is already full, a valid skill may still be loadable through `/skill insurance_copilot` or direct `/insurance_copilot` even if it is omitted from Telegram's visible autocomplete menu. Release testing should verify both: the Hermes resolver path and the actual Bot API menu state after gateway restart or manual command registration.

