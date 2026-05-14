#!/usr/bin/env python3
"""Tests for the deterministic ingestion gateway."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / "scripts" / "ingest_gateway.py"


def run_gateway(source_record: Path, raw_text: Path | None = None, output_root: Path | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(GATEWAY), str(source_record)]
    if raw_text:
        cmd.extend(["--raw-text", str(raw_text)])
    if output_root:
        cmd.extend(["--output-root", str(output_root)])
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def test_gateway_stages_product_source(tmp_path: Path) -> None:
    source = tmp_path / "source.yaml"
    raw = tmp_path / "raw.md"
    out = tmp_path / "staging"
    source.write_text(
        """
id: aia-test-product
institution: aia
jurisdiction: [HK]
language: zh-Hans
source_type: official-product-page
source_url: https://example.com/aia-product
retrieved_at: 2026-05-14
public_source: true
redistribution:
  mode: link-only
product_lines: [life]
status: queued
submitted_by: test
""".lstrip(),
        encoding="utf-8",
    )
    raw.write_text(
        "This public product page describes coverage benefits and riders. "
        "Contract terms, exclusions, waiting periods, and current availability must be verified.",
        encoding="utf-8",
    )

    proc = run_gateway(source, raw, out)

    assert proc.returncode == 0, proc.stdout
    stage = out / "aia" / "aia-test-product"
    assert (stage / "classification.yaml").exists()
    assert (stage / "extraction.yaml").exists()
    assert (stage / "provenance.json").exists()
    assert (stage / "validation-report.md").exists()
    report = (stage / "validation-report.md").read_text(encoding="utf-8")
    assert "official-product-page" in report
    assert "product-summary" in report
    provenance = json.loads((stage / "provenance.json").read_text(encoding="utf-8"))
    assert provenance["human_reviewed"] is False
    assert provenance["generated_pages"]


def test_gateway_rejects_private_source(tmp_path: Path) -> None:
    source = tmp_path / "source.yaml"
    source.write_text(
        """
id: private-source
institution: aia
source_type: official-product-page
source_url: https://example.com/private
retrieved_at: 2026-05-14
public_source: false
redistribution:
  mode: link-only
status: queued
""".lstrip(),
        encoding="utf-8",
    )

    proc = run_gateway(source, output_root=tmp_path / "staging")

    assert proc.returncode != 0
    assert "public_source: true" in proc.stdout


def test_gateway_unknown_source_reports_schema_gap(tmp_path: Path) -> None:
    source = tmp_path / "source.yaml"
    out = tmp_path / "staging"
    source.write_text(
        """
id: unusual-format
institution: aia
source_type: mystery-format
source_url: https://example.com/mystery
retrieved_at: 2026-05-14
public_source: true
redistribution:
  mode: link-only
status: queued
""".lstrip(),
        encoding="utf-8",
    )

    proc = run_gateway(source, output_root=out)

    assert proc.returncode == 0, proc.stdout
    gaps = (out / "aia" / "unusual-format" / "schema-gaps.yaml").read_text(encoding="utf-8")
    assert "Source could not be safely mapped" in gaps
