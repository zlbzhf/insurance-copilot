# Hermes-First Design

This repository intentionally packages Insurance Copilot as a Hermes skill.

## Why not Claude plugin layout?

`claude-for-legal` is useful as a reference for domain-specific workflows, guardrails, examples, and managed-agent ideas. Hermes consumes reusable procedures primarily through skills, project context files, toolsets, cron jobs, MCP configuration, and memory.

Therefore the canonical artifact is:

```text
skills/insurance_copilot/SKILL.md
```

The previous `legacy Claude plugin metadata`, `.mcp.json`, and `CLAUDE.md` layout has been replaced by Hermes-native docs, references, and recipes.

## Unified Project Identity and Telegram Runtime Limit

Use one canonical underscore-safe project identity everywhere new user-facing or runtime material names this project:

1. **Repository/product slug:** `insurance_copilot`.
   - Canonical GitHub URL: `https://github.com/zlbzhf/insurance_copilot`.
   - Local checkout path should use `insurance_copilot` when possible.
2. **Hermes skill command/install identity:** `insurance_copilot`.
   - Source path: `skills/insurance_copilot/`.
   - Installed path: `~/.hermes/skills/insurance/insurance_copilot/`.
   - User-facing load command: `/skill insurance_copilot`.
   - Telegram-safe direct command/menu name: `/insurance_copilot`.
3. **Agent-private workspace root:** `~/.insurance_copilot/agents/<agent-id>/`.
   - The previous `~/.insurance-copilot/` root was a legacy path. Migrate private data deliberately and never copy customer/private data into the public repository.

Current Hermes core behavior normalizes skill slash-command keys internally to hyphenated slugs. A skill with `name: insurance_copilot` may be stored internally as `/insurance-copilot`, while Telegram menu rendering sanitizes hyphens back to underscores because Telegram commands allow underscores but not hyphens. Gateway matching treats underscore and hyphen command input as aliases, so `/insurance_copilot` resolves even if Hermes internals expose an `/insurance-copilot` key.

Repository-level mitigation: make the repository slug, installable skill, private workspace root, and all user-facing Telegram examples underscore-safe; add tests/validators for the unified identity; and clean stale installed runtime copies that still live under legacy hyphen paths such as `~/.hermes/skills/insurance/insurance-copilot/`.

Known Hermes core limitation: `/skill insurance_copilot` or `/insurance_copilot` loads the skill content and forwards it into the normal agent turn; Hermes core does not provide a per-skill `on_load` hook that can execute deterministic onboarding before the model responds. Therefore the first-use Practice Profile behavior must be encoded in `SKILL.md`, `references/cold-start-interview.md`, examples, evals, tests, and validators. If stronger behavior is needed upstream, propose a Hermes core enhancement for skill activation hooks or a frontmatter field such as `on_empty_invocation_prompt`.

Telegram allows up to 100 bot menu commands. Hermes builds the menu as core commands first, then plugin commands, then local skill commands until the cap is reached. If the menu is already full, a valid skill may still be loadable through `/skill insurance_copilot` or direct `/insurance_copilot` even if it is omitted from Telegram's visible autocomplete menu. Release testing should verify both: the Hermes resolver path and the actual Bot API menu state after gateway restart or manual command registration.
