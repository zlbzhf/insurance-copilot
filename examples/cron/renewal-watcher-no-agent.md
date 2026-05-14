# Synthetic no-agent Renewal Watcher Example

This example shows the intended Hermes script-only cron shape without creating a live job.

## Dry Run

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --mode always
```

Expected stdout includes:

```text
# Internal Renewal Watcher Alert
Draft for licensed/compliance review
[verify]
No External Writes
```

## Alert-only Watchdog Mode

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --mode alert-only
```

For `no_agent=True` Hermes jobs:

- non-empty stdout is delivered as the alert;
- empty stdout is silent/no-alert;
- non-zero exit is delivered as an error alert.

## Live Job Shape After Approval

Do not create this job until the private workspace path, schedule, reviewer, and compliance boundary are approved.

```python
cronjob(
    action="create",
    name="insurance renewal watcher",
    schedule="0 8 * * 1-5",
    script="renewal_watcher.sh",
    no_agent=True,
    deliver="origin",
    enabled_toolsets=["terminal"],
)
```

## Optional LLM Summary

If a later summary job is approved, use a per-job model override, not a global Hermes model change:

```python
model={"provider": "custom:fufu", "model": "mimo-v2.5-pro"}
```

The summary job must preserve `[verify]`, avoid send-ready customer language, and avoid any coverage/lapse/reinstatement conclusion.


Safety note: if `TMPDIR` is set for the wrapper, it must resolve outside the private workspace; broken child commands should fail loudly with stderr rather than silently exiting.

Repo-root note: the wrapper expects repository-relative helper scripts. For real Hermes deployment, use this repository as the job `workdir`, or copy the wrapper together with the required `scripts/local_file_connectors.py` and `scripts/renewal_watcher.py`; do not copy only the shell wrapper unless relative helper-script access is preserved.
