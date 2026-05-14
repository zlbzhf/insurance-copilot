#!/usr/bin/env python3
"""Tests for the private dry-run deployment harness."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "private_dry_run.py"

FIELDNAMES = [
    "customer_ref",
    "policy_ref",
    "carrier",
    "product_category",
    "premium_due_date",
    "grace_period_end",
    "status_source",
    "status_as_of",
    "last_contact",
    "next_action",
    "review_flags",
]
EXPECTED_ARTIFACTS = [
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


def run_dry_run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def write_workspace(tmp_path: Path, rows: list[dict[str, str]], *, include_retention: bool = True) -> Path:
    ws = tmp_path / "workspace"
    for folder in ["clients", "meetings", "policies", "claims", "referrals", "tasks", "renewal-registers"]:
        (ws / folder).mkdir(parents=True, exist_ok=True)
    (ws / "README.md").write_text("# Private workspace\n\nDo not publish. No External Writes.\n", encoding="utf-8")
    if include_retention:
        (ws / "RETENTION.md").write_text(
            "# Retention / Audit\n\n- retention owner: SYN agent\n- audit log: log.md\n- deletion review cadence: monthly\n",
            encoding="utf-8",
        )
    (ws / "log.md").write_text("# Log\n\n## [2026-05-14]\n- synthetic update\n", encoding="utf-8")
    with (ws / "renewal-registers" / "synthetic-renewal-register.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return ws


def fresh_actionable_rows() -> list[dict[str, str]]:
    return [
        {
            "customer_ref": "SYN-CUSTOMER-001",
            "policy_ref": "SYN-POLICY-001",
            "carrier": "Example Carrier",
            "product_category": "life",
            "premium_due_date": "2026-05-20",
            "grace_period_end": "2026-06-20",
            "status_source": "carrier export",
            "status_as_of": "2026-05-14",
            "last_contact": "",
            "next_action": "verify payment status",
            "review_flags": "possible lapse risk",
        }
    ]


def workspace_hashes(workspace: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(p for p in workspace.rglob("*") if p.is_file() and not p.is_symlink()):
        hashes[str(path.relative_to(workspace))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def assert_expected_artifacts(out: Path) -> None:
    for name in EXPECTED_ARTIFACTS:
        assert (out / name).is_file(), name


def test_synthetic_workspace_generates_complete_diagnostic_bundle(tmp_path: Path) -> None:
    out = tmp_path / "dry-run"

    proc = run_dry_run(
        "--workspace",
        "examples/local-connectors/synthetic-agent-workspace",
        "--as-of",
        "2026-05-14",
        "--out",
        str(out),
    )

    assert proc.returncode == 1, proc.stderr + proc.stdout
    assert "Private dry-run deployment harness complete" in proc.stdout
    assert_expected_artifacts(out)
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["workflow"] == "Private Dry-Run Deployment Harness"
    assert manifest["read_only"] is True
    assert manifest["no_external_writes"] is True
    assert manifest["live_cron_created"] is False
    assert manifest["ready_for_scheduled_watcher"] is False
    assert manifest["stages"]["readiness"]["exit_code"] == 1
    assert set(manifest["artifacts"]) >= set(EXPECTED_ARTIFACTS)
    for name, item in manifest["artifacts"].items():
        assert item["size_bytes"] >= 0
        artifact_path = Path(item["path"])
        assert artifact_path.is_file()
        if name == "manifest.json":
            assert item["checksum_recorded"] is False
            assert item["sha256"] == "self-referential-not-recorded"
        else:
            assert item["checksum_recorded"] is True
            assert hashlib.sha256(artifact_path.read_bytes()).hexdigest() == item["sha256"]


def test_not_ready_readiness_is_captured_while_all_diagnostics_are_generated(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows(), include_retention=False)
    out = tmp_path / "dry-run"

    proc = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(out))

    assert proc.returncode == 1
    assert_expected_artifacts(out)
    readiness = json.loads((out / "readiness-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert readiness["ready_for_cron"] is False
    assert any(risk["id"] == "missing-retention-audit-policy" for risk in readiness["risks"])
    assert manifest["ready_for_scheduled_watcher"] is False
    assert manifest["stages"]["readiness"]["status"] == "blocked"
    assert manifest["stages"]["connector_json"]["status"] == "ok"
    assert manifest["stages"]["cron_simulation"]["status"] == "ok"


def test_ready_workspace_returns_zero_and_manifest_ready(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows())
    out = tmp_path / "dry-run"

    proc = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(out), "--synthetic-mode")

    assert proc.returncode == 0, proc.stderr + proc.stdout
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["ready_for_scheduled_watcher"] is True
    assert manifest["stages"]["readiness"]["exit_code"] == 0
    assert "Ready for private dry-run gate" in (out / "deployment-checklist.md").read_text(encoding="utf-8")


def test_dry_run_does_not_mutate_source_workspace(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows())
    before = workspace_hashes(ws)

    proc = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(tmp_path / "dry-run"))

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert workspace_hashes(ws) == before


def test_out_inside_workspace_is_rejected(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows())
    out = ws / "tasks" / "dry-run"

    proc = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(out))

    assert proc.returncode == 2
    assert "out path must be outside workspace" in proc.stderr.lower()
    assert not out.exists()


def test_out_hardlink_to_workspace_file_is_rejected(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows())
    out = tmp_path / "dry-run-hardlink"
    out.hardlink_to(ws / "README.md")
    before = (ws / "README.md").read_text(encoding="utf-8")

    proc = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(out))

    assert proc.returncode == 2
    assert "out path must not overwrite workspace file" in proc.stderr.lower()
    assert (ws / "README.md").read_text(encoding="utf-8") == before


def test_existing_non_empty_out_dir_requires_force(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows())
    out = tmp_path / "dry-run"
    out.mkdir()
    (out / "old.txt").write_text("old\n", encoding="utf-8")

    proc = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(out))

    assert proc.returncode == 2
    assert "already exists and is not empty" in proc.stderr.lower()
    assert (out / "old.txt").read_text(encoding="utf-8") == "old\n"

    proc_force = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(out), "--force")
    assert proc_force.returncode == 0, proc_force.stderr + proc_force.stdout
    assert (out / "manifest.json").is_file()


def test_symlinked_workspace_root_is_rejected(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows())
    link = tmp_path / "workspace-link"
    link.symlink_to(ws, target_is_directory=True)

    proc = run_dry_run("--workspace", str(link), "--as-of", "2026-05-14", "--out", str(tmp_path / "dry-run"))

    assert proc.returncode == 2
    assert "workspace path must not be a symlink" in proc.stderr.lower()


def test_cron_simulation_contains_internal_alert_verify_and_no_external_writes(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_actionable_rows())
    out = tmp_path / "dry-run"

    proc = run_dry_run("--workspace", str(ws), "--as-of", "2026-05-14", "--out", str(out))

    assert proc.returncode == 0, proc.stderr + proc.stdout
    text = (out / "cron-simulation.md").read_text(encoding="utf-8")
    assert "Internal Renewal Watcher Alert" in text
    assert "[verify]" in text
    assert "No External Writes" in text
    assert "customer message sent" not in text.lower()
