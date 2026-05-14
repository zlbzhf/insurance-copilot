#!/usr/bin/env python3
"""Validate the Insurance Copilot Hermes-first skill repository."""
from __future__ import annotations

from pathlib import Path
import csv
import json
import re
import subprocess
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
    ROOT / "LICENSE",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "CHANGELOG.md",
    ROOT / "requirements-dev.txt",
    ROOT / "docs" / "continuity.md",
    ROOT / "docs" / "quality-gates.md",
    ROOT / "docs" / "hermes-first-design.md",
    ROOT / "docs" / "quickstart.md",
    ROOT / "docs" / "workflow-surface.md",
    ROOT / "docs" / "local-file-connectors.md",
    ROOT / "docs" / "local-renewal-watcher.md",
    ROOT / "docs" / "script-only-cron-wrapper.md",
    ROOT / "docs" / "private-workspace-readiness.md",
    ROOT / "docs" / "plans" / "2026-05-14-practical-agent-workflow-beta.md",
    ROOT / "docs" / "plans" / "2026-05-14-local-file-connector-slice.md",
    ROOT / "docs" / "plans" / "2026-05-14-local-renewal-watcher.md",
    ROOT / "docs" / "plans" / "2026-05-14-script-only-cron-wrapper.md",
    ROOT / "docs" / "plans" / "2026-05-14-private-workspace-readiness.md",
    ROOT / "docs" / "privacy-and-data-handling.md",
    ROOT / "docs" / "action-safety.md",
    ROOT / "docs" / "jurisdiction-adaptation.md",
    ROOT / "docs" / "release-checklist.md",
    ROOT / "docs" / "architecture.md",
    ROOT / "docs" / "public-knowledge-packs.md",
    ROOT / "docs" / "agent-private-knowledge.md",
    ROOT / "docs" / "llm-wiki-method.md",
    ROOT / "docs" / "contribution-workflow.md",
    ROOT / "docs" / "evidence-driven-standards.md",
    ROOT / "docs" / "github-knowledge-governance.md",
    ROOT / ".github" / "workflows" / "validate.yml",
    ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "source_contribution.yml",
    ROOT / "mcp" / "README.md",
    ROOT / "evals" / "README.md",
    ROOT / "scripts" / "package_skill.py",
    ROOT / "scripts" / "run_evals.py",
    ROOT / "scripts" / "validate_knowledge_pack.py",
    ROOT / "scripts" / "validate_agent_workspace.py",
    ROOT / "scripts" / "create_source_record.py",
    ROOT / "scripts" / "local_file_connectors.py",
    ROOT / "scripts" / "renewal_watcher.py",
    ROOT / "scripts" / "private_workspace_readiness.py",
    ROOT / "cron" / "scripts" / "renewal_watcher.sh",
    ROOT / "tests" / "test_local_file_connectors.py",
    ROOT / "tests" / "test_renewal_watcher.py",
    ROOT / "tests" / "test_renewal_watcher_cron_wrapper.py",
    ROOT / "tests" / "test_private_workspace_readiness.py",
    ROOT / "examples" / "local-connectors" / "synthetic-agent-workspace" / "README.md",
    ROOT / "examples" / "local-connectors" / "expected-daily-workbench.md",
    ROOT / "examples" / "renewal-watcher" / "synthetic-renewal-alert.md",
    ROOT / "examples" / "renewal-watcher" / "synthetic-renewal-alert.json",
    ROOT / "examples" / "cron" / "renewal-watcher-no-agent.md",
    ROOT / "examples" / "private-workspace-readiness" / "synthetic-readiness-report.md",
    ROOT / "examples" / "private-workspace-readiness" / "synthetic-readiness-report.json",
    ROOT / "cron" / "renewal-watcher.md",
    ROOT / "cron" / "compliance-copy-monitor.md",
    ROOT / "cron" / "replacement-risk-monitor.md",
    ROOT / "knowledge" / "README.md",
    ROOT / "knowledge" / "registry.json",
    ROOT / "knowledge" / "institutions" / "README.md",
    ROOT / "knowledge" / "institutions" / "_template" / "PACK.md",
    ROOT / "knowledge" / "institutions" / "aia" / "PACK.md",
    ROOT / "agent-workspace-template" / "README.md",
    ROOT / "agent-workspace-template" / "AGENT.md",
    ROOT / "agent-workspace-template" / "SCHEMA.md",
    ROOT / "agent-workspace-template" / "index.md",
    ROOT / "agent-workspace-template" / "log.md",
    ROOT / "contributions" / "README.md",
    ROOT / "contributions" / "templates" / "source-record.yaml",
    ROOT / "contributions" / "templates" / "contribution.yaml",
]

