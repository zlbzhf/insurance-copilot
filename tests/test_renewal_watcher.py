#!/usr/bin/env python3
"""Tests for internal-only local renewal watcher."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCHER = ROOT / "scripts" / "renewal_watcher.py"
CONNECTOR = ROOT / "scripts" / "local_file_connectors.py"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def write_csv(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
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
            ],
        )
        writer.writeheader()
        writer.writerows(
            [
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
                    "customer_ref": "SYN-CUSTOMER-DPLUS1",
                    "policy_ref": "SYN-POLICY-DPLUS1",
                    "carrier": "Example Carrier",
                    "product_category": "health",
                    "premium_due_date": "2026-05-13",
                    "grace_period_end": "2026-06-13",
                    "status_source": "",
                    "status_as_of": "",
                    "last_contact": "",
                    "next_action": "check grace period",
                    "review_flags": "grace follow-up",
                },
                {
                    "customer_ref": "SYN-CUSTOMER-GRACE-END",
                    "policy_ref": "SYN-POLICY-GRACE-END",
                    "carrier": "Example Carrier",
                    "product_category": "life",
                    "premium_due_date": "2026-04-01",
                    "grace_period_end": "2026-05-15",
                    "status_source": "",
                    "status_as_of": "",
                    "last_contact": "",
                    "next_action": "escalate before grace ends",
                    "review_flags": "possible lapse risk",
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
        )
    return path


def make_bundle(tmp_path: Path) -> Path:
    csv_path = write_csv(tmp_path / "workspace" / "renewal-registers" / "synthetic-renewal-register.csv")
    bundle = tmp_path / "bundle.json"
    proc = run_cmd(str(CONNECTOR), "daily-workbench", "--workspace", str(csv_path.parents[1]), "--format", "json", "--output", str(bundle))
    assert proc.returncode == 0, proc.stdout
    return bundle


def test_watcher_reads_connector_bundle_and_outputs_internal_markdown(tmp_path: Path) -> None:
    bundle = make_bundle(tmp_path)

    proc = run_cmd(str(WATCHER), "--bundle", str(bundle), "--as-of", "2026-05-14", "--format", "markdown")

    assert proc.returncode == 0, proc.stdout
    assert "# Internal Renewal Watcher Alert" in proc.stdout
    assert "D-7" in proc.stdout
    assert "D+1" in proc.stdout
    assert "grace-period-before-end" in proc.stdout
    assert "grace-ended" in proc.stdout
    assert "[verify]" in proc.stdout
    assert "No External Writes" in proc.stdout
    assert "Draft for licensed/compliance review" in proc.stdout
    assert "send message" not in proc.stdout.lower()


def test_watcher_reads_csv_and_outputs_json_counts(tmp_path: Path) -> None:
    csv_path = write_csv(tmp_path / "workspace" / "renewal-registers" / "synthetic-renewal-register.csv")

    proc = run_cmd(str(WATCHER), "--csv", str(csv_path), "--as-of", "2026-05-14", "--format", "json")

    assert proc.returncode == 0, proc.stdout
    data = json.loads(proc.stdout)
    assert data["internal_only"] is True
    assert data["no_external_writes"] is True
    assert data["as_of"] == "2026-05-14"
    assert data["counts"]["total"] == 4
    assert data["counts"]["d_7"] == 1
    assert data["counts"]["d_plus_1"] == 1
    assert data["counts"]["grace_period_before_end"] == 1
    assert data["counts"]["grace_ended"] == 1
    assert data["alerts"][0]["policy_ref"].startswith("SYN-POLICY")


def test_watcher_rejects_missing_input(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"

    proc = run_cmd(str(WATCHER), "--bundle", str(missing), "--as-of", "2026-05-14")

    assert proc.returncode != 0
    assert "input file missing" in proc.stdout.lower()


def test_watcher_rejects_symlink_outside_workspace_when_workspace_supplied(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    outside = tmp_path / "outside.csv"
    write_csv(outside)
    link = ws / "renewal-registers" / "linked.csv"
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(outside)

    proc = run_cmd(str(WATCHER), "--csv", str(link), "--workspace", str(ws), "--as-of", "2026-05-14")

    assert proc.returncode != 0
    assert "input path must be a regular file" in proc.stdout.lower()


def test_bundle_outside_workspace_is_allowed_for_tmp_connector_output(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    csv_path = write_csv(ws / "renewal-registers" / "synthetic-renewal-register.csv")
    bundle = tmp_path / "bundle.json"
    connector = run_cmd(
        str(CONNECTOR),
        "daily-workbench",
        "--workspace",
        str(csv_path.parents[1]),
        "--format",
        "json",
        "--output",
        str(bundle),
    )
    assert connector.returncode == 0, connector.stdout

    proc = run_cmd(str(WATCHER), "--bundle", str(bundle), "--workspace", str(ws), "--as-of", "2026-05-14")

    assert proc.returncode == 0, proc.stdout
    assert "Internal Renewal Watcher Alert" in proc.stdout


def test_symlinked_bundle_is_rejected_even_without_workspace(tmp_path: Path) -> None:
    bundle = make_bundle(tmp_path)
    link = tmp_path / "bundle-link.json"
    link.symlink_to(bundle)

    proc = run_cmd(str(WATCHER), "--bundle", str(link), "--as-of", "2026-05-14")

    assert proc.returncode != 0
    assert "input path must be a regular file" in proc.stdout.lower()


def test_watcher_rejects_output_inside_workspace(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    csv_path = write_csv(ws / "renewal-registers" / "synthetic-renewal-register.csv")
    output = ws / "tasks" / "renewal-alert.md"

    proc = run_cmd(
        str(WATCHER),
        "--csv",
        str(csv_path),
        "--workspace",
        str(ws),
        "--as-of",
        "2026-05-14",
        "--output",
        str(output),
    )

    assert proc.returncode != 0
    assert "output path must be outside the workspace" in proc.stdout.lower()
    assert not output.exists()


def test_watcher_rejects_output_inside_inferred_csv_workspace(tmp_path: Path) -> None:
    ws = tmp_path / "workspace"
    csv_path = write_csv(ws / "renewal-registers" / "synthetic-renewal-register.csv")
    output = ws / "tasks" / "renewal-alert.md"

    proc = run_cmd(
        str(WATCHER),
        "--csv",
        str(csv_path),
        "--as-of",
        "2026-05-14",
        "--output",
        str(output),
    )

    assert proc.returncode != 0
    assert "output path must be outside the workspace" in proc.stdout.lower()
    assert not output.exists()


def test_watcher_rejects_output_overwriting_input(tmp_path: Path) -> None:
    csv_path = write_csv(tmp_path / "workspace" / "renewal-registers" / "synthetic-renewal-register.csv")
    before = csv_path.read_text(encoding="utf-8")

    proc = run_cmd(
        str(WATCHER),
        "--csv",
        str(csv_path),
        "--as-of",
        "2026-05-14",
        "--output",
        str(csv_path),
    )

    assert proc.returncode != 0
    assert "output path must not overwrite input" in proc.stdout.lower()
    assert csv_path.read_text(encoding="utf-8") == before


def test_watcher_rejects_output_hardlink_to_input(tmp_path: Path) -> None:
    csv_path = write_csv(tmp_path / "workspace" / "renewal-registers" / "synthetic-renewal-register.csv")
    hardlink = tmp_path / "hardlink.csv"
    hardlink.hardlink_to(csv_path)
    before = csv_path.read_text(encoding="utf-8")

    proc = run_cmd(
        str(WATCHER),
        "--csv",
        str(csv_path),
        "--as-of",
        "2026-05-14",
        "--output",
        str(hardlink),
    )

    assert proc.returncode != 0
    assert "output path must not overwrite input" in proc.stdout.lower()
    assert csv_path.read_text(encoding="utf-8") == before
