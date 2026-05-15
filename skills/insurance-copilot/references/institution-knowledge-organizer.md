# Institution Knowledge Organizer

Use this reference when a maintainer or agent wants to organize public insurer/institution knowledge, especially an **AIA public pack** update, without mixing public sources with private customer or agent materials. This is the runtime playbook for a **source-backed public pack update**.

Runtime files:

- `references/institution-knowledge-organizer.md`
- `templates/institution-knowledge-organizer.md`

The workflow translates insurance RAG/policy-assistant grounding ideas into a manual-first Hermes skill process: start from a public source, create or check a **source record**, map it to a canonical page type, preserve the **public/private boundary**, mark uncertain fields with `[verify]`, and require **pack maintainer review** before canonical knowledge is trusted.

## When to Use

Use **Institution Knowledge Organizer** when:

- a user provides a public AIA/友邦, carrier, regulator, or insurer-service source;
- a maintainer wants to add a source record or page to `knowledge/institutions/<pack>/`;
- a workflow needs public insurer facts but must keep customer documents in the agent-private workspace;
- a source suggests a schema gap rather than fitting a current template;
- a claims, renewal, product, FAQ, underwriting, marketing, or service-process page needs source-backed curation.

Do not use this workflow to process real customer files, CRM exports, claim files, private agent notes, non-public training material, or institution-confidential SOPs. Those belong outside the public repository.

## Required Inputs

Minimum useful inputs:

1. Pack ID, for example `aia` for the AIA public pack.
2. Public source URL/title and retrieval date.
3. Source type if known: `official-service-guide`, `official-faq`, `official-product-page`, `official-terms`, `regulator-guidance`, or another type from `standards/source-taxonomy.yaml`.
4. Target page type if known, or the schema gap to investigate.
5. Whether excerpts are allowed. Default to link-only unless rights are explicit.
6. Intended use: internal source organization, proposed public page, or customer-facing draft support.

## Method

1. **Read standards first.** Check `standards/current.yaml`, `standards/source-taxonomy.yaml`, `standards/page-type-registry.yaml`, and the pack `SCHEMA.md` before inventing fields.
2. **Create or verify the source record.** The record must include id, institution, source type, URL, retrieved date, `public_source: true`, and redistribution mode.
3. **Classify the page type.** Use canonical mappings such as `official-service-guide -> claims-process-summary` and `official-faq -> faq-summary`.
4. **Draft the page as source-backed summary, not copied source text.** Use short facts, links, and `[verify]` markers. Do not paste full copyrighted pages unless redistribution is explicit.
5. **Preserve the public/private boundary.** No customer data, private agent notes, secrets, production exports, or non-public institution materials in `knowledge/institutions/`.
6. **Mark review status.** Every proposed page should state Source-backed status, verification gaps, and pack maintainer review requirement.
7. **Run validators.** At minimum run `python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia` for the AIA public pack and include the result in the handoff.
8. **Use Professional Review Gate if output becomes customer-facing or regulated.** Public pack pages support service, but they are not final claims, underwriting, product, or compliance decisions.

## AIA Public Pack Defaults

For the AIA public pack:

- Keep public AIA Hong Kong / AIA official pages as public sources only.
- Use `sources/*.yaml` records with `redistribution.mode: link-only` unless usage rights are clear.
- Claims-process pages must say they are not a final claims decision and must not promise payment, timing, approval, coverage, or policy interpretation.
- FAQ pages should summarize questions covered and keep customer-facing usage under `[verify]` plus pack maintainer review.
- If a source conflicts with policy contract language, regulator guidance, or updated carrier notices, mark the conflict and escalate to a maintainer.

## Output Format

Use this structure for a source-backed public pack update:

```markdown
## Institution Knowledge Organizer
- Pack:
- Workflow: source-backed public pack update
- Source record:
- Source type / page type:
- Public/private boundary:
- Source-backed status:
- `[verify]` items:
- Pack maintainer review:

## Proposed Pack Changes
- Source records:
- Pages:
- Index/log updates:
- Schema gaps:

## Validation Plan
- `python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia`
- `python3 scripts/run_evals.py`
- `python3 scripts/validate_repo.py`

## Professional Review Gate
- Action class:
- Review owner:
- Source verification status:
- Customer-facing approval status: draft for licensed/compliance review; not approved to send
- Side-effect status: no external action is authorized
- Minimum safe next step:
```

## Guardrails

- Do not add customer data, private notes, secrets, or non-public institution materials to public packs.
- Do not invent product, underwriting, renewal, or claims facts absent from source records.
- Do not treat public FAQ or service summaries as policy contracts.
- Do not claim a page is current unless retrieved date, source URL, and review status are visible.
- Do not make a final underwriting, claims, coverage, product, legal, tax, investment, or compliance decision.
- Do not perform external writes, customer sending, claim filing, CRM updates, or source publication without explicit user authorization and required review.
- If the source does not fit existing standards, record a schema gap instead of creating a one-off template.