REQUIRED_REFERENCES = [
    "cold-start-interview.md",
    "client-needs-intake.md",
    "coverage-gap-analysis.md",
    "product-fit-review.md",
    "objection-response.md",
    "compliance-check.md",
    "policy-review.md",
    "replacement-suitability.md",
    "claims-triage.md",
    "annuity-investment-linked-review.md",
    "renewal-review.md",
    "stakeholder-summary.md",
    "compliance-starter.md",
    "default-practice-profile.md",
    "daily-agent-workbench.md",
    "client-plan-draft.md",
    "chinese-talk-tracks.md",
    "referral-ask.md",
]

REQUIRED_TEMPLATES = [
    "practice-profile.md",
    "client-intake.md",
    "coverage-gap-analysis.md",
    "compliance-check.md",
    "product-fit-review.md",
    "policy-review.md",
    "replacement-suitability.md",
    "claims-triage.md",
    "annuity-investment-linked-review.md",
    "renewal-review.md",
    "stakeholder-summary.md",
    "objection-response.md",
    "client-plan-draft.md",
    "daily-agent-workbench.md",
    "chinese-talk-tracks.md",
    "referral-ask.md",
]

REQUIRED_MCP_CONTRACTS = [
    "crm-customer-facts.md",
    "policy-document-kb.md",
    "product-library.md",
    "compliance-script-library.md",
    "renewal-register.md",
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

BAD_OPERATIONAL_TERMS_IN_SKILL = [
    "configured plugin profile path",
    "Claude plugin",
    "slash command plugin",
]

REQUIRED_SAFETY_PHRASES = [
    "draft for licensed",
    "guarantee",
    "conceal, minimize, or omit",
    "replacement",
    "[verify]",
    "Do not persist sensitive customer data",
]

REQUIRED_ARCHITECTURE_PHRASES = [
    "three-layer",
    "Public institution knowledge",
    "Agent private",
    "knowledge/registry.json",
]

REFERENCE_REQUIRED_SECTIONS = ["Output Format", "Guardrails"]
CORE_REFERENCE_MIN_BYTES = 900
PII_PATTERNS = {
    "ssn-like": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit-card-like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


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


def text_files_for_pii() -> list[Path]:
    ignored = {".git", ".venv", ".pytest_cache"}
    suffixes = {".md", ".json", ".csv", ".txt", ".yaml", ".yml"}
    return [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in suffixes and not any(part in ignored for part in p.parts)]


def run_script(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.strip()


def main() -> int:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
    missing += [str((REF_DIR / name).relative_to(ROOT)) for name in REQUIRED_REFERENCES if not (REF_DIR / name).exists()]
    missing += [str((TEMPLATE_DIR / name).relative_to(ROOT)) for name in REQUIRED_TEMPLATES if not (TEMPLATE_DIR / name).exists()]
    missing += [str((ROOT / "mcp" / "contracts" / name).relative_to(ROOT)) for name in REQUIRED_MCP_CONTRACTS if not (ROOT / "mcp" / "contracts" / name).exists()]
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
    for term in BAD_OPERATIONAL_TERMS_IN_SKILL:
        if term in text:
            return fail(f"operational plugin wording in SKILL.md: {term}")

    arch_doc = (ROOT / "docs" / "architecture.md").read_text()
    for phrase in REQUIRED_ARCHITECTURE_PHRASES:
        if phrase not in arch_doc and phrase not in text:
            return fail(f"architecture phrase missing from docs/skill: {phrase}")

    refs = sorted(REF_DIR.glob("*.md"))
    if len(refs) < len(REQUIRED_REFERENCES):
        return fail(f"expected at least {len(REQUIRED_REFERENCES)} workflow references, found {len(refs)}")
    for ref in refs:
        rtext = ref.read_text()
        if len(rtext.strip()) < CORE_REFERENCE_MIN_BYTES:
            return fail(f"reference too thin: {ref.relative_to(ROOT)}")
        if ref.name not in {"compliance-starter.md", "default-practice-profile.md", "cold-start-interview.md"}:
            for section in REFERENCE_REQUIRED_SECTIONS:
                if f"## {section}" not in rtext:
                    return fail(f"{ref.relative_to(ROOT)} missing section: {section}")
        if ref.name == "cold-start-interview.md" and "## Completion Criteria" not in rtext:
            return fail("cold-start-interview.md missing Completion Criteria")
        for term in BAD_OPERATIONAL_TERMS_IN_SKILL:
            if term in rtext:
                return fail(f"operational plugin wording in {ref.relative_to(ROOT)}: {term}")

    for name in REQUIRED_REFERENCES:
        rel = f"references/{name}"
        if rel not in text:
            return fail(f"SKILL.md does not mention required reference: {rel}")

    all_text = "\n".join(p.read_text(errors="ignore") for p in markdown_files())
    found = [term for term in BAD_TERMS if term in all_text]
    if found:
        return fail("Claude-specific install/command terms remain: " + ", ".join(found))

    readme = (ROOT / "README.md").read_text()
    for snippet in [
        "mkdir -p ~/.hermes/skills/insurance/insurance-copilot",
        "python3 scripts/validate_repo.py",
        "python3 scripts/package_skill.py --check",
        "python3 scripts/run_evals.py",
        "python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia",
        "python3 scripts/validate_agent_workspace.py agent-workspace-template --template",
        "full skill directory",
        "knowledge/institutions/",
        "agent-workspace-template/",
        "docs/workflow-surface.md",
        "Daily Agent Workbench",
        "Client Plan Draft",
        "scripts/local_file_connectors.py",
        "docs/local-file-connectors.md",
        "scripts/renewal_watcher.py",
        "docs/local-renewal-watcher.md",
        "docs/script-only-cron-wrapper.md",
        "docs/private-workspace-readiness.md",
        "cron/scripts/renewal_watcher.sh",
        "scripts/private_workspace_readiness.py",
    ]:
        if snippet not in readme:
            return fail(f"README missing required install/validation snippet: {snippet}")

    cron_doc = (ROOT / "docs" / "script-only-cron-wrapper.md").read_text()
    for phrase in ["no_agent=True", "empty stdout", "non-zero exit", "custom:fufu", "mimo-v2.5-pro", "No External Writes"]:
        if phrase not in cron_doc:
            return fail(f"script-only cron wrapper doc missing phrase: {phrase}")

    readiness_doc = (ROOT / "docs" / "private-workspace-readiness.md").read_text()
    for phrase in ["Private Workspace Readiness Report", "Renewal Register Freshness", "Retention / Audit Checklist", "No External Writes", "ready_for_cron"]:
        if phrase not in readiness_doc:
            return fail(f"private workspace readiness doc missing phrase: {phrase}")

    workflow_surface = (ROOT / "docs" / "workflow-surface.md").read_text()
    for name in [
        "Agency Playbook Builder",
        "Daily Agent Workbench",
        "Client Plan Draft",
        "Compliance Copy Checker",
        "Referral Ask Drafter",
        "Renewal/Lapse Follow-up Planner",
        "Institution Knowledge Organizer",
    ]:
        if name not in workflow_surface:
            return fail(f"workflow surface missing workflow: {name}")

    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text()
    for cmd in [
        "python3 scripts/validate_repo.py",
        "python3 scripts/package_skill.py --check",
        "python3 scripts/run_evals.py",
        "python3 scripts/validate_knowledge_pack.py knowledge/institutions/aia",
        "python3 scripts/validate_agent_workspace.py agent-workspace-template --template",
        "python3 -m pytest tests/test_local_file_connectors.py -q",
        "python3 -m pytest tests/test_renewal_watcher.py -q",
        "python3 -m pytest tests/test_renewal_watcher_cron_wrapper.py -q",
        "python3 -m pytest tests/test_private_workspace_readiness.py -q",
        "python3 -m pip install -r requirements-dev.txt",
    ]:
        if cmd not in workflow:
            return fail(f"CI workflow missing command: {cmd}")

    registry = json.loads((ROOT / "knowledge" / "registry.json").read_text())
    if not registry.get("packs") or not any(p.get("id") == "aia" and p.get("data_classification") == "public" for p in registry["packs"]):
        return fail("knowledge registry missing public aia pack")

    eval_cases = sorted((ROOT / "evals" / "cases").glob("*.json"))
    if len(eval_cases) < 17:
        return fail("expected at least 17 eval cases")
    for case in eval_cases:
        try:
            data = json.loads(case.read_text())
        except json.JSONDecodeError as exc:
            return fail(f"invalid eval JSON {case.relative_to(ROOT)}: {exc}")
        for key in ["id", "workflow", "input_summary", "must_include", "must_not_include", "escalation_expected", "expected_output"]:
            if key not in data:
                return fail(f"eval case {case.relative_to(ROOT)} missing key: {key}")
        if not isinstance(data["must_include"], list) or not isinstance(data["must_not_include"], list):
            return fail(f"eval case {case.relative_to(ROOT)} must_include/must_not_include must be lists")
        expected_path = ROOT / data["expected_output"]
        if not expected_path.exists():
            return fail(f"eval case {case.relative_to(ROOT)} expected output missing: {data['expected_output']}")

    register = ROOT / "examples" / "renewal-registers" / "synthetic-renewal-register.csv"
    with register.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or "policy_ref" not in rows[0]:
        return fail("synthetic renewal register missing parseable policy_ref data")

    # Basic PII scan in committed examples/evals/public knowledge/template docs.
    for path in text_files_for_pii():
        if any(part in {"examples", "evals", "knowledge", "agent-workspace-template"} for part in path.parts):
            ptext = path.read_text(errors="ignore")
            for label, pattern in PII_PATTERNS.items():
                if pattern.search(ptext):
                    return fail(f"possible {label} PII in {path.relative_to(ROOT)}")

    for cmd in [
        [sys.executable, "scripts/package_skill.py", "--check"],
        [sys.executable, "scripts/run_evals.py"],
        [sys.executable, "scripts/validate_knowledge_pack.py", "knowledge/institutions/aia"],
        [sys.executable, "scripts/validate_knowledge_pack.py", "knowledge/institutions/_template", "--template"],
        [sys.executable, "scripts/validate_agent_workspace.py", "agent-workspace-template", "--template"],
        [sys.executable, "scripts/local_file_connectors.py", "daily-workbench", "--workspace", "examples/local-connectors/synthetic-agent-workspace", "--format", "json"],
        [sys.executable, "-m", "pytest", "tests/test_local_file_connectors.py", "-q"],
        [sys.executable, "-m", "pytest", "tests/test_renewal_watcher.py", "-q"],
        [sys.executable, "-m", "pytest", "tests/test_renewal_watcher_cron_wrapper.py", "-q"],
        [sys.executable, "-m", "pytest", "tests/test_private_workspace_readiness.py", "-q"],
        [sys.executable, "scripts/renewal_watcher.py", "--csv", "examples/local-connectors/synthetic-agent-workspace/renewal-registers/synthetic-renewal-register.csv", "--as-of", "2026-05-14", "--format", "json"],
        ["bash", "cron/scripts/renewal_watcher.sh", "--workspace", "examples/local-connectors/synthetic-agent-workspace", "--as-of", "2026-05-14", "--mode", "always"],
    ]:
        code, output = run_script(cmd)
        if code != 0:
            return fail(f"command failed {' '.join(cmd)}:\n{output}")

    readiness_cmd = [
        sys.executable,
        "scripts/private_workspace_readiness.py",
        "--workspace",
        "examples/local-connectors/synthetic-agent-workspace",
        "--as-of",
        "2026-05-14",
        "--format",
        "markdown",
    ]
    code, output = run_script(readiness_cmd)
    if code not in {0, 1}:
        return fail(f"command failed {' '.join(readiness_cmd)}:\n{output}")
    for phrase in ["Private Workspace Readiness Report", "Readiness Verdict", "No External Writes"]:
        if phrase not in output:
            return fail(f"private workspace readiness smoke output missing phrase: {phrase}")

    print("insurance-copilot Hermes-first repo ok")
    print(f"references: {len(refs)}")
    print(f"templates: {len(list(TEMPLATE_DIR.glob('*.md')))}")
    print(f"eval_cases: {len(eval_cases)}")
    print("knowledge_packs: aia + template")
    print(f"skill: {SKILL.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
