# Insurance Agent Managed-Agent Cookbooks

These mirror the scheduled-agent idea from `claude-for-legal`, adapted to insurance agency operations.

## 1. Renewal Watcher

**Cadence:** daily or weekly.

**Inputs:** policy register, premium due dates, grace periods, customer contact rules.

**Output:** grouped list of urgent renewal/lapse actions with draft outreach.

**Human gate:** agent verifies status with carrier before telling customer coverage status.

## 2. Compliance Copy Monitor

**Cadence:** on new marketing copy or weekly folder scan.

**Inputs:** draft ads, scripts, seminar slides, social posts.

**Output:** Green/Yellow/Red compliance review and safer language suggestions.

**Human gate:** compliance approves before external use.

## 3. Replacement Risk Monitor

**Cadence:** on proposal creation or daily CRM scan.

**Inputs:** proposals referencing cancellation, surrender, transfer, replacement, or policy loan.

**Output:** list of cases requiring replacement analysis and supervisor review.

**Human gate:** no customer instruction to replace coverage before formal review.

## 4. Playbook Drift Monitor

**Cadence:** monthly.

**Inputs:** deviation log, compliance corrections, manager overrides.

**Output:** proposed updates to agency practice profile.

**Human gate:** manager/compliance approves profile changes.
