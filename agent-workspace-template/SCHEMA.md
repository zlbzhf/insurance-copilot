# Agent Private Wiki Schema

## Domain

Private working knowledge for one insurance agent: customers, follow-ups, personal notes, private institution materials, and private evals.

## Conventions

- File names use pseudonymous IDs, not customer names.
- Every substantive page starts with YAML frontmatter.
- Use `[[wikilinks]]` for customer, segment, product, and follow-up relationships.
- Every new or updated page should be listed in `index.md` if it is a durable page.
- Append all material changes to `log.md`.
- Do not copy private workspace files into public repo paths.

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: agent-profile | client | policy-summary | followup | segment | private-institution-note | private-script | private-eval | query
data_classification: private-agent-knowledge | private-customer-data | private-institution-note
institution: <institution-pack-id> | unknown
customer_id: optional-pseudonymous-id
sensitivity: low | medium | high
sources: []
retention: review | keep | delete-after-date
---
```

## Customer Pages

Required sections:

- Identity Handling
- Known Facts
- Goals / Concerns
- Policies / Coverage Summary
- Follow-ups
- Missing Facts / Verify
- Privacy Notes

## Private Institution Notes

Use `private-institution-notes/<institution>/`. Required sections:

- Source / Authorization
- Summary
- How It Affects Workflows
- Conflicts / Verify
- Public-Pack Candidate?

Only mark something as a public-pack candidate if it can be shared publicly without customer data, confidential material, or redistribution issues.


## CRM-lite Page Types

- `lead` — private lead source, consent, known facts, missing facts, and next action.
- `customer` — private customer page under `clients/`.
- `opportunity` — potential new sale, review, renewal, referral, or service opportunity.
- `meeting-note` — meeting prep, facts learned, missing facts, and follow-up tasks.
- `policy-summary` — private policy facts with `[verify]` carrier/source status markers.
- `claim-tracker` — claim-support documents, deadlines, and neutral service notes.
- `referral-tracker` — referral consent, channel, incentive verification, and next action.
- `task-list` — daily/weekly tasks and CRM/calendar export drafts.

CRM-lite pages must keep private facts in the private workspace only. They may be summarized for public repo examples only after full de-identification or synthetic rewriting.
