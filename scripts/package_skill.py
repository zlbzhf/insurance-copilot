#!/usr/bin/env python3
"""Build and check the Insurance Copilot Hermes skill bundle."""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRS = [
    ROOT / "skills" / "insurance_copilot",
    ROOT / "skills" / "coach_me",
]
REQUIRED_SUBDIRS = ["references", "templates"]

# Per-skill bundle checks
SKILL_CHECKS: dict[str, dict] = {
    "insurance_copilot": {
        "name": "insurance_copilot",
        "refs": [
            "references/client-needs-intake.md",
            "references/daily-agent-workbench.md",
            "references/compliance-check.md",
            "references/replacement-suitability.md",
            "templates/practice-profile.md",
            "templates/customer-advocacy-memo.md",
            "references/professional-review-gate.md",
            "templates/professional-review-gate.md",
            "references/chinese-talk-tracks.md",
            "templates/chinese-talk-tracks.md",
            "references/institution-knowledge-organizer.md",
            "templates/institution-knowledge-organizer.md",
            "references/source-grounding-guardrails.md",
            "templates/source-grounding-guardrails.md",
            "references/private-workspace-trace-readiness.md",
            "templates/private-workspace-audit-trace.md",
            "references/external-write-action-boundary.md",
            "templates/external-write-action-boundary.md",
        ],
        "text_checks": {
            "name_check": "name: insurance_copilot",
            "body_checks": [
                "Practical MVP Operating Mode",
                "默认使用中文",
                "[待核实]",
                "不得默认机构",
                "主动询问角色",
            ],
        },
    },
    "coach_me": {
        "name": "coach_me",
        "refs": [
            "templates/working-document.md",
        ],
        "text_checks": {
            "name_check": "name: coach_me",
            "body_checks": [
                "Not a fixed count",
                "Not a fixed format",
                "Dynamic, not frozen",
                "Coach_me Working Document",
            ],
        },
    },
}


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def copy_skill(src: Path, dest: Path) -> None:
    bundle = dest / src.name
    if bundle.exists():
        shutil.rmtree(bundle)
    shutil.copytree(src, bundle)


def check_bundle(bundle_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_name = bundle_dir.name
    checks = SKILL_CHECKS.get(skill_name)

    if not checks:
        errors.append(f"no checks defined for skill: {skill_name}")
        return errors

    text = (bundle_dir / "SKILL.md").read_text(errors="ignore") if (bundle_dir / "SKILL.md").exists() else ""

    if not text:
        errors.append(f"missing SKILL.md in {skill_name}")
        return errors

    text_checks = checks.get("text_checks", {})
    if text_checks.get("name_check") and text_checks["name_check"] not in text:
        errors.append(f"SKILL.md does not declare {text_checks['name_check']}")

    for phrase in text_checks.get("body_checks", []):
        if phrase not in text:
            errors.append(f"SKILL.md missing phrase: {phrase}")

    for rel in checks.get("refs", []):
        if not (bundle_dir / rel).exists():
            errors.append(f"missing referenced bundle file: {rel}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, help="destination directory for bundle copy")
    parser.add_argument("--check", action="store_true", help="build in a temp dir and verify contents")
    args = parser.parse_args()

    missing = [str(d) for d in SKILL_DIRS if not d.exists()]
    if missing:
        return fail(f"missing skill dir(s): {missing}")

    if args.check or not args.out:
        with tempfile.TemporaryDirectory(prefix="insurance_copilot-bundle-") as tmp:
            bundle_root = Path(tmp)
            for sd in SKILL_DIRS:
                copy_skill(sd, bundle_root)

            all_errors = []
            for sd in SKILL_DIRS:
                errors = check_bundle(bundle_root / sd.name)
                if errors:
                    for e in errors:
                        print(f"[{sd.name}] {e}")
                    all_errors.extend(errors)

            if all_errors:
                return fail(f"{len(all_errors)} bundle error(s)")

            if args.out:
                for sd in SKILL_DIRS:
                    copy_skill(sd, args.out)

            print(f"bundle check ok: {bundle_root}")
        return 0

    if args.out:
        for sd in SKILL_DIRS:
            copy_skill(sd, args.out)
        print(f"bundle copied to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
