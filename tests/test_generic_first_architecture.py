#!/usr/bin/env python3
"""Regression tests for generic-first insurance-copilot architecture."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_institution_knowledge_organizer_is_generic_first_in_runtime_surfaces() -> None:
    """Layer-1 workflow docs must define the organizer generically, with AIA only as a seed example."""
    runtime_docs = {
        "SKILL.md": "skills/insurance-copilot/SKILL.md",
        "institution reference": "skills/insurance-copilot/references/institution-knowledge-organizer.md",
        "institution template": "skills/insurance-copilot/templates/institution-knowledge-organizer.md",
        "README": "README.md",
        "README zh": "README.zh-CN.md",
        "workflow surface": "docs/workflow-surface.md",
        "quality gates": "docs/quality-gates.md",
        "product spec": "docs/product-development-spec.md",
        "reference landscape": "docs/reference-landscape.md",
        "documentation map": "docs/documentation-map.md",
        "ROADMAP": "ROADMAP.md",
        "eval README": "evals/README.md",
    }

    required_generic = [
        "Institution Knowledge Organizer",
        "public institution pack",
        "source-backed public pack update",
        "source record",
        "public/private boundary",
        "pack maintainer review",
        "[verify]",
    ]
    forbidden_aia_first = [
        "AIA public pack or other insurer",
        "AIA public pack or other public institution",
        "AIA/友邦, carrier, regulator",
        "especially an **AIA public pack** update",
        "Use for an **AIA public pack**",
        "Use Institution Knowledge Organizer. Help me organize this public insurance source for the AIA public pack",
        "AIA/public pack preference",
    ]

    for label, rel in runtime_docs.items():
        text = read(rel)
        lower = text.lower()
        for phrase in required_generic:
            assert phrase.lower() in lower, f"{label} missing generic phrase: {phrase}"
        for phrase in forbidden_aia_first:
            assert phrase not in text, f"{label} still frames generic workflow as AIA-first: {phrase}"

    combined = "\n".join(read(rel) for rel in runtime_docs.values())
    assert "AIA/友邦 is the current seed example" in combined or "AIA/友邦 是当前 seed 示例" in combined
    assert "Seed packs are examples; the runtime Institution Knowledge Organizer applies to any public institution pack." in combined


def test_generic_templates_do_not_default_to_aia() -> None:
    """Generic templates should use placeholders/unknowns, not an AIA default."""
    generic_templates = [
        "agent-workspace-template/AGENT.md",
        "agent-workspace-template/SCHEMA.md",
        "contributions/templates/source-record.yaml",
        "contributions/templates/contribution.yaml",
        "contributions/templates/proposed-product-page.md",
        "intake/templates/intake.yaml",
        "skills/insurance-copilot/templates/practice-profile.md",
        "skills/insurance-copilot/references/cold-start-interview.md",
    ]

    forbidden = [
        "default_institution_pack: aia",
        "institution: aia",
        "AIA/public pack preference",
    ]
    for rel in generic_templates:
        text = read(rel)
        for phrase in forbidden:
            assert phrase not in text, f"{rel} still uses AIA as a generic default: {phrase}"

    assert "default_institution_pack: unknown" in read("agent-workspace-template/AGENT.md")
    assert "institution: <institution-pack-id>" in read("contributions/templates/source-record.yaml")
    assert "institution: <institution-pack-id>" in read("contributions/templates/contribution.yaml")
    assert "institution: <institution-pack-id>" in read("intake/templates/intake.yaml")
    assert "Institution/public pack preference" in read("skills/insurance-copilot/templates/practice-profile.md")


def test_generic_public_pack_eval_exists_separate_from_aia_seed_eval() -> None:
    generic_case = json.loads((ROOT / "evals/cases/institution-public-pack-source-backed-generic.json").read_text(encoding="utf-8"))
    aia_case = json.loads((ROOT / "evals/cases/aia-public-pack-source-backed.json").read_text(encoding="utf-8"))
    generic_expected = read(generic_case["expected_output"])

    assert generic_case["workflow"] == "institution-knowledge-organizer"
    assert generic_case["id"] == "institution-public-pack-source-backed-generic"
    assert aia_case["id"] == "aia-public-pack-source-backed"
    assert "public institution pack" in generic_case["must_include"]
    assert "AIA public pack" not in generic_case["must_include"]
    assert "AIA public pack" in generic_case["must_not_include"]
    assert "knowledge/institutions/aia/" in generic_case["must_not_include"]
    for phrase in generic_case["must_include"]:
        assert phrase in generic_expected
    for phrase in generic_case["must_not_include"]:
        assert phrase not in generic_expected


def test_all_registered_public_knowledge_packs_validator_runs() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_all_knowledge_packs.py"],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "validated public institution packs" in result.stdout
    assert "aia" in result.stdout
