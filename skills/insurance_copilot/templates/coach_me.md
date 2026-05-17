# Coach_me Working Document — Insurance Handoff Template

> Use after the standalone **coach_me** skill has clarified a messy insurance-agent question, or when Insurance Copilot needs to start that clarification. This template is the insurance-domain wrapper around `skills/coach_me/templates/working-document.md`; it is not a separate fixed questionnaire.

---

## Situation

- **Trigger:**
- **Insurance classification:** client intake / policy review / claims support / replacement risk / renewal-lapse / product fit / compliance copy / customer advocacy / other
- **Customer-impacting risk:**
- **Requested output:** internal note / customer-safe draft / review packet / source checklist / next-workflow handoff

---

## Known Facts

- ...

*Use only facts confirmed by the conversation or reviewed sources.*

---

## Pending Verification / [待核实]

- ...

*Use `[待核实]` for carrier, policy, payment, claim, underwriting, product, jurisdiction, compliance, or customer facts that are not verified against authoritative sources.*

---

## Working Understanding

- **Current understanding:**
- **Most important uncertainty:**
- **Customer-first advocacy angle:**
- **Compliance / escalation concern:**

---

## Information Sufficiency

- **Enough to proceed?** yes / partial / no
- **Safest next action with current facts:**
- **What would make it sufficient:**
- **Risk of proceeding now:**

---

## Next Question If Continuing

Ask one dynamic question at a time in conversational interfaces.

- **Question:**
- **Why it matters:**
- **Recommended default answer if the agent is unsure:**

*Do not force exactly three questions. Do not force Direction/Risk/Source/Action categories. Continue only while the next answer materially improves the working document.*

---

## Recommended Insurance Route

- **Next workflow:** Client Needs Intake / Policy Review Assistant / Claims Support Triage / Replacement Risk Triager / Renewal-Lapse Follow-up Planner / Product Fit Reviewer / Compliance Copy Checker / Customer Advocacy Memo / Stakeholder Summary / other
- **Why this route:**
- **Human review owner:** licensed agent / supervisor / compliance / claims specialist / underwriting support / legal-tax-investment professional / pack maintainer
- **Minimum safe next step:**

---

## Review Gates Needed

- **Source Grounding and Data Boundary Gate:** yes / no / [待核实]
- **Professional Review Gate:** yes / no / [待核实]
- **External Write Action Boundary Gate:** yes / no / [待核实]
- **Side-effect status:** no external action is authorized

---

## Backfeed Candidate

- **Reusable scenario pattern:**
- **Public-pack safe?** yes / no — no customer data in public packs
- **Agent-private only?** yes / no
- **Requires explicit persistence approval?** yes

## Coach_me Runtime Phrase Ledger

This surface intentionally preserves these runtime concepts for deterministic gates: **standalone Coach_me skill**, **Coach_me Guided Reasoning Mode**, **Coach_me before Client Needs Intake**, **source discovery order**, **dynamic questioning**, **not a fixed questionnaire**, **not a fixed question count**, **not fixed categories**, **one question at a time**, **interactive conversational gateway**, **recommended default answer**, **answer now or continue questioning**, **automatically stop questioning when information is sufficient**, **Coach_me Working Document**, **public institution knowledge**, **agent-private workspace**, **customer-specific materials**, **Q&A intake is raw source input**, **no automatic persistence**, **manual-first practitioner workflow**, **Source Grounding and Data Boundary Gate**, and **Professional Review Gate**.

