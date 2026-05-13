# Hermes-First Design

This repository intentionally packages Insurance Copilot as a Hermes skill.

## Why not Claude plugin layout?

`claude-for-legal` is useful as a reference for domain-specific workflows, guardrails, examples, and managed-agent ideas. Hermes consumes reusable procedures primarily through skills, project context files, toolsets, cron jobs, MCP configuration, and memory.

Therefore the canonical artifact is:

```text
skills/insurance-copilot/SKILL.md
```

The previous `legacy Claude plugin metadata`, `.mcp.json`, and `CLAUDE.md` layout has been replaced by Hermes-native docs, references, and recipes.
