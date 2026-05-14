# Agent Private Knowledge

The agent-private layer stores personal/customer knowledge and any non-public institution materials that should not enter the public repository.

## Suggested Location

```text
~/.insurance-copilot/agents/<agent-id>/
```

Initialize from:

```text
agent-workspace-template/
```

## What Belongs Here

- customer notes, policy summaries, follow-ups, renewal registers;
- private scripts and working preferences;
- non-public institution notes that the agent is permitted to hold but not publish;
- private evals using de-identified or synthetic scenarios;
- private raw documents with appropriate authority and retention controls.

## What Does Not Belong in Public Packs

If an institution material is not public/shareable, keep it here. Do not create a public `private-institution-packs` folder. The public/private boundary is by layer:

```text
knowledge/institutions/*       public only
~/.insurance-copilot/agents/*  private agent knowledge
```

## Promoting Private Notes to Public Contributions

A private note can become a public contribution only after it is transformed into a contribution bundle that:

- removes customer data;
- removes non-public/confidential content;
- cites public sources;
- follows the pack schema;
- passes validation;
- is reviewed by maintainers.


## Readiness Gate Before Scheduled Monitoring

Before connecting a private workspace to local connector, renewal watcher, or Hermes cron wrapper workflows, run:

```bash
python3 scripts/private_workspace_readiness.py \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --format markdown
```

The readiness gate checks structure, renewal register freshness, privacy/PII-like risks, output boundaries, and retention/audit readiness. It is read-only and creates no live cron job.
