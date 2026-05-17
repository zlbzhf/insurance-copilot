---
name: coach_me
description: "Use when the user brings a messy, incomplete, or strategic question. Iteratively ask the next most useful question until enough information exists to form a structured working document and recommend a next route or action."
version: 1.0.0
author: Insurance Copilot Project
license: MIT
metadata:
  hermes:
    tags: [questioning, reasoning, workflow, decision-support, clarification]
    related_skills: []
---

# Coach_me

## Overview

Coach_me is a questioning-to-document method. It takes a messy, incomplete, or strategic question and converts it into a structured working document through iterative, issue-specific questioning.

It is inspired by [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) (relentless one-question-at-a-time interviewing) and [`grill-with-docs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs) (questioning that sharpens terminology and crystallizes decisions into lightweight documents). Coach_me adapts these methods into a general-purpose fact-development workflow: **question → obtain information → form a working document → recommend next route**.

Coach_me is **not**:
- Domain-specific;
- A fixed questionnaire;
- A newcomer coach or training mode;
- A decision engine or advice system.

It is a **method**: the thing you do before you apply specialized knowledge.

---

## When to Use

Use Coach_me when:

- The user asks a broad or strategic question whose answer depends on facts not yet stated;
- The user provides an incomplete situation, problem, or decision point;
- The user asks "what should I do?" or "how should I think about this?";
- The available context or supplied sources are insufficient for a safe, accurate, or useful answer;
- A one-shot answer would likely miss material facts, risks, or alternatives.

Do **not** use Coach_me for:

- Simple lookups or factual queries the available sources already answer;
- Direct formatting requests with all needed facts supplied;
- Administrative or technical tasks with a clear known state;
- Any scenario where the next step is already obvious and safe;
- Making binding decisions, predictions, guarantees, or giving regulated advice.

---

## Process

### 1. Triage and Initialize

Classify the type of situation. Start a **Coach_me Working Document** with whatever is already known, then assess the gap between what you know and what you need.

### 2. Check Available Context First

Before asking any question, check whether the answer can be obtained from:
- The current conversation or context;
- Supplied documents, files, or sources;
- Existing knowledge bases, profiles, or reference materials available to you.

If you can find the answer without asking, use it. Do not ask questions you can answer yourself.

### 3. Ask the Next Most Useful Question

Ask exactly **one question** (in conversational interfaces) or up to three (when the user requests a batch/checklist). Each question must be the single most useful clarification for the current situation.

For each question:
- State what you need to know and why it matters;
- Provide a **recommended default answer** — useful when the user is unsure or wants to move faster;
- Keep it focused on the current gap, not a broad survey.

### 4. After Each Answer, Update the Working Document

Add what was learned. Reassess whether more questions are still needed.

### 5. Choice Point

After a question round, offer a choice:
- **Answer now** — produce the best current document with everything marked as confirmed or unconfirmed.
- **Continue questioning** — ask another round, only if the next question materially improves the document.

### 6. Stop When Information Is Sufficient

Stop questioning when:
- The remaining unknowns do not materially change the recommended next action;
- The answer would become more burdensome than useful;
- Source facts are unavailable and must simply be marked as needing verification;
- The user asks to stop and answer from current facts.

### 7. Output the Working Document

Produce the final **Coach_me Working Document**. It should capture:
- What was asked;
- What is known;
- What is still pending or unconfirmed;
- A recommended next route or action;
- Whether the current output is safe to act on, needs human review, or needs more sources.

---

## Questioning Rules

- **Not a fixed count.** Do not require exactly three questions every time. Stop when sufficient.
- **Not a fixed format.** Do not require Direction/Risk/Source/Action or any other fixed categories every time. The question content depends on the situation.
- **One at a time in conversational mode.** In interactive chat, send one question per turn. Batch only when the user requests a written checklist to complete offline.
- **Dynamic, not frozen.** Each question must be generated from the current issue, available sources, missing information, and intended action, not from a predetermined script.
- **Default for unsure users.** When the user says "I don't know" or seems unsure, accept the recommended default answer, mark it `[verify]` / needs confirmation, and continue.
- **Automatic stop.** Stop when information is sufficient. The user may also stop at any time and request a current-state answer.

---

## Output: Coach_me Working Document

The output is a structured document, not just conversation. Use `templates/working-document.md` for the standard format.

The minimum fields are:

```markdown
## Coach_me Working Document

### Situation
- Trigger:
- Classification:

### Known Facts
- ...
### Pending Verification
- ...
### Working Understanding
- ...
### Information Sufficiency
- Is there enough to proceed? yes / partial / no
- Safest next action:
- What is still missing:
### Recommended Route
- Suggested next workflow, skill, or action:
### Output State
- Safe to use now / needs human review / needs more sources
```

---

## Route Recommendation

After the working document is formed, recommend the next route. The recommended route is **not** part of Coach_me itself — it is a handoff to the appropriate domain-specific skill, workflow, or human:

```text
Coach_me Working Document → route recommendation → domain-specific skill or workflow
```

Examples:
- `insurance_copilot` (insurance domain) — for insurance agent workflows;
- `claims-triage` — for claims-related decisions;
- Any other domain skill that consumes structured working documents;
- Human review, when the situation requires judgment Coach_me is not designed for.

Coach_me does not execute the next step. It prepares the input.

---

## Relationship to Domain Skills

Coach_me works alongside domain-specific skills:

- **Coach_me** provides the general method: ask → learn → document → route.
- **Domain skills** (e.g. insurance_copilot, legal-assistant, medical-triage) provide the domain knowledge, safety rules, compliance boundaries, and final output format.

When a domain skill is loaded together with Coach_me, Coach_me handles fact development; the domain skill handles domain-specific judgment, guardrails, and output.

---

## Common Pitfalls

1. **Fixing the question count.** Asking exactly three questions when two are sufficient (or three are not enough) makes the user answer unnecessary questions. Stop when sufficient.

2. **Fixing the question content.** `Direction / Risk / Source / Action` is one possible frame, not the universal frame. Choose questions that fit the situation.

3. **Asking what you can look up.** Before any question, check whether available context, sources, or tools can answer it first.

4. **Forgetting the recommended default answer.** Unsure users benefit from "here's what I'd assume" as a conversational shortcut, with a `[verify]` marker.

5. **Outputting raw chat instead of a structured document.** The output should be a reusable working document, not just conversation summary.

6. **Performing the recommended action inside Coach_me.** Coach_me forms the document and recommends the route; the domain skill or human performs the action.

7. **Domain contamination.** Do not hardcode insurance-specific, legal-specific, or other domain-specific rules into Coach_me. Domain rules belong in domain skills.

---

## Verification Checklist

- [ ] Generic — no domain-specific rules, markers, or templates.
- [ ] Concise — method definition fits in a page or two.
- [ ] No fixed question count or fixed categories in the method description.
- [ ] Dynamic questioning — each question based on current issue.
- [ ] Check available context before asking.
- [ ] One question at a time in conversational interfaces.
- [ ] Recommended default answer included when useful.
- [ ] Choice point after each round: answer now or continue.
- [ ] Automatic stop when sufficient.
- [ ] Structured working document output.
- [ ] Route recommendation, not action execution.
- [ ] No domain-specific terms, markers, or guardrails.
