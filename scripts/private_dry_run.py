#!/usr/bin/env python3
"""Run a read-only private dry-run before scheduled watcher deployment.

The harness chains existing local gates and scripts, writes diagnostic artifacts to
an explicit output directory outside the private workspace, and never creates a
live Hermes cron job.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT_NAMES = [
    "readiness-report.md",
    "readiness-report.json",
    "workbench-bundle.json",
    "workbench-bundle.md",
    "renewal-alert.json",
    "renewal-alert.md",
    "cron-simulation.md",
    "audit-trace.json",
    "audit-trace.md",
    "manifest.json",
    "deployment-checklist.md",
]


@dataclass
class StageResult:
    status: str
    exit_code: int
    command: list[str]
    stderr: str = ""


def fail(msg: str) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return 2


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def safe_workspace_file(path: Path, workspace: Path) -> bool:
    """Accept only regular files whose resolved target remains inside workspace."""
    if path.is_symlink() or not path.is_file():
        return False
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        return False
    return is_relative_to(resolved, workspace.resolve())


def workspace_files(workspace: Path) -> list[Path]:
    return sorted(p for p in workspace.rglob("*") if safe_workspace_file(p, workspace))


def workspace_inventory(workspace: Path) -> dict[str, dict[str, str | int]]:
    inventory: dict[str, dict[str, str | int]] = {}
    for path in workspace_files(workspace):
        rel = str(path.relative_to(workspace))
        inventory[rel] = {
            "path": rel,
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    return inventory


def assert_out_safe(workspace: Path, out: Path) -> tuple[bool, str]:
    out_abs = out.expanduser().resolve()
    if is_relative_to(out_abs, workspace):
        return False, f"out path must be outside workspace: {out_abs}"
    if out.exists():
        for source in workspace_files(workspace):
            try:
                if out.samefile(source):
                    return False, f"out path must not overwrite workspace file: {out_abs}"
            except FileNotFoundError:
                continue
    return True, str(out_abs)


def prepare_out_dir(out: Path, force: bool) -> None:
    if out.exists():
        if out.is_symlink():
            raise ValueError(f"out path must not be a symlink: {out}")
        if out.is_file():
            raise ValueError(f"out path must be a directory or absent: {out}")
        if any(out.iterdir()):
            if not force:
                raise ValueError(f"out path already exists and is not empty; pass --force to replace: {out}")
            shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)


def run_stage(command: list[str], *, ok_codes: set[int] | None = None) -> tuple[StageResult, subprocess.CompletedProcess[str]]:
    ok_codes = ok_codes or {0}
    proc = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status = "ok" if proc.returncode == 0 else "blocked" if proc.returncode in ok_codes else "failed"
    return StageResult(status=status, exit_code=proc.returncode, command=command, stderr=proc.stderr), proc


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def artifact_inventory(out: Path) -> dict[str, dict[str, str | int | bool | None]]:
    artifacts: dict[str, dict[str, str | int | bool | None]] = {}
    for name in ARTIFACT_NAMES:
        path = out / name
        if not path.exists() or not path.is_file():
            continue
        if name == "manifest.json":
            artifacts[name] = {
                "path": str(path),
                "size_bytes": None,
                "size_recorded": False,
                "sha256": "self-referential-not-recorded",
                "checksum_recorded": False,
            }
            continue
        artifacts[name] = {
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "size_recorded": True,
            "sha256": sha256(path),
            "checksum_recorded": True,
        }
    return artifacts


def source_inventory(before: dict[str, dict[str, str | int]], after: dict[str, dict[str, str | int]]) -> list[dict[str, str | int | bool]]:
    inventory: list[dict[str, str | int | bool]] = []
    for rel in sorted(set(before) | set(after)):
        before_item = before.get(rel)
        after_item = after.get(rel)
        inventory.append(
            {
                "path": rel,
                "operation": "read",
                "boundary": "regular in-workspace file",
                "size_bytes_before": before_item.get("size_bytes", 0) if before_item else 0,
                "size_bytes_after": after_item.get("size_bytes", 0) if after_item else 0,
                "sha256_before": before_item.get("sha256", "missing") if before_item else "missing",
                "sha256_after": after_item.get("sha256", "missing") if after_item else "missing",
                "unchanged": before_item == after_item,
            }
        )
    return inventory


def build_audit_trace(
    *,
    workspace: Path,
    as_of: str,
    readiness: dict,
    stages: dict[str, StageResult],
    workbench_bundle: dict,
    before_inventory: dict[str, dict[str, str | int]],
    after_inventory: dict[str, dict[str, str | int]],
) -> dict:
    inventory = source_inventory(before_inventory, after_inventory)
    unchanged = before_inventory == after_inventory and all(item["unchanged"] for item in inventory)
    return {
        "workflow": "Private Workspace Audit Trace",
        "trace_type": "audit-style trace",
        "workspace": str(workspace),
        "as_of": as_of,
        "read_only": True,
        "read_only_verified": unchanged,
        "workspace_unchanged": unchanged,
        "no_external_writes": True,
        "internal_only": True,
        "live_cron_created": False,
        "readiness_gate": {
            "mode": "readiness gate dry-run",
            "ready_for_cron": bool(readiness.get("ready_for_cron")),
            "risk_count": len(readiness.get("risks", [])) if isinstance(readiness.get("risks", []), list) else 0,
        },
        "stage_ledger": {name: stage_dict(stage) for name, stage in stages.items()},
        "source_inventory": inventory,
        "connector_source_trace": workbench_bundle.get("source_trace", []),
        "boundary_ledger": [
            "read-only local/private workspace connector only; source files are read, not mutated.",
            "readiness gate dry-run only; no live Hermes cron job is created.",
            "No External Writes: no customer sending, CRM writes, carrier contact, claims filing, application submission, or policy change.",
            "Artifacts are written only to the explicit output directory outside the private workspace.",
            "Trace records metadata and checksums only; private source content is not copied into audit-trace.json.",
        ],
    }


def render_audit_trace(trace: dict) -> str:
    lines = [
        "# Private Workspace Audit Trace",
        "",
        "audit-style trace for a read-only local/private workspace connector and readiness gate dry-run.",
        "",
        "## Boundary",
    ]
    for item in trace["boundary_ledger"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Read-Only Verification",
            f"- Read-only verified: {str(trace['read_only_verified']).lower()}",
            f"- Workspace unchanged: {str(trace['workspace_unchanged']).lower()}",
            "- No External Writes: true",
            "- Live Hermes cron created: false",
            "",
            "## Readiness Gate",
            "- Mode: readiness gate dry-run",
            f"- ready_for_cron: {str(trace['readiness_gate']['ready_for_cron']).lower()}",
            f"- Risk count: {trace['readiness_gate']['risk_count']}",
            "",
            "## Stage Ledger",
        ]
    )
    for name, stage in trace["stage_ledger"].items():
        lines.append(f"- {name}: {stage['status']} (exit {stage['exit_code']})")
    lines.extend(["", "## Source Files Checked"])
    for item in trace["source_inventory"]:
        lines.append(f"- `{item['path']}` — {item['operation']}; {item['boundary']}; unchanged: {str(item['unchanged']).lower()}")
    lines.extend(["", "## Connector Source Trace"])
    for item in trace["connector_source_trace"]:
        lines.append(f"- `{item['path']}` — {item['operation']}; {item['boundary']}; sha256: `{item['sha256']}`")
    if not trace["connector_source_trace"]:
        lines.append("- None recorded by connector bundle.")
    return "\n".join(lines).rstrip() + "\n"


def render_checklist(manifest: dict, readiness: dict) -> str:
    ready_label = "Ready for private dry-run gate" if manifest["ready_for_scheduled_watcher"] else "Blocked before scheduled watcher deployment"
    lines = [
        "# Private Dry-Run Deployment Checklist",
        "",
        "Draft for licensed/compliance/operations review.",
        "",
        "## Verdict",
        f"- {ready_label}",
        f"- As of: `{manifest['as_of']}`",
        f"- Workspace: `{manifest['workspace']}`",
        "- Read-only: true",
        "- No External Writes: true",
        "- Live Hermes cron created: false",
        "",
        "## Artifacts to Review",
    ]
    for name in ARTIFACT_NAMES:
        if name in manifest["artifacts"]:
            lines.append(f"- `{name}`")
    audit_trace = manifest.get("audit_trace", {})
    if audit_trace:
        lines.extend(
            [
                "",
                "## Audit Trace",
                "- Audit trace: `audit-trace.json`",
                "- Audit trace summary: `audit-trace.md`",
                f"- Source files checked: {audit_trace.get('source_files_checked', 0)}",
                f"- Workspace unchanged: {str(manifest.get('workspace_unchanged', False)).lower()}",
                f"- Read-only verified: {str(manifest.get('read_only_verified', False)).lower()}",
            ]
        )
    lines.extend([
        "",
        "## Gate Checks",
        f"- Readiness: {manifest['stages']['readiness']['status']} (exit {manifest['stages']['readiness']['exit_code']})",
        f"- Connector bundle: {manifest['stages']['connector_json']['status']} (exit {manifest['stages']['connector_json']['exit_code']})",
        f"- Renewal watcher: {manifest['stages']['renewal_json']['status']} (exit {manifest['stages']['renewal_json']['exit_code']})",
        f"- Cron wrapper simulation: {manifest['stages']['cron_simulation']['status']} (exit {manifest['stages']['cron_simulation']['exit_code']})",
        "",
        "## Before Any Live Scheduled Job",
        "- Resolve all readiness blockers.",
        "- Confirm schedule, timezone, delivery target, reviewer, and retention/audit owner.",
        "- Keep any future Hermes job `no_agent=True` unless an explicitly reviewed summary job is added.",
        "- If an LLM summary job is later added, use per-job model override `custom:fufu` / `mimo-v2.5-pro` instead of changing global model config.",
        "- Preserve `[verify]` markers and internal-only wording.",
        "",
        "## Safety Boundary",
        "- This dry run did not create a live Hermes cron job.",
        "- It did not send customer messages, write CRM/calendar tasks, contact carriers, file claims, submit applications, or change policies.",
        "- No External Writes.",
    ])
    risks = readiness.get("risks", []) if isinstance(readiness, dict) else []
    if risks:
        lines.extend(["", "## Readiness Risks"])
        for risk in risks:
            lines.append(f"- {risk.get('severity')} / {risk.get('id')}: {risk.get('detail')}")
    return "\n".join(lines) + "\n"


def compute_ready_for_scheduled_watcher(
    *,
    readiness: dict,
    stages: dict[str, StageResult],
    audit_trace: dict,
) -> bool:
    """Final scheduled-watcher readiness is fail-closed on audit trace evidence."""
    required_stage_keys = ["connector_json", "connector_markdown", "renewal_json", "renewal_markdown", "cron_simulation"]
    child_stages_ok = all(stages[key].exit_code == 0 for key in required_stage_keys)
    audit_read_only_ok = audit_trace.get("read_only_verified") is True and audit_trace.get("workspace_unchanged") is True
    return bool(readiness.get("ready_for_cron")) and child_stages_ok and audit_read_only_ok


def stage_dict(stage: StageResult) -> dict:
    return {
        "status": stage.status,
        "exit_code": stage.exit_code,
        "command": stage.command,
        "stderr": stage.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only private dry-run harness before scheduled watcher deployment")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-stale-days", type=int, default=7)
    parser.add_argument("--synthetic-mode", action="store_true")
    parser.add_argument("--force", action="store_true", help="Replace existing non-empty output directory")
    args = parser.parse_args()

    workspace_input = args.workspace.expanduser()
    if workspace_input.is_symlink():
        return fail(f"workspace path must not be a symlink: {workspace_input}")
    workspace = workspace_input.resolve()
    if not workspace.exists() or not workspace.is_dir():
        return fail(f"workspace missing: {workspace}")
    before_inventory = workspace_inventory(workspace)
    ok, msg = assert_out_safe(workspace, args.out)
    if not ok:
        return fail(msg)
    out = Path(msg)
    try:
        prepare_out_dir(out, args.force)
    except ValueError as exc:
        return fail(str(exc))

    stages: dict[str, StageResult] = {}

    readiness_json = out / "readiness-report.json"
    readiness_cmd = [
        "python3",
        "scripts/private_workspace_readiness.py",
        "--workspace",
        str(workspace),
        "--as-of",
        args.as_of,
        "--max-stale-days",
        str(args.max_stale_days),
        "--format",
        "json",
        "--output",
        str(readiness_json),
    ]
    if args.synthetic_mode:
        readiness_cmd.append("--synthetic-mode")
    stages["readiness"], proc = run_stage(readiness_cmd, ok_codes={0, 1})
    if proc.returncode not in {0, 1}:
        print(stages["readiness"].stderr, file=sys.stderr, end="")
        return 2

    readiness_md = out / "readiness-report.md"
    readiness_md_cmd = readiness_cmd.copy()
    readiness_md_cmd[readiness_md_cmd.index("json")] = "markdown"
    readiness_md_cmd[readiness_md_cmd.index(str(readiness_json))] = str(readiness_md)
    stages["readiness_markdown"], proc_md = run_stage(readiness_md_cmd, ok_codes={0, 1})
    if proc_md.returncode not in {0, 1}:
        print(stages["readiness_markdown"].stderr, file=sys.stderr, end="")
        return 2

    readiness = json.loads(readiness_json.read_text(encoding="utf-8"))

    workbench_json = out / "workbench-bundle.json"
    cmd = ["python3", "scripts/local_file_connectors.py", "daily-workbench", "--workspace", str(workspace), "--format", "json", "--output", str(workbench_json)]
    stages["connector_json"], proc = run_stage(cmd)
    if proc.returncode != 0:
        print(stages["connector_json"].stderr or proc.stdout, file=sys.stderr, end="")
        return 2

    workbench_md = out / "workbench-bundle.md"
    cmd = ["python3", "scripts/local_file_connectors.py", "daily-workbench", "--workspace", str(workspace), "--format", "markdown", "--output", str(workbench_md)]
    stages["connector_markdown"], proc = run_stage(cmd)
    if proc.returncode != 0:
        print(stages["connector_markdown"].stderr or proc.stdout, file=sys.stderr, end="")
        return 2

    renewal_json = out / "renewal-alert.json"
    cmd = ["python3", "scripts/renewal_watcher.py", "--bundle", str(workbench_json), "--workspace", str(workspace), "--as-of", args.as_of, "--format", "json", "--output", str(renewal_json)]
    stages["renewal_json"], proc = run_stage(cmd)
    if proc.returncode != 0:
        print(stages["renewal_json"].stderr or proc.stdout, file=sys.stderr, end="")
        return 2

    renewal_md = out / "renewal-alert.md"
    cmd = ["python3", "scripts/renewal_watcher.py", "--bundle", str(workbench_json), "--workspace", str(workspace), "--as-of", args.as_of, "--format", "markdown", "--output", str(renewal_md)]
    stages["renewal_markdown"], proc = run_stage(cmd)
    if proc.returncode != 0:
        print(stages["renewal_markdown"].stderr or proc.stdout, file=sys.stderr, end="")
        return 2

    cron_simulation = out / "cron-simulation.md"
    cmd = ["bash", "cron/scripts/renewal_watcher.sh", "--workspace", str(workspace), "--as-of", args.as_of, "--mode", "always", "--format", "markdown", "--output", str(cron_simulation)]
    stages["cron_simulation"], proc = run_stage(cmd)
    if proc.returncode != 0:
        print(stages["cron_simulation"].stderr or proc.stdout, file=sys.stderr, end="")
        return 2

    workbench_bundle = json.loads(workbench_json.read_text(encoding="utf-8"))
    after_inventory = workspace_inventory(workspace)
    audit_trace = build_audit_trace(
        workspace=workspace,
        as_of=args.as_of,
        readiness=readiness,
        stages=stages,
        workbench_bundle=workbench_bundle,
        before_inventory=before_inventory,
        after_inventory=after_inventory,
    )
    write_text(out / "audit-trace.json", json.dumps(audit_trace, indent=2, sort_keys=True) + "\n")
    write_text(out / "audit-trace.md", render_audit_trace(audit_trace))
    ready = compute_ready_for_scheduled_watcher(readiness=readiness, stages=stages, audit_trace=audit_trace)

    manifest: dict = {
        "workflow": "Private Dry-Run Deployment Harness",
        "workspace": str(workspace),
        "as_of": args.as_of,
        "ready_for_scheduled_watcher": ready,
        "read_only": True,
        "read_only_verified": audit_trace["read_only_verified"],
        "workspace_unchanged": audit_trace["workspace_unchanged"],
        "no_external_writes": True,
        "internal_only": True,
        "live_cron_created": False,
        "review_notice": "Draft diagnostics for licensed/compliance/operations review; no live Hermes cron job was created.",
        "stages": {name: stage_dict(stage) for name, stage in stages.items()},
        "audit_trace": {
            "path": str(out / "audit-trace.json"),
            "markdown_path": str(out / "audit-trace.md"),
            "source_files_checked": len(audit_trace["source_inventory"]),
            "connector_source_files_checked": len(audit_trace["connector_source_trace"]),
        },
        "artifacts": {},
    }

    checklist = render_checklist(manifest | {"artifacts": {name: {} for name in ARTIFACT_NAMES}}, readiness)
    write_text(out / "deployment-checklist.md", checklist)
    # `manifest.json` is self-referential: embedding its own final digest would change
    # the file. Record every other artifact checksum and mark the manifest checksum as
    # intentionally not recorded.
    write_text(out / "manifest.json", "{}\n")
    manifest["artifacts"] = artifact_inventory(out)
    checklist = render_checklist(manifest, readiness)
    write_text(out / "deployment-checklist.md", checklist)
    manifest["artifacts"] = artifact_inventory(out)
    write_text(out / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print(f"Private dry-run deployment harness complete: {out}")
    print(f"Ready for scheduled watcher: {str(ready).lower()}")
    print("Live Hermes cron created: false")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
