# Script-only Cron Wrapper

`cron/scripts/renewal_watcher.sh` is a deployable template for running the Local Renewal Watcher as a Hermes script-only watchdog. It is intentionally **not** a live scheduled job in this repository.

## Purpose

This wrapper turns the previous manual sequence:

```text
local workspace -> local_file_connectors.py -> renewal_watcher.py -> internal alert
```

into a single script suitable for later Hermes cron `no_agent=True` use:

```text
cron/scripts/renewal_watcher.sh -> stdout alert or silent no-alert
```

## Safety Model

The wrapper:

- reads a local private workspace only;
- creates temporary connector/report artifacts outside the workspace;
- rejects `TMPDIR` if it resolves inside the private workspace;
- prints to stdout by default;
- writes to `--output` only when explicitly requested;
- rejects `--output` inside the workspace;
- has no network calls;
- sends no customer messages;
- writes no CRM/calendar tasks;
- does not contact carrier portals;
- preserves `[verify]`, `No External Writes`, and licensed/compliance review language from the watcher.

## Commands

Always-print mode, useful for dry runs:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --mode always
```

Alert-only mode, useful for no-agent cron:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --mode alert-only
```

Write a reviewed artifact outside the workspace:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --mode always \
  --output /tmp/insurance-renewal-alert.md
```

JSON output for downstream deterministic checks:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --mode always \
  --format json
```

## `no_agent=True` Semantics

Hermes script-only cron behavior should be treated as follows:

- **Non-empty stdout:** deliver the stdout verbatim as the alert.
- **Empty stdout:** silent no-alert; the user sees nothing.
- **Non-zero exit:** error alert; broken configuration must fail loudly and include child command output on stderr.

That is why `--mode alert-only` suppresses monitor-only output and exits `0` with empty stdout.

## Example Hermes Cron Tool Shape

Do **not** create this live job until the private workspace path, schedule, reviewer, and compliance boundary are approved.

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

For this repository, prefer running the script from this repo with a project `workdir`, or copy the full repository-aware wrapper plus helper scripts together. Do not copy only `renewal_watcher.sh` into `~/.hermes/scripts/` unless you also preserve its relative access to `scripts/local_file_connectors.py` and `scripts/renewal_watcher.py`. `TMPDIR` must resolve outside the workspace.

## Optional LLM Summary Job

A separate LLM summary job may be added after approval. For the user's scheduled update/check/report jobs, use a per-job model override rather than changing global Hermes configuration:

```python
model={"provider": "custom:fufu", "model": "mimo-v2.5-pro"}
```

The summary prompt must be self-contained and must say:

- summarize internal-only alert output;
- preserve `[verify]` markers;
- do not draft send-ready customer messages;
- do not claim coverage is active, lapsed, or reinstated;
- output urgent internal items, verification checklist, escalation list, and reviewed task notes only.

## Private Workspace Readiness Gate

Run the private workspace readiness gate before wrapper dry runs on real private data:

```bash
python3 scripts/private_workspace_readiness.py \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --format markdown
```

Run the private workspace readiness gate before wrapper dry runs on real private data. Resolve blocker risks before creating or enabling any scheduled watcher.

## Deployment Checklist

Before creating a live job:

- confirm the private workspace path;
- confirm schedule and timezone;
- confirm reviewer/owner;
- confirm data retention and log policy;
- run synthetic dry run;
- run one private dry run with no delivery;
- verify empty stdout behavior on a monitor-only register;
- verify non-zero exit on a deliberately missing workspace.
