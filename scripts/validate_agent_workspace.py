#!/usr/bin/env python3
"""Validate an agent-private workspace or the public template."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT = ["README.md", "AGENT.md", "SCHEMA.md", "index.md", "log.md"]
REQUIRED_DIRS = [
    "clients",
    "private-institution-notes",
    "renewal-registers",
    "private-scripts",
    "private-evals",
    "raw",
    "queries",
]
TEMPLATE_FORBIDDEN_REAL_DATA = [
    "john smith",
    "jane doe",
    "policy number:",
    "claim number:",
]
PII_PATTERNS = {
    "ssn-like": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit-card-like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(errors="ignore")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter not closed")
    fm_text = text[4:end]
    body = text[text.find("\n", end + 4) + 1 :]
    if yaml:
        fm = yaml.safe_load(fm_text) or {}
    else:
        fm = {}
        for line in fm_text.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                fm[key.strip()] = value.strip().strip('"\'')
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a mapping")
    return fm, body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--template", action="store_true", help="Validate public template; reject real-looking data")
    args = parser.parse_args()
    ws = args.workspace.resolve()
    if not ws.exists() or not ws.is_dir():
        return fail(f"workspace directory missing: {ws}")
    for name in REQUIRED_ROOT:
        if not (ws / name).exists():
            return fail(f"missing {name}")
    for name in REQUIRED_DIRS:
        if not (ws / name).is_dir():
            return fail(f"missing directory {name}/")

    try:
        fm, body = parse_frontmatter(ws / "AGENT.md")
    except Exception as exc:
        return fail(f"AGENT.md invalid: {exc}")
    if fm.get("data_classification") != "private-agent-knowledge":
        return fail("AGENT.md data_classification must be private-agent-knowledge")
    if fm.get("public_upload_allowed") is not False:
        return fail("AGENT.md must set public_upload_allowed: false")
    if "Do not copy" not in body and "Do not publish" not in body:
        return fail("AGENT.md must warn against public upload")

    schema = (ws / "SCHEMA.md").read_text(errors="ignore")
    for phrase in ["Agent Private Wiki Schema", "private-institution-note", "Customer Pages", "Private Institution Notes"]:
        if phrase not in schema:
            return fail(f"SCHEMA.md missing required phrase: {phrase}")
    if "Do not publish" not in (ws / "README.md").read_text(errors="ignore"):
        return fail("README.md must warn not to publish private workspace")
    if "## [" not in (ws / "log.md").read_text(errors="ignore"):
        return fail("log.md missing dated entries")

    if args.template:
        all_text = "\n".join(p.read_text(errors="ignore") for p in ws.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".txt", ".csv"})
        lower = all_text.lower()
        for term in TEMPLATE_FORBIDDEN_REAL_DATA:
            if term in lower:
                return fail(f"template contains real-data-looking term: {term}")
        for label, pattern in PII_PATTERNS.items():
            if pattern.search(all_text):
                return fail(f"template contains possible {label} PII")

    print(f"agent workspace ok: {ws.relative_to(ROOT) if ws.is_relative_to(ROOT) else ws}")
    print("template:" if args.template else "workspace:", "yes" if args.template else "private")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
