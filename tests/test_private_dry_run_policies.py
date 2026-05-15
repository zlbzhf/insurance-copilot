#!/usr/bin/env python3
"""Unit regression tests for private dry-run audit readiness policies."""
from __future__ import annotations

from itertools import product
from pathlib import Path

from scripts import private_dry_run


def passing_child_stages() -> dict[str, private_dry_run.StageResult]:
    return {
        "connector_json": private_dry_run.StageResult("ok", 0, ["connector-json"]),
        "connector_markdown": private_dry_run.StageResult("ok", 0, ["connector-md"]),
        "renewal_json": private_dry_run.StageResult("ok", 0, ["renewal-json"]),
        "renewal_markdown": private_dry_run.StageResult("ok", 0, ["renewal-md"]),
        "cron_simulation": private_dry_run.StageResult("ok", 0, ["cron"]),
    }


def test_final_ready_requires_audit_trace_read_only_and_workspace_unchanged() -> None:
    for read_only_verified, workspace_unchanged in product([False, True], repeat=2):
        audit_trace = {
            "read_only_verified": read_only_verified,
            "workspace_unchanged": workspace_unchanged,
        }

        assert private_dry_run.compute_ready_for_scheduled_watcher(
            readiness={"ready_for_cron": True},
            stages=passing_child_stages(),
            audit_trace=audit_trace,
        ) is (read_only_verified is True and workspace_unchanged is True)


def test_final_ready_blocks_when_audit_trace_booleans_are_missing_or_not_strict_true() -> None:
    for audit_trace in [
        {},
        {"read_only_verified": True},
        {"workspace_unchanged": True},
        {"read_only_verified": None, "workspace_unchanged": True},
        {"read_only_verified": True, "workspace_unchanged": None},
        {"read_only_verified": "true", "workspace_unchanged": True},
        {"read_only_verified": True, "workspace_unchanged": "true"},
    ]:
        assert (
            private_dry_run.compute_ready_for_scheduled_watcher(
                readiness={"ready_for_cron": True},
                stages=passing_child_stages(),
                audit_trace=audit_trace,
            )
            is False
        )


def test_final_ready_is_true_only_when_stage_readiness_and_audit_trace_all_pass() -> None:
    audit_trace = {
        "read_only_verified": True,
        "workspace_unchanged": True,
    }

    assert (
        private_dry_run.compute_ready_for_scheduled_watcher(
            readiness={"ready_for_cron": True},
            stages=passing_child_stages(),
            audit_trace=audit_trace,
        )
        is True
    )


def test_manifest_self_artifact_does_not_record_unstable_size(tmp_path: Path) -> None:
    out = tmp_path
    (out / "manifest.json").write_text("{}\n", encoding="utf-8")

    artifacts = private_dry_run.artifact_inventory(out)

    assert artifacts["manifest.json"]["checksum_recorded"] is False
    assert artifacts["manifest.json"]["sha256"] == "self-referential-not-recorded"
    assert artifacts["manifest.json"]["size_recorded"] is False
    assert artifacts["manifest.json"]["size_bytes"] is None
