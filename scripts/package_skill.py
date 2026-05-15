#!/usr/bin/env python3
"""Build and check the Insurance Copilot Hermes skill bundle."""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "insurance-copilot"
REQUIRED_SUBDIRS = ["references", "templates"]


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def copy_skill(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SKILL_DIR, dest)


def check_bundle(bundle_dir: Path) -> list[str]:
    errors: list[str] = []
    if not (bundle_dir / "SKILL.md").exists():
        errors.append("missing SKILL.md")
    for subdir in REQUIRED_SUBDIRS:
        p = bundle_dir / subdir
        if not p.is_dir():
            errors.append(f"missing {subdir}/")
        elif not list(p.glob("*.md")):
            errors.append(f"{subdir}/ has no markdown files")
    text = (bundle_dir / "SKILL.md").read_text(errors="ignore") if (bundle_dir / "SKILL.md").exists() else ""
    for rel in [
        "references/client-needs-intake.md",
        "references/daily-agent-workbench.md",
        "references/compliance-check.md",
        "references/replacement-suitability.md",
        "templates/practice-profile.md",
        "templates/customer-advocacy-memo.md",
        "references/institution-knowledge-organizer.md",
        "templates/institution-knowledge-organizer.md",
    ]:
        if not (bundle_dir / rel).exists():
            errors.append(f"missing referenced bundle file: {rel}")
    if "name: insurance-copilot" not in text:
        errors.append("SKILL.md does not declare name: insurance-copilot")
    if "Practical MVP Operating Mode" not in text:
        errors.append("SKILL.md missing Practical MVP Operating Mode")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, help="destination directory for bundle copy")
    parser.add_argument("--check", action="store_true", help="build in a temp dir and verify contents")
    args = parser.parse_args()

    if not SKILL_DIR.exists():
        return fail(f"missing skill dir: {SKILL_DIR}")

    if args.check or not args.out:
        with tempfile.TemporaryDirectory(prefix="insurance-copilot-bundle-") as tmp:
            dest = Path(tmp) / "insurance-copilot"
            copy_skill(dest)
            errors = check_bundle(dest)
            if errors:
                return fail("; ".join(errors))
            print(f"bundle check ok: {dest}")
            return 0

    copy_skill(args.out)
    errors = check_bundle(args.out)
    if errors:
        return fail("; ".join(errors))
    print(f"bundle written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
