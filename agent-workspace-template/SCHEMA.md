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
institution: aia | ping-an | pacific | unknown
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
