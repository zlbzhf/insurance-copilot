#!/usr/bin/env python3
"""Tests for private workspace readiness validation."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "private_workspace_readiness.py"

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


def run_readiness(*args: str) -> subprocess.CompletedProcess[str]:
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
    (ws / "README.md").write_text(
        "# Private workspace\n\nDo not publish. No External Writes.\n", encoding="utf-8"
    )
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


def fresh_rows() -> list[dict[str, str]]:
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


def stale_rows() -> list[dict[str, str]]:
    rows = fresh_rows()
    rows[0] = {**rows[0], "status_as_of": "2026-04-01"}
    return rows


def workspace_hashes(workspace: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(p for p in workspace.rglob("*") if p.is_file()):
        hashes[str(path.relative_to(workspace))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def test_markdown_readiness_report_from_synthetic_workspace() -> None:
    proc = run_readiness(
        "--workspace",
        "examples/local-connectors/synthetic-agent-workspace",
        "--as-of",
        "2026-05-14",
        "--format",
        "markdown",
    )

    assert proc.returncode == 1, proc.stderr + proc.stdout
    assert "# Private Workspace Readiness Report" in proc.stdout
    assert "NOT READY for scheduled watcher deployment" in proc.stdout
    assert "Readiness Verdict" in proc.stdout
    assert "Renewal Register Freshness" in proc.stdout
    assert "Retention / Audit Checklist" in proc.stdout
    assert "Scheduled Watcher Deployment Gate" in proc.stdout
    assert "No External Writes" in proc.stdout
    assert "customer message sent" not in proc.stdout.lower()


def test_json_output_contains_readiness_shape(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 0, proc.stderr + proc.stdout
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is True
    assert data["internal_only"] is True
    assert data["no_external_writes"] is True
    assert set(data) >= {"summary", "checks", "risks", "recommended_next_actions"}
    assert data["summary"]["workspace"] == str(ws.resolve())
    assert any(check["id"] == "required-structure" for check in data["checks"])


def test_missing_required_directory_blocks_readiness(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())
    (ws / "claims").rmdir()

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "missing-required-directory" and "claims" in risk["detail"] for risk in data["risks"])


def test_stale_renewal_register_blocks_readiness(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, stale_rows())

    proc = run_readiness(
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--max-stale-days",
        "7",
        "--format",
        "json",
    )

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "stale-renewal-register-row" for risk in data["risks"])
    assert any(action.startswith("Refresh renewal register") for action in data["recommended_next_actions"])


def test_pii_like_content_blocks_synthetic_mode(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())
    (ws / "clients" / "bad.md").write_text("Synthetic leak 123-45-678" + "9\n", encoding="utf-8")

    proc = run_readiness(
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--synthetic-mode",
        "--format",
        "json",
    )

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "possible-pii" and risk["severity"] == "blocker" for risk in data["risks"])


def test_readiness_validation_does_not_mutate_source_workspace(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())
    before = workspace_hashes(ws)

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "markdown")

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert workspace_hashes(ws) == before


def test_output_inside_workspace_is_rejected(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())
    output = ws / "tasks" / "readiness.md"

    proc = run_readiness(
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--format",
        "markdown",
        "--output",
        str(output),
    )

    assert proc.returncode != 0
    assert proc.stdout == ""
    assert "output path must be outside workspace" in proc.stderr.lower()
    assert not output.exists()


def test_output_file_outside_workspace_suppresses_stdout(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())
    output = tmp_path / "readiness.md"

    proc = run_readiness(
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--format",
        "markdown",
        "--output",
        str(output),
    )

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert proc.stdout == ""
    text = output.read_text(encoding="utf-8")
    assert "# Private Workspace Readiness Report" in text
    assert "No External Writes" in text


def test_output_hardlink_to_workspace_file_is_rejected(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())
    output = tmp_path / "hardlinked-readme.md"
    output.hardlink_to(ws / "README.md")
    before = (ws / "README.md").read_text(encoding="utf-8")

    proc = run_readiness(
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--format",
        "markdown",
        "--output",
        str(output),
    )

    assert proc.returncode != 0
    assert "output path must not overwrite workspace file" in proc.stderr.lower()
    assert (ws / "README.md").read_text(encoding="utf-8") == before


def test_missing_retention_file_is_not_ready_but_reported_as_audit_gap(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows(), include_retention=False)

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "missing-retention-audit-policy" for risk in data["risks"])
    assert any("retention" in action.lower() for action in data["recommended_next_actions"])


def test_symlinked_renewal_register_directory_outside_workspace_blocks_readiness(tmp_path: Path) -> None:
    outside = write_workspace(tmp_path / "outside-root", fresh_rows())
    ws = write_workspace(tmp_path, fresh_rows())
    for child in (ws / "renewal-registers").iterdir():
        child.unlink()
    (ws / "renewal-registers").rmdir()
    (ws / "renewal-registers").symlink_to(outside / "renewal-registers", target_is_directory=True)

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "symlinked-workspace-path" for risk in data["risks"])


def test_symlinked_required_file_blocks_readiness(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, fresh_rows())
    outside_readme = tmp_path / "outside-readme.md"
    outside_readme.write_text("# outside\n", encoding="utf-8")
    (ws / "README.md").unlink()
    (ws / "README.md").symlink_to(outside_readme)

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "symlinked-workspace-path" for risk in data["risks"])


def test_mixed_fresh_and_blank_status_as_of_blocks_readiness(tmp_path: Path) -> None:
    rows = fresh_rows() + [{**fresh_rows()[0], "policy_ref": "SYN-POLICY-BLANK", "status_as_of": ""}]
    ws = write_workspace(tmp_path, rows)

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "missing-renewal-status-date" for risk in data["risks"])


def test_mixed_fresh_and_stale_status_as_of_blocks_readiness(tmp_path: Path) -> None:
    rows = fresh_rows() + [{**fresh_rows()[0], "policy_ref": "SYN-POLICY-STALE", "status_as_of": "2026-04-01"}]
    ws = write_workspace(tmp_path, rows)

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--max-stale-days", "7", "--format", "json")

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "stale-renewal-register-row" for risk in data["risks"])


def test_future_status_as_of_blocks_readiness(tmp_path: Path) -> None:
    ws = write_workspace(tmp_path, [{**fresh_rows()[0], "status_as_of": "2026-05-20"}])

    proc = run_readiness("--workspace", str(ws), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 1
    data = json.loads(proc.stdout)
    assert data["ready_for_cron"] is False
    assert any(risk["id"] == "future-renewal-register-date" and risk["severity"] == "blocker" for risk in data["risks"])
