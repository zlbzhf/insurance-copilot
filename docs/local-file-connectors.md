# Local File Connectors

Local file connectors are the first read-only connector slice for Insurance Copilot. They turn private-workspace-shaped local files into a Daily Agent Workbench bundle that can be pasted into Hermes after loading the `insurance-copilot` skill.

This is intentionally not a production CRM/carrier integration. It reads local Markdown/CSV files and emits Markdown or JSON. It does not send messages, update CRM/calendar systems, contact carriers, file claims, submit applications, or change policies.

## Supported Inputs

From a private workspace or synthetic fixture:

- `clients/` or `customers/` Markdown customer/profile pages;
- `meetings/` Markdown meeting notes;
- `policies/` Markdown policy summaries;
- `renewal-registers/*.csv` renewal/lapse rows;
- `claims/` Markdown claim-support trackers;
- `referrals/` Markdown referral trackers;
- `tasks/` Markdown task lists.

All product, policy, payment, claim, and referral facts that are missing or stale remain `[verify]`.

## Developer Test Dependency

Install developer test dependencies before running pytest locally or in CI:

```bash
python3 -m pip install -r requirements-dev.txt
```

## Markdown Bundle

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format markdown
```

Use the output as input to Hermes:

```text
/skill insurance-copilot
Use Daily Agent Workbench on this connector bundle. Preserve [verify] markers, do not send or write anything automatically, and produce licensed/compliance review drafts only.
```

## JSON Bundle

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format json
```

The JSON includes:

- `read_only: true`;
- `no_external_writes: true`;
- normalized counts;
- renewal rows;
- customer/meeting/policy/claim/referral/task records;
- high-risk items;
- verify-before-action checklist;
- `source_trace`: metadata-only provenance for every regular in-workspace file read by the connector. Each entry records relative path, `operation: read`, `boundary: regular in-workspace file`, size, and SHA-256; it never copies source content into the trace.

## Explicit Output File

Stdout is the default. Writing requires an explicit `--output` path:

```bash
python3 scripts/local_file_connectors.py daily-workbench   --workspace examples/local-connectors/synthetic-agent-workspace   --format markdown   --output /tmp/insurance-daily-workbench.md
```

Do not commit real private bundles. Public repo examples must remain synthetic or fully de-identified. The output path must be outside the workspace so generated bundles cannot overwrite input records.

## Private Workspace Trace and Readiness Gate

Connector JSON/Markdown includes `source_trace` so the **Private Workspace Trace and Readiness Gate** can review a **Private Workspace Audit Trace** as a **read-only local/private workspace connector**. The trace is **metadata/checksums only** and supports `read_only_verified`, `workspace_unchanged`, **readiness gate dry-run**, **audit-style trace**, **No External Writes**, `live_cron_created: false`, and **no live automation** decisions when paired with the private dry-run harness.

## Safety Boundaries

- Read-only local files only.
- Symlinked input files are skipped so the connector does not read outside the workspace.
- No network calls.
- No CRM/calendar writes.
- No customer messaging.
- No carrier status assertions unless a current source is supplied and still cited.
- No final recommendations, claim decisions, underwriting decisions, or compliance approvals.

## Production Path Later

A future production connector should keep this shape but replace local files with approved read-only MCP/data connectors, least-privilege auth, audit logging, retention rules, and institution compliance review.
