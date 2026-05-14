# Public Knowledge Layer

This directory contains public knowledge assets that complement the general `insurance-copilot` Hermes skill.

The project uses three layers:

1. **General public layer** — the Hermes skill and domain workflows under `skills/insurance-copilot/`.
2. **Public institution knowledge layer** — collaboratively maintained public institution packs under `knowledge/institutions/`.
3. **Agent private knowledge layer** — local/private agent workspaces based on `agent-workspace-template/`.

Only public, shareable, non-customer, non-confidential material belongs here.

## Remote-First Direction

Institution packs may later live in separate remote repositories. This repo keeps the canonical schema, templates, seed packs, and registry format. Hermes can use the registry to discover remote pack indexes and fetch only the pages needed for a task.
