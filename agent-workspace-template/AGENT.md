---
agent_id: replace-with-agent-id
default_institution_pack: unknown
data_classification: private-agent-knowledge
storage_policy: local-or-private-repo-only
customer_data_allowed: true
public_upload_allowed: false
---

# Agent Private Workspace

This workspace is private. It may contain customer data and non-public institution notes. Do not copy it into the public `insurance-copilot` repository.

## Privacy Rules

- Use minimum necessary customer data.
- Prefer pseudonymous customer IDs in file names.
- Do not paste unnecessary PII into prompts or summaries.
- Do not export customer data into public institution packs.
- Keep non-public institution material under `private-institution-notes/`.
- Draft customer-facing outputs only; do not send automatically.

## Source Priority in This Workspace

1. Current customer-provided documents and confirmed facts.
2. Current official carrier/policy/portal source.
3. Public institution pack pages.
4. Private institution notes in this workspace.
5. Agent personal notes.

If a private note conflicts with an official public/current source, mark `[verify]` and escalate.
