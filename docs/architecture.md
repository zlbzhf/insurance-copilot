# Insurance Copilot Architecture

Insurance Copilot uses a three-layer knowledge architecture.

```text
Layer 1: General Public Workflow Skill
Layer 2: Public Institution Knowledge Packs
Layer 3: Agent Private Knowledge Workspace
```

## Layer 1 — General Public Workflow Skill

Path:

```text
skills/insurance-copilot/
```

Purpose:

- reusable Hermes skill;
- general insurance workflow discipline;
- safety, privacy, action-safety, compliance-review boundaries;
- templates and references that apply across institutions.

This layer should not contain institution-confidential material or customer data.

## Layer 2 — Public Institution Knowledge Packs

Path:

```text
knowledge/institutions/
```

Purpose:

- public, collaboratively maintained knowledge packs by insurer/institution;
- Karpathy-style LLM wiki structure;
- public source records, product/service summaries, concepts, comparisons, and query pages;
- remote-first direction so users can fetch only the packs/pages they need.

Institution packs are public knowledge only. If a material is not public/shareable, it does not belong here.

## Public Knowledge Maintenance Pipeline

The public institution layer is maintained through evidence-driven schema evolution, not one-time template guessing.

```text
public source package
  -> intake/
  -> scripts/ingest_gateway.py
  -> staging/<institution>/<source-id>/
  -> schema gaps + proposed pages
  -> validator + human review
  -> knowledge/institutions/<institution>/
```

Canonical standards live in:

```text
standards/
schemas/
prompts/
```

Contributor local drafts may help, but the public repository treats them as hints. The gateway and maintainers re-check raw/source evidence before content becomes canonical.

## Layer 3 — Agent Private Knowledge Workspace

Template:

```text
agent-workspace-template/
```

Suggested private location:

```text
~/.insurance-copilot/agents/<agent-id>/
```

Purpose:

- customer data;
- private agent notes;
- non-public institution materials held by the agent;
- private scripts, renewal registers, private evals, and follow-up plans.

This layer is local/private and must not be committed to the public repository.

## Conflict and Priority Rules

When sources conflict:

1. Law/regulation/compliance red lines and action-safety constraints.
2. Current authoritative customer/policy/carrier facts.
3. Current official institution source.
4. Public institution pack summary.
5. Agent-private notes.
6. General workflow template.

If uncertainty remains, mark `[verify]` and escalate.

## Why Packs May Later Become Separate Repositories

Do not split too early. Start in this repo to stabilize schema and contribution rules.

Split an institution pack into its own repository only when:

- the pack has significant volume;
- it has dedicated maintainers;
- users benefit from remote-only discovery/loading;
- release cadence differs from the general skill;
- CI/review ownership is clearer in a separate repo.

The registry format in `knowledge/registry.json` supports both in-repo and remote packs.
