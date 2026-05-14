# Agent Private Workspace Template

This template shows how an individual insurance agent can keep private customer knowledge, personal notes, and non-public institution materials outside the public repository. Do not publish private workspaces or upload them into public institution packs.

Copy this directory to a private location, for example:

```bash
mkdir -p ~/.insurance-copilot/agents/<agent-id>
cp -R agent-workspace-template/* ~/.insurance-copilot/agents/<agent-id>/
```

## What Belongs Here

- private agent profile and working preferences;
- customer notes, policy summaries, follow-up logs, and renewal registers;
- non-public institution notes that the agent is allowed to hold but not publish;
- private scripts and private eval cases;
- raw private documents only when the agent has authority and a secure storage plan.

## What Must Not Be Uploaded to the Public Repo

- customer names, phone numbers, email addresses, addresses, IDs, policy numbers, claim numbers, payment data, health facts, or financial facts;
- non-public insurer training material or SOPs;
- private CRM, policy, or claims exports;
- secrets, API keys, access tokens, or credentials.

## LLM Wiki Operating Rule

Before adding/updating pages, read:

1. `SCHEMA.md`
2. `index.md`
3. last entries in `log.md`

Then update `index.md` and append to `log.md` after changes.


## CRM-lite Operating Areas

This template now includes lightweight private operating areas for real agent work:

- `leads/` — lead source, consent, and first next action.
- `clients/` — customer pages and private customer knowledge.
- `opportunities/` — sales/service opportunity tracking.
- `meetings/` — meeting prep and post-meeting notes.
- `policies/` — policy summaries and verification flags.
- `renewal-registers/` — renewal/lapse registers and due-date data.
- `claims/` — claim-support trackers and document checklists.
- `referrals/` — referral consent and follow-up tracking.
- `tasks/` — daily workbench and task export drafts.

Do not publish private copies of these files. Public examples must remain synthetic or de-identified.
