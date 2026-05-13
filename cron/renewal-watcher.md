# Renewal Watcher Cron Recipe

Use Hermes cron to periodically review a renewal register exported by the agency.

Recommended prompt shape:

```text
Load the insurance-copilot skill. Review the renewal register at <path>. Identify policies with due, grace-period, lapse, or review windows in the next 30 days. Produce internal draft outreach only. Mark all carrier status as [verify with carrier]. Do not send customer messages.
```

Required toolsets: `file`, optionally `web` if regulator/carrier public checks are needed.
