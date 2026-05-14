#!/usr/bin/env python3
"""Tests for read-only local-file connector slice."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "local_file_connectors.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "synthetic-agent-workspace"
    write(ws / "clients" / "SYN-CUSTOMER-001.md", """---
type: customer
public_upload_allowed: false
---
# SYN-CUSTOMER-001

## Profile
- Household: synthetic family with two children
- Priority: family protection review

## Missing Facts
- Existing life/disability coverage
- Monthly budget
""")
    write(ws / "meetings" / "SYN-MEETING-001.md", """---
type: meeting-note
---
# SYN-MEETING-001

## Meeting
- Date: 2026-05-14
- Customer/private ref: SYN-CUSTOMER-001
- Purpose: family protection intake

## Follow-up Tasks
- Ask budget and existing coverage questions.
""")
    write(ws / "policies" / "SYN-POLICY-001.md", """---
type: policy-summary
---
# SYN-POLICY-001

## Policy Snapshot
- Customer/private ref: SYN-CUSTOMER-001
- Policy/private ref: SYN-POLICY-001
- Status/source: [verify]

## Premium / Renewal
- Due date: 2026-05-20
- Payment status: [verify]
""")
    write(ws / "claims" / "SYN-CLAIM-001.md", """---
type: claim-tracker
---
# SYN-CLAIM-001

## Claim Context
- Customer/private ref: SYN-CUSTOMER-002
- Carrier status/source: [verify]

## Deadlines / Follow-ups
- Confirm document checklist.
""")
    write(ws / "referrals" / "SYN-REFERRAL-001.md", """---
type: referral-tracker
---
# SYN-REFERRAL-001

## Referral Context
- Consent to contact: [verify]

## Outreach Status
- Next action: draft low-pressure thank-you.
""")
    write(ws / "tasks" / "SYN-TASKS.md", """---
type: task-list
---
# Task List

## Today
- Task: Prepare follow-up draft for SYN-CUSTOMER-001
  - Review needed: licensed/compliance
""")
    (ws / "renewal-registers").mkdir(parents=True, exist_ok=True)
    with (ws / "renewal-registers" / "synthetic-renewal-register.csv").open("w", newline="", encoding="utf-8") as f:
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
        writer.writerow(
            {
                "customer_ref": "SYN-CUSTOMER-001",
                "policy_ref": "SYN-POLICY-001",
                "carrier": "Example Carrier",
                "product_category": "life",
                "premium_due_date": "2026-05-20",
                "grace_period_end": "2026-06-20",
                "status_source": "",
                "status_as_of": "",
                "last_contact": "",
                "next_action": "verify payment status before outreach",
                "review_flags": "possible lapse risk",
            }
        )
    return ws


def run_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd or ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def snapshot_files(ws: Path) -> dict[str, str]:
    return {str(path.relative_to(ws)): path.read_text(encoding="utf-8") for path in sorted(ws.rglob("*")) if path.is_file()}


def test_daily_workbench_markdown_reads_workspace_and_is_read_only(tmp_path: Path) -> None:
    ws = make_workspace(tmp_path)
    before = snapshot_files(ws)

    proc = run_cli("daily-workbench", "--workspace", str(ws), "--format", "markdown")

    assert proc.returncode == 0, proc.stdout
    assert "## Today's Priorities" in proc.stdout
    assert "## High-Risk Items" in proc.stdout
    assert "## Verify Before Action" in proc.stdout
    assert "## No External Writes" in proc.stdout
    assert "Draft for licensed/compliance review" in proc.stdout
    assert "SYN-POLICY-001" in proc.stdout
    assert "[verify]" in proc.stdout
    assert before == snapshot_files(ws)


def test_daily_workbench_json_normalizes_arrays(tmp_path: Path) -> None:
    ws = make_workspace(tmp_path)

    proc = run_cli("daily-workbench", "--workspace", str(ws), "--format", "json")

    assert proc.returncode == 0, proc.stdout
    data = json.loads(proc.stdout)
    assert data["read_only"] is True
    assert data["no_external_writes"] is True
    assert data["workspace"].endswith("synthetic-agent-workspace")
    assert data["counts"]["renewals"] == 1
    assert data["counts"]["customers"] == 1
    assert data["renewals"][0]["policy_ref"] == "SYN-POLICY-001"
    assert data["renewals"][0]["status_source"] == "[verify]"
    assert data["high_risk_items"]


def test_daily_workbench_can_write_explicit_output_without_mutating_sources(tmp_path: Path) -> None:
    ws = make_workspace(tmp_path)
    before = snapshot_files(ws)
    output = tmp_path / "workbench.md"

    proc = run_cli("daily-workbench", "--workspace", str(ws), "--format", "markdown", "--output", str(output))

    assert proc.returncode == 0, proc.stdout
    assert "wrote" in proc.stdout.lower()
    assert output.exists()
    assert "No External Writes" in output.read_text(encoding="utf-8")
    assert before == snapshot_files(ws)


def test_missing_workspace_is_rejected(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    proc = run_cli("daily-workbench", "--workspace", str(missing), "--format", "json")

    assert proc.returncode != 0
    assert "workspace directory missing" in proc.stdout.lower()



def test_symlinked_input_outside_workspace_is_not_read(tmp_path: Path) -> None:
    ws = make_workspace(tmp_path)
    outside = tmp_path / "outside-secret.md"
    outside.write_text("# SYN-SECRET\n\nSHOULD_NOT_LEAK_OUTSIDE_WORKSPACE\n", encoding="utf-8")
    (ws / "clients" / "SYN-LEAK.md").symlink_to(outside)

    proc = run_cli("daily-workbench", "--workspace", str(ws), "--format", "json")

    assert proc.returncode == 0, proc.stdout
    data = json.loads(proc.stdout)
    assert "SHOULD_NOT_LEAK_OUTSIDE_WORKSPACE" not in proc.stdout
    assert all(record["title"] != "SYN-SECRET" for record in data["customers"])


def test_output_inside_workspace_is_rejected_to_preserve_input_records(tmp_path: Path) -> None:
    ws = make_workspace(tmp_path)
    output = ws / "tasks" / "generated-workbench.md"

    proc = run_cli("daily-workbench", "--workspace", str(ws), "--format", "markdown", "--output", str(output))

    assert proc.returncode != 0
    assert "output path must be outside the workspace" in proc.stdout.lower()
    assert not output.exists()
