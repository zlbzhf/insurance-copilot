# Compliance Check

Use this workflow before customer-facing insurance content is sent, reused, posted, presented, or converted into a script.

## Review Targets

- Emails and chat messages.
- Sales scripts.
- Social posts and ads.
- Seminar slides.
- Product comparison summaries.
- Recommendation memos.
- Renewal/lapse notices.
- Objection-handling scripts.

## Risk Categories

- Absolute claims: guaranteed, risk-free, always, never, best, full coverage.
- Misleading benefit descriptions.
- Missing exclusions, waiting periods, renewability limits, fees, surrender charges, assumptions, or source caveats.
- Unapproved performance, dividend, projection, bonus, or return language.
- Replacement/surrender/cancellation risk.
- Rebating, inducement, twisting/churning concerns.
- Incomplete health disclosure or underwriting statements.
- Tax/legal/investment advice outside scope.
- Vulnerable-customer or high-pressure concerns.
- Claims-handling statements that imply guaranteed payout or coverage.

## Severity Rules

- **Green:** no obvious risky language; normal licensed review still required.
- **Yellow:** content may be usable after edits, missing disclosures, or source verification.
- **Red:** do not use until reviewed; contains guarantee language, replacement pressure, unapproved performance claims, disclosure problems, or vulnerable-customer risk.

## Review Procedure

1. Identify audience, channel, jurisdiction, and product line if known.
2. Quote the risky phrase exactly.
3. Explain why it is risky in practical terms.
4. Provide safer replacement language that preserves intent.
5. List missing disclosures or source verification.
6. State whether escalation is required.

## Output Format

```markdown
## Compliance Check

### Overall Risk
- Green / Yellow / Red:
- Reason:

### Required Fixes Before Use
1. Original text:
   - Issue:
   - Risk category:
   - Safer replacement:

### Optional Improvements
- ...

### Missing Disclosures / Assumptions
- ...

### Escalation Required?
- Yes/No
- Reason:

### Clean Draft, If Appropriate
[only include if risk is not Red or if the user asked for safer wording]
```

## Safer Language Patterns

Prefer:

- "may help address..." instead of "will cover..."
- "subject to policy terms, exclusions, underwriting, and carrier approval" instead of "guaranteed"
- "one option to consider" instead of "the best option"
- "draft for review" instead of "approved copy"
- "verify with the carrier/policy contract" instead of relying on brochure text

## Guardrails

- Do not mark customer-facing content as approved.
- Do not remove necessary caveats to make copy more persuasive.
- Do not produce fear-based, high-pressure, or misleading urgency language.
- Do not treat this workflow as legal or regulatory advice.
- Red-risk output must include a clear do-not-use-until-reviewed statement.
