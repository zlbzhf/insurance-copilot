# Local Renewal Watcher

The Local Renewal Watcher is the first scheduled-managed-agent-ready slice for Insurance Copilot. It turns a synthetic/private renewal register or a local connector JSON bundle into an **internal-only** renewal/lapse alert.

It is deliberately conservative:

- reads local files only;
- stdout by default;
- optional `--output` only when explicitly requested;
- no customer messages;
- no CRM/calendar writes;
- no carrier portal calls;
- no coverage/lapse/reinstatement conclusions without `[verify]`.

## Input Options

### Option A: local connector JSON bundle

```bash
python3 scripts/local_file_connectors.py daily-workbench \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --format json \
  --output /tmp/insurance-workbench-bundle.json

python3 scripts/renewal_watcher.py \
  --bundle /tmp/insurance-workbench-bundle.json \
  --as-of 2026-05-14 \
  --format markdown
```

### Option B: direct renewal register CSV

```bash
python3 scripts/renewal_watcher.py \
  --csv examples/local-connectors/synthetic-agent-workspace/renewal-registers/synthetic-renewal-register.csv \
  --as-of 2026-05-14 \
  --format markdown
```

## Output Options

Default is stdout. If writing a report, write outside the private workspace:

```bash
python3 scripts/renewal_watcher.py \
  --bundle /tmp/insurance-workbench-bundle.json \
  --as-of 2026-05-14 \
  --format markdown \
  --output /tmp/insurance-renewal-alert.md
```

When `--workspace` is supplied, direct CSV inputs must remain inside that workspace. JSON bundles may live outside the workspace, such as `/tmp`, because they are generated artifacts; the watcher still rejects symlinked or non-regular bundle files and uses `--workspace` to protect report output paths. Direct CSV paths under `renewal-registers/` are treated as belonging to the parent workspace for output-contamination protection, even when `--workspace` is omitted. The watcher also refuses to overwrite the input file, including same-file/hard-link aliases:

```bash
python3 scripts/renewal_watcher.py \
  --csv ~/.insurance-copilot/agents/synthetic/renewal-registers/register.csv \
  --workspace ~/.insurance-copilot/agents/synthetic \
  --as-of 2026-05-14 \
  --output /tmp/insurance-renewal-alert.md
```

## Buckets

The watcher classifies rows into conservative internal buckets:

- `D-30`
- `D-14`
- `D-7`
- `D+1`
- `in-grace-period`
- `grace-period-before-end`
- `grace-ended`
- `verify-status`
- `monitor`

These buckets are **not** binding status determinations. They are work-queue labels to help the licensed agent verify current carrier/payment facts.

## Internal Alert Requirements

Every alert includes:

- `internal_only: true` in JSON;
- `no_external_writes: true` in JSON;
- `Draft for licensed/compliance review` in Markdown;
- `[verify]` status language;
- `No External Writes` section;
- neutral internal follow-up language only.

## Checked Script-only Wrapper

Use the checked wrapper for dry runs and future `no_agent=True` cron deployment:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace examples/local-connectors/synthetic-agent-workspace \
  --as-of 2026-05-14 \
  --mode always
```

For alert-only behavior:

```bash
bash cron/scripts/renewal_watcher.sh \
  --workspace ~/.insurance-copilot/agents/<agent-id> \
  --as-of "$(date +%F)" \
  --mode alert-only
```

In Hermes `no_agent=True` cron, non-empty stdout is delivered, empty stdout is silent/no-alert, and non-zero exit is an error alert. See `docs/script-only-cron-wrapper.md`.

## Script-only Cron Pattern

A future Hermes cron job can run this as a script-only watchdog. Do not create a live job until the private workspace path, schedule, reviewer, and compliance boundary are approved.

Example script wrapper:

```bash
#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="$HOME/.insurance-copilot/agents/<agent-id>"
BUNDLE="/tmp/insurance-workbench-bundle.json"
ALERT="/tmp/insurance-renewal-alert.md"
python3 scripts/local_file_connectors.py daily-workbench \
  --workspace "$WORKSPACE" \
  --format json \
  --output "$BUNDLE" >/dev/null
python3 scripts/renewal_watcher.py \
  --bundle "$BUNDLE" \
  --workspace "$WORKSPACE" \
  --as-of "$(date +%F)" \
  --format markdown \
  --output "$ALERT" >/dev/null
cat "$ALERT"
```

For scheduled summary jobs, the user may choose a per-job Hermes model override such as `custom:fufu` / `mimo-v2.5-pro` without changing global model configuration.

## Guardrails

- Do not pipe this alert into a sender.
- Do not treat bucket labels as coverage, lapse, reinstatement, claim, or underwriting conclusions.
- Verify official carrier/payment status before any customer statement.
- Verify contact consent and approved scripts before outreach.
- Escalate grace-period, grace-ended, complaint, vulnerable-customer, replacement, or ambiguous-status items.


Safety note: if `TMPDIR` is set for the wrapper, it must resolve outside the private workspace; broken child commands should fail loudly with stderr rather than silently exiting.
