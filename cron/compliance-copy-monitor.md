# Compliance Copy Monitor Cron Recipe

Use Hermes cron to review a folder of draft ads, posts, scripts, emails, or renewal messages before reuse.

## Recommended Prompt

```text
Load the insurance-copilot skill. Review markdown/text files under <path> using references/compliance-check.md. Output only risk findings, exact risky phrases, safer replacement language, and escalation requirements. Do not publish, send, edit live production files, or mark content approved.
```

## Safety

- No publishing.
- No customer sending.
- Red-risk content must say: do not use until reviewed.
- Preserve exact risky phrases for reviewer traceability.
