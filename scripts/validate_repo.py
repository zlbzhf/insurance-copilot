#!/usr/bin/env python3
"""Validate the Insurance Copilot Hermes-first skill repository."""
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

try:
    import yaml
except Exception:  # pragma: no cover - validator works without PyYAML for top-level keys
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "insurance-copilot"
SKILL = SKILL_DIR / "SKILL.md"
REF_DIR = SKILL_DIR / "references"
TEMPLATE_DIR = SKILL_DIR / "templates"

REQUIRED = [
    SKILL,
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "ROADMAP.md",
    ROOT / "docs" / "continuity.md",
    ROOT / "docs" / "quality-gates.md",
    ROOT / "docs" / "hermes-first-design.md",
    ROOT / ".github" / "workflows" / "validate.yml",
    ROOT / "mcp" / "README.md",
    ROOT / "evals" / "README.md",
    ROOT / "cron" / "renewal-watcher.md",
    ROOT / "cron" / "compliance-copy-monitor.md",
    ROOT / "cron" / "replacement-risk-monitor.md",
]

REQUIRED_REFERENCES = [
    "cold-start-interview.md",
    "client-needs-intake.md",
    "coverage-gap-analysis.md",
    "product-fit-review.md",
    "objection-response.md",
    "compliance-check.md",
    "policy-review.md",
    "renewal-review.md",
    "stakeholder-summary.md",
    "compliance-starter.md",
    "default-practice-profile.md",
]

REQUIRED_TEMPLATES = [
    "practice-profile.md",
    "client-intake.md",
    "compliance-check.md",
    "product-fit-review.md",
    "policy-review.md",
    "renewal-review.md",
    "stakeholder-summary.md",
]

FORBIDDEN_PATHS = [
    ROOT / "insurance-copilot" / ("." + "claude-plugin"),
    ROOT / "insurance-copilot" / "CLAUDE.md",
    ROOT / "insurance-copilot" / ("." + "mcp.json"),
]

BAD_TERMS = [
    "~/." + "claude/plugins/config",
    "/insurance-copilot" + ":",
    "." + "claude-plugin",
]

REQUIRED_SAFETY_PHRASES = [
    "draft for licensed",
    "guarantee",
    "conceal, minimize, or omit",
    "replacement",
    "[verify]",
]

REFERENCE_REQUIRED_SECTIONS = [
    "Output Format",
]


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    match = re.search(r"\n---\s*\n", text[4:])
    if not match:
        raise ValueError("SKILL.md frontmatter is not closed")
    end = 4 + match.start()
    fm_text = text[4:end]
    body = text[4 + match.end() :]
    if yaml:
        fm = yaml.safe_load(fm_text)
    else:
        fm = {}
        for line in fm_text.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                fm[key.strip()] = value.strip()
    if not isinstance(fm, dict):
        raise ValueError("SKILL.md frontmatter must parse as a mapping")
    return fm, body


def markdown_files() -> list[Path]:
    ignored = {".git", ".venv", ".pytest_cache"}
    return [p for p in ROOT.rglob("*.md") if not any(part in ignored for part in p.parts)]


def main() -> int:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
    missing += [str((REF_DIR / name).relative_to(ROOT)) for name in REQUIRED_REFERENCES if not (REF_DIR / name).exists()]
    missing += [str((TEMPLATE_DIR / name).relative_to(ROOT)) for name in REQUIRED_TEMPLATES if not (TEMPLATE_DIR / name).exists()]
    if missing:
        return fail("missing required files: " + ", ".join(missing))

    forbidden = [str(p.relative_to(ROOT)) for p in FORBIDDEN_PATHS if p.exists()]
    if forbidden:
        return fail("Claude-first artifacts still present: " + ", ".join(forbidden))

    text = SKILL.read_text()
    fm, body = parse_frontmatter(text)
    if fm.get("name") != "insurance-copilot":
        return fail("skill frontmatter name must be insurance-copilot")
    desc = fm.get("description", "")
    if not desc or len(desc) > 1024:
        return fail("skill description missing or >1024 chars")
    if len(text) > 100_000:
        return fail("SKILL.md exceeds Hermes skill size limit")
    if not body.strip():
        return fail("skill body is empty")

    for phrase in REQUIRED_SAFETY_PHRASES:
        if phrase not in text:
            return fail(f"SKILL.md missing required safety phrase: {phrase}")

    refs = sorted(REF_DIR.glob("*.md"))
    if len(refs) < len(REQUIRED_REFERENCES):
        return fail(f"expected at least {len(REQUIRED_REFERENCES)} workflow references, found {len(refs)}")

    for ref in refs:
        rtext = ref.read_text()
        if len(rtext.strip()) < 500:
            return fail(f"reference too thin: {ref.relative_to(ROOT)}")
        if ref.name not in {"compliance-starter.md", "default-practice-profile.md", "cold-start-interview.md"}:
            for section in REFERENCE_REQUIRED_SECTIONS:
                if f"## {section}" not in rtext:
                    return fail(f"{ref.relative_to(ROOT)} missing section: {section}")
        if ref.name not in {"compliance-starter.md", "default-practice-profile.md", "cold-start-interview.md"}:
            if "## Guardrails" not in rtext:
                return fail(f"{ref.relative_to(ROOT)} missing section: Guardrails")
        if ref.name == "cold-start-interview.md" and "## Completion Criteria" not in rtext:
            return fail("cold-start-interview.md missing Completion Criteria")

    all_text = "\n".join(p.read_text(errors="ignore") for p in markdown_files())
    found = [term for term in BAD_TERMS if term in all_text]
    if found:
        return fail("Claude-specific install/command terms remain: " + ", ".join(found))

    eval_cases = sorted((ROOT / "evals" / "cases").glob("*.json"))
    if len(eval_cases) < 3:
        return fail("expected at least 3 eval cases")
    for case in eval_cases:
        try:
            data = json.loads(case.read_text())
        except json.JSONDecodeError as exc:
            return fail(f"invalid eval JSON {case.relative_to(ROOT)}: {exc}")
        for key in ["id", "workflow", "input_summary", "must_include", "must_not_include", "escalation_expected"]:
            if key not in data:
                return fail(f"eval case {case.relative_to(ROOT)} missing key: {key}")
        if not isinstance(data["must_include"], list) or not isinstance(data["must_not_include"], list):
            return fail(f"eval case {case.relative_to(ROOT)} must_include/must_not_include must be lists")

    readme = (ROOT / "README.md").read_text()
    if "mkdir -p ~/.hermes/skills/insurance/insurance-copilot" not in readme:
        return fail("README missing local Hermes install command")
    if "python3 scripts/validate_repo.py" not in readme:
        return fail("README missing validation command")

    print("insurance-copilot Hermes-first repo ok")
    print(f"references: {len(refs)}")
    print(f"templates: {len(list(TEMPLATE_DIR.glob('*.md')))}")
    print(f"eval_cases: {len(eval_cases)}")
    print(f"skill: {SKILL.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
