#!/usr/bin/env python3
from pathlib import Path
import re
import sys
try:
    import yaml
except Exception:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "insurance-copilot" / "SKILL.md"
REQUIRED = [
    SKILL,
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "skills" / "insurance-copilot" / "references" / "cold-start-interview.md",
    ROOT / "skills" / "insurance-copilot" / "references" / "client-needs-intake.md",
    ROOT / "skills" / "insurance-copilot" / "references" / "coverage-gap-analysis.md",
    ROOT / "skills" / "insurance-copilot" / "references" / "product-fit-review.md",
    ROOT / "skills" / "insurance-copilot" / "templates" / "practice-profile.md",
]
FORBIDDEN_PATHS = [
    ROOT / "insurance-copilot" / ".claude-plugin",
    ROOT / "insurance-copilot" / "CLAUDE.md",
]

def fail(msg):
    print(f"ERROR: {msg}")
    return 1

def parse_frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    m = re.search(r"\n---\s*\n", text[4:])
    if not m:
        raise ValueError("SKILL.md frontmatter is not closed")
    end = 4 + m.start()
    fm_text = text[4:end]
    body = text[4 + m.end():]
    if yaml:
        fm = yaml.safe_load(fm_text)
    else:
        fm = {}
        for line in fm_text.splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm, body

def main():
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
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
    if not body.strip():
        return fail("skill body is empty")
    refs = sorted((SKILL.parent / "references").glob("*.md"))
    if len(refs) < 9:
        return fail(f"expected at least 9 workflow references, found {len(refs)}")
    all_text = "\n".join(p.read_text(errors="ignore") for p in [ROOT/'README.md', ROOT/'AGENTS.md', SKILL, *refs])
    bad_terms = ["~/." + "claude/plugins/config", "/insurance-copilot" + ":", "." + "claude-plugin"]
    found = [t for t in bad_terms if t in all_text]
    if found:
        return fail("Claude-specific install/command terms remain: " + ", ".join(found))
    print("insurance-copilot Hermes-first repo ok")
    print(f"references: {len(refs)}")
    print(f"skill: {SKILL.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
