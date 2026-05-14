#!/usr/bin/env python3
"""Tests for script-only cron wrapper around the local renewal watcher."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "cron" / "scripts" / "renewal_watcher.sh"


def run_wrapper(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(WRAPPER), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )


def write_workspace(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    ws = tmp_path / "workspace"
    for folder in ["clients", "meetings", "policies", "claims", "referrals", "tasks"]:
        (ws / folder).mkdir(parents=True, exist_ok=True)
    csv_path = ws / "renewal-registers" / "synthetic-renewal-register.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
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
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    (ws / "README.md").write_text("# SYN workspace\n", encoding="utf-8")
    return ws


def actionable_rows() -> list[dict[str, str]]:
    return [
        {
            "customer_ref": "SYN-CUSTOMER-D7",
            "policy_ref": "SYN-POLICY-D7",
            "carrier": "Example Carrier",
            "product_category": "life",
            "premium_due_date": "2026-05-21",
            "grace_period_end": "2026-06-21",
            "status_source": "",
            "status_as_of": "",
            "last_contact": "",
            "next_action": "verify payment status",
            "review_flags": "",
        },
        {
            "customer_ref": "SYN-CUSTOMER-ENDED",
            "policy_ref": "SYN-POLICY-ENDED",
            "carrier": "Example Carrier",
            "product_category": "life",
            "premium_due_date": "2026-03-01",
            "grace_period_end": "2026-04-01",
            "status_source": "",
            "status_as_of": "",
            "last_contact": "",
            "next_action": "supervisor review",
            "review_flags": "grace ended",
        },
    ]


def monitor_rows() -> list[dict[str, str]]:
    return [
        {
            "customer_ref": "SYN-CUSTOMER-MONITOR",
            "policy_ref": "SYN-POLICY-MONITOR",
            "carrier": "Example Carrier",
            "product_category": "life",
            "premium_due_date": "2026-07-01",
            "grace_period_end": "2026-08-01",
            "status_source": "carrier export",
            "status_as_of": "2026-05-14",
            "last_contact": "",
            "next_action": "monitor later",
            "review_flags": "",
        }
    ]


def workspace_hashes(workspace: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(p for p in workspace.rglob("*") if p.is_file()):
        hashes[str(path.relative_to(workspace))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def test_wrapper_always_mode_prints_internal_alert_from_synthetic_workspace() -> None:
    proc = run_wrapper(
        "--workspace",
        "examples/local-connectors/synthetic-agent-workspace",
        "--as-of",
        "2026-05-14",
        "--mode",
        "always",
    )

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "# Internal Renewal Watcher Alert" in proc.stdout
    assert "[verify]" in proc.stdout
    assert "No External Writes" in proc.stdout
    assert "Draft for licensed/compliance review" in proc.stdout
    assert "message sent" not in proc.stdout.lower()
    assert proc.stderr == ""


def test_wrapper_alert_only_is_silent_when_only_monitor_rows(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, monitor_rows())

    proc = run_wrapper("--workspace", str(ws), "--as-of", "2026-05-14", "--mode", "alert-only")

    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == ""
    assert proc.stderr == ""


def test_wrapper_alert_only_prints_when_actionable_rows_exist(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, actionable_rows())

    proc = run_wrapper("--workspace", str(ws), "--as-of", "2026-05-14", "--mode", "alert-only")

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "Internal Renewal Watcher Alert" in proc.stdout
    assert "SYN-POLICY-D7" in proc.stdout
    assert "SYN-POLICY-ENDED" in proc.stdout


def test_wrapper_missing_workspace_fails_loudly(tmp_path: Path) -> None:
    missing = tmp_path / "missing-workspace"

    proc = run_wrapper("--workspace", str(missing), "--as-of", "2026-05-14", "--mode", "always")

    assert proc.returncode != 0
    assert proc.stdout == ""
    assert "workspace missing" in proc.stderr.lower()


def test_wrapper_rejects_output_inside_workspace(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, actionable_rows())
    output = ws / "tasks" / "renewal-alert.md"

    proc = run_wrapper(
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--mode",
        "always",
        "--output",
        str(output),
    )

    assert proc.returncode != 0
    assert "output path must be outside workspace" in proc.stderr.lower()
    assert not output.exists()


def test_wrapper_output_file_outside_workspace_suppresses_stdout(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, actionable_rows())
    output = tmp_path / "renewal-alert.md"

    proc = run_wrapper(
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--mode",
        "always",
        "--output",
        str(output),
    )

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert proc.stdout == ""
    assert output.exists()
    text = output.read_text(encoding="utf-8")
    assert "Internal Renewal Watcher Alert" in text
    assert "No External Writes" in text


def test_wrapper_does_not_mutate_source_workspace(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, actionable_rows())
    before = workspace_hashes(ws)

    proc = run_wrapper("--workspace", str(ws), "--as-of", "2026-05-14", "--mode", "always")

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert workspace_hashes(ws) == before


def test_wrapper_json_format_outputs_internal_alert_json(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, actionable_rows())

    proc = run_wrapper("--workspace", str(ws), "--as-of", "2026-05-14", "--mode", "always", "--format", "json")

    assert proc.returncode == 0, proc.stderr + proc.stdout
    data = json.loads(proc.stdout)
    assert data["internal_only"] is True
    assert data["no_external_writes"] is True
    assert data["counts"]["total"] == 2
    assert any(alert["bucket"] == "grace-ended" for alert in data["alerts"])


def test_wrapper_rejects_tmpdir_inside_workspace(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, actionable_rows())
    workspace_tmp = ws / "tmp"
    workspace_tmp.mkdir()
    env = os.environ.copy()
    env["TMPDIR"] = str(workspace_tmp)

    proc = run_wrapper("--workspace", str(ws), "--as-of", "2026-05-14", "--mode", "always", env=env)

    assert proc.returncode != 0
    assert proc.stdout == ""
    assert "tmpdir must be outside workspace" in proc.stderr.lower()
    assert not any(workspace_tmp.iterdir())


def test_wrapper_invalid_as_of_fails_loudly(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, actionable_rows())

    proc = run_wrapper("--workspace", str(ws), "--as-of", "not-a-date", "--mode", "always")

    assert proc.returncode != 0
    assert proc.stdout == ""
    assert "renewal watcher failed" in proc.stderr.lower()
    assert "invalid --as-of date" in proc.stderr.lower()
