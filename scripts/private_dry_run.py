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


def workspace_files(workspace: Path) -> list[Path]:
    return sorted(p for p in workspace.rglob("*") if p.is_file() and not p.is_symlink())


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


def artifact_inventory(out: Path) -> dict[str, dict[str, str | int | bool]]:
    artifacts: dict[str, dict[str, str | int | bool]] = {}
    for name in ARTIFACT_NAMES:
        path = out / name
        if not path.exists() or not path.is_file():
            continue
        if name == "manifest.json":
            artifacts[name] = {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": "self-referential-not-recorded",
                "checksum_recorded": False,
            }
            continue
        artifacts[name] = {
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "checksum_recorded": True,
        }
    return artifacts


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

    ready = bool(readiness.get("ready_for_cron")) and all(stages[key].exit_code == 0 for key in ["connector_json", "connector_markdown", "renewal_json", "renewal_markdown", "cron_simulation"])

    manifest: dict = {
        "workflow": "Private Dry-Run Deployment Harness",
        "workspace": str(workspace),
        "as_of": args.as_of,
        "ready_for_scheduled_watcher": ready,
        "read_only": True,
        "no_external_writes": True,
        "internal_only": True,
        "live_cron_created": False,
        "review_notice": "Draft diagnostics for licensed/compliance/operations review; no live Hermes cron job was created.",
        "stages": {name: stage_dict(stage) for name, stage in stages.items()},
        "artifacts": {},
    }

    checklist = render_checklist(manifest | {"artifacts": {name: {} for name in ARTIFACT_NAMES}}, readiness)
    write_text(out / "deployment-checklist.md", checklist)
    # `manifest.json` is self-referential: embedding its own final digest would change
    # the file. Record every other artifact checksum and mark the manifest checksum as
    # intentionally not recorded.
    write_text(out / "manifest.json", "{}\n")
    manifest["artifacts"] = artifact_inventory(out)
    write_text(out / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print(f"Private dry-run deployment harness complete: {out}")
    print(f"Ready for scheduled watcher: {str(ready).lower()}")
    print("Live Hermes cron created: false")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
