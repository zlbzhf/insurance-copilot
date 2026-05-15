#!/usr/bin/env python3
"""Regression tests for the practical practitioner-facing MVP surface."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_readme_leads_with_manual_practitioner_mvp_not_cron_or_ci() -> None:
    text = read("README.md")
    assert "[简体中文](README.zh-CN.md)" in text
    assert "standalone Hermes skill repository" in text
    assert "## Product Philosophy" in text
    assert "customer-first advocacy within compliance boundaries" in text
    assert "## Practical MVP: How an Agent Uses It" in text
    assert "## Recommended First Session" in text
    assert "workflow router, not a menu bot" in text
    assert "manual-first" in text
    assert "## Runtime-Effective Constraint Model" in text
    assert "not the runtime source by itself" in text

    mvp_pos = text.index("## Practical MVP: How an Agent Uses It")
    cron_pos = text.index("## Advanced / Later: Local Connectors and Watchers")
    validate_pos = text.index("## Developer Validation")
    assert mvp_pos < cron_pos < validate_pos

    early = text[:cron_pos]
    assert "cronjob(" not in early
    assert "Private Dry-Run Deployment Harness" not in early
    assert "Scheduled Watcher" not in early


def test_chinese_readme_and_changelogs_are_first_class_project_surfaces() -> None:
    zh_readme = read("README.zh-CN.md")
    changelog = read("CHANGELOG.md")
    zh_changelog = read("CHANGELOG.zh-CN.md")

    for phrase in [
        "保险代理人工作流助手",
        "独立的 Hermes 技能型产品仓库",
        "产品理念",
        "在合规边界内，以客户利益为先",
        "客户优先",
        "合规边界",
        "运行时约束链",
        "本身不是运行时来源",
        "公共保险机构知识包",
        "代理人私有工作区",
        "开发验证",
    ]:
        assert phrase in zh_readme

    for phrase in [
        "## [Unreleased]",
        "## [0.1.0] - 2026-05-15",
        "### Added",
        "### Changed",
        "### Fixed",
        "### Security and Compliance",
        "customer-first advocacy within compliance boundaries",
        "runtime-effective",
    ]:
        assert phrase in changelog

    for phrase in [
        "## [未发布]",
        "## [0.1.0] - 2026-05-15",
        "### 新增",
        "### 变更",
        "### 修复",
        "### 安全与合规",
        "customer-first advocacy within compliance boundaries",
        "runtime-effective constraints",
    ]:
        assert phrase in zh_changelog


def test_quickstart_is_short_practitioner_loop_before_advanced_appendix() -> None:
    text = read("docs/quickstart.md")
    assert "# Quickstart: Practical Insurance Agent Loop" in text
    assert "Use this guide when you want a usable first version" in text
    assert "## The 30-Minute Useful Loop" in text
    assert "## Advanced Appendix" in text

    loop_pos = text.index("## The 30-Minute Useful Loop")
    appendix_pos = text.index("## Advanced Appendix")
    assert loop_pos < appendix_pos

    loop = text[loop_pos:appendix_pos]
    assert "Practice Profile" in loop
    assert "Daily Agent Workbench" in loop
    assert "Client Needs Intake" in loop
    assert "Coverage Gap Drafter" in loop
    assert "Compliance Copy Checker" in loop
    assert "cron" not in loop.lower()
    assert "private_dry_run" not in loop


def test_skill_contains_task_first_routing_rules() -> None:
    text = read("skills/insurance-copilot/SKILL.md")
    assert "## Practical MVP Operating Mode" in text
    assert "Do not start by dumping the full workflow catalog" in text
    assert "If the user already states a task, route directly" in text
    assert "Ask at most three essential questions" in text
    assert "Manual-first" in text
    assert "customer-facing drafts remain drafts" in text


def test_practical_playbook_example_exists_and_avoids_deployment_language() -> None:
    text = read("examples/practical-mvp/agent-first-session.md")
    assert "# Practical MVP Example: First Agent Session" in text
    assert "Input 1 — Set the Practice Profile" in text
    assert "Input 2 — Daily Workbench" in text
    assert "Input 3 — Client Intake" in text
    assert "Input 4 — Safer WeChat Draft" in text
    assert "Do not send automatically" in text
    forbidden = ["cronjob(", "private_dry_run.py", "scheduled watcher", "deployment harness"]
    lower = text.lower()
    for term in forbidden:
        assert term.lower() not in lower


def test_eval_case_covers_practical_mvp_entry() -> None:
    case_path = ROOT / "evals/cases/practical-mvp-first-session.json"
    data = json.loads(case_path.read_text(encoding="utf-8"))
    assert data["workflow"] == "practical-mvp-first-session"
    assert "workflow router" in data["must_include"]
    assert "cronjob(" in data["must_not_include"]
    expected = read(data["expected_output"])
    for phrase in data["must_include"]:
        assert phrase in expected
    for phrase in data["must_not_include"]:
        assert phrase not in expected


def test_practical_mvp_eval_forbidden_terms_are_not_safe_negative_language() -> None:
    data = json.loads((ROOT / "evals/cases/practical-mvp-first-session.json").read_text(encoding="utf-8"))
    forbidden = set(data["must_not_include"])
    phrases_that_may_be_quoted_or_negated_in_safe_outputs = {
        "guaranteed approval",
        "best risk-free plan",
        "risk-free",
        "every family",
        "automatically send customer messages",
        "approved to send",
        "no compliance review needed",
        "live scheduled job",
        "safe to send without review",
    }
    assert forbidden.isdisjoint(phrases_that_may_be_quoted_or_negated_in_safe_outputs)
    assert all(term == term.upper() or term == "cronjob(" for term in forbidden)


def test_onboarding_is_guided_not_manual_profile_form() -> None:
    skill = read("skills/insurance-copilot/SKILL.md")
    cold_start = read("skills/insurance-copilot/references/cold-start-interview.md")
    quickstart = read("docs/quickstart.md")
    workflow_surface = read("docs/workflow-surface.md")

    for text in [skill, cold_start, quickstart, workflow_surface]:
        assert "Never ask the agent to manually fill the profile template" in text
        assert "template is an internal storage format" in text
        assert "New Agent Default Mode" in text
        assert "I don't know yet" in text

    assert "ask no more than three onboarding questions before producing a provisional profile" in cold_start
    assert "Use conservative defaults when the agent is unsure" in cold_start


def test_scenarios_and_evals_are_ai_assisted_not_agent_homework() -> None:
    skill = read("skills/insurance-copilot/SKILL.md")
    workflow_surface = read("docs/workflow-surface.md")
    example = read("examples/practical-mvp/agent-friendly-onboarding.md")
    eval_readme = read("evals/README.md")

    for text in [skill, workflow_surface, eval_readme, example]:
        assert "Agents provide messy real-world context" in text
        assert "AI converts it into structured scenarios" in text
        assert "evals are internal quality fixtures" in text
        assert "agents do not write JSON eval cases" in text

    assert "customer says: I already have insurance" in example
    assert "AI-generated scenario card" in example
    assert "AI-generated eval intent" in example


def test_skill_customer_first_advocacy_not_empty_neutrality() -> None:
    text = read("skills/insurance-copilot/SKILL.md")
    workflow_surface = read("docs/workflow-surface.md")

    for phrase in [
        "customer-first advocacy within compliance boundaries",
        "do not use neutral caveats as a substitute for service",
        "maximum lawful support",
        "advocacy memo",
        "client-interest action plan",
    ]:
        assert phrase in text.lower()
        assert phrase in workflow_surface.lower()


def test_underwriting_disclosure_supports_approval_without_misrepresentation() -> None:
    intake = read("skills/insurance-copilot/references/client-needs-intake.md")
    compliance = read("skills/insurance-copilot/references/compliance-starter.md")
    expected = read("evals/expected/underwriting-disclosure-advocacy.md")

    for text in [intake, compliance, expected]:
        lowered = text.lower()
        assert "help the customer present accurate, complete, and favorable-underwriting-relevant facts" in lowered
        assert "do not conceal, minimize, omit, or reframe material facts" in lowered
        assert "disclosure support memo" in lowered
        assert "customer-first" in lowered

    assert "make it sound minor" not in expected
    assert "leave it out" not in expected


def test_claims_triage_preserves_customer_claim_arguments() -> None:
    claims = read("skills/insurance-copilot/references/claims-triage.md")
    expected = read("evals/expected/property-claim-late-notice-advocacy.md")

    for text in [claims, expected]:
        lowered = text.lower()
        assert "develop the strongest good-faith claim-support position" in lowered
        assert "do not stop at `the carrier decides`" in lowered
        assert "knew or should have known" in lowered
        assert "claim advocacy memo" in lowered
        assert "customer-first" in lowered

    assert "dead-end disposition" in expected
    assert "giving up without reviewing" in expected


def test_service_philosophy_is_systemic_not_case_patch() -> None:
    philosophy = read("docs/customer-first-service-philosophy.md")
    operating_model = read("docs/customer-advocacy-operating-model.md")
    scenario_matrix = read("docs/customer-service-scenario-matrix.md")
    roadmap = read("ROADMAP.md")

    for text in [philosophy, operating_model, scenario_matrix, roadmap]:
        lowered = text.lower()
        assert "customer-first advocacy within compliance boundaries" in lowered
        assert "compliance is a guardrail for service" in lowered
        assert "empty neutrality is insufficient" in lowered
        assert "from idea to product principle to operating model to workflow to scenario matrix to eval" in lowered

    for phrase in [
        "underwriting / disclosure",
        "claims / review",
        "policy review found unclaimed benefit",
        "replacement / surrender",
        "complaint or mis-selling concern",
        "renewal / lapse / reinstatement",
        "new agent coach mode",
    ]:
        assert phrase in scenario_matrix.lower()


def test_advocacy_operating_model_defines_standard_output() -> None:
    model = read("docs/customer-advocacy-operating-model.md")
    required_sections = [
        "Facts and Timeline",
        "Customer Goal",
        "Favorable Facts",
        "Risks and Weak Points",
        "Good-Faith Arguments to Preserve",
        "Evidence and Materials Checklist",
        "Compliance Boundary",
        "Next Actions",
        "Customer-Safe Language",
        "Agent Internal Notes",
        "Forbidden Moves",
        "Escalation Path",
    ]
    for section in required_sections:
        assert section in model

    assert "the carrier decides" in model
    assert "must be paired with concrete next steps" in model


def test_new_agent_coach_mode_is_first_class_service_pattern() -> None:
    skill = read("skills/insurance-copilot/SKILL.md")
    workflow = read("docs/workflow-surface.md")
    quickstart = read("docs/quickstart.md")

    for text in [skill, workflow, quickstart]:
        assert "New Agent Coach Mode" in text
        assert "what this situation is" in text
        assert "what to do first" in text
        assert "what not to do" in text
        assert "who to escalate to" in text


def test_empty_neutrality_gate_requires_action_plan() -> None:
    quality = read("docs/quality-gates.md")
    compliance = read("skills/insurance-copilot/references/compliance-starter.md")

    for text in [quality, compliance]:
        lowered = text.lower()
        assert "empty neutrality is insufficient" in lowered
        assert "以保险公司审核为准" in text
        assert "must be paired with" in lowered
        assert "evidence requests" in lowered
        assert "source checks" in lowered
        assert "escalation path" in lowered
        assert "customer-safe language" in lowered


def test_runtime_constraints_are_not_docs_only() -> None:
    doc_map = read("docs/documentation-map.md")
    skill = read("skills/insurance-copilot/SKILL.md")
    quality = read("docs/quality-gates.md")
    template = read("skills/insurance-copilot/templates/customer-advocacy-memo.md")

    for phrase in [
        "runtime-effective",
        "User-facing",
        "Runtime skill",
        "Maintainer governance",
        "Executable gates",
        "not every document is end-user reading",
    ]:
        assert phrase in doc_map

    for phrase in [
        "For substantive workflow work, load the matching reference before drafting",
        "docs/ is not the runtime source by itself",
        "runtime-effective constraints must live in SKILL.md, references, templates, evals, or validators",
        "templates/customer-advocacy-memo.md",
    ]:
        assert phrase in skill
        assert phrase in quality or phrase == "For substantive workflow work, load the matching reference before drafting"

    required_sections = [
        "Facts and Timeline",
        "Customer Goal",
        "Favorable Facts",
        "Risks and Weak Points",
        "Good-Faith Arguments to Preserve",
        "Evidence and Materials Checklist",
        "Compliance Boundary",
        "Next Actions",
        "Customer-Safe Language",
        "Agent Internal Notes",
        "Forbidden Moves",
        "Escalation Path",
    ]
    for section in required_sections:
        assert section in template

    assert "Empty neutrality is insufficient" in template
    assert "draft for licensed/compliance review" in template
    assert "do not send" in template.lower()

def test_systemic_eval_cases_cover_beyond_two_examples() -> None:
    required_cases = {
        "empty-neutrality-is-insufficient": "advocacy-operating-model",
        "new-agent-needs-coach-mode": "new-agent-coach-mode",
        "underwriting-postpone-reconsideration": "client-needs-intake",
        "claim-denial-appeal-path": "claims-triage",
        "policy-review-found-unclaimed-benefit": "policy-review",
        "replacement-customer-interest-protection": "replacement-suitability",
    }
    for case_id, workflow in required_cases.items():
        case_path = ROOT / "evals" / "cases" / f"{case_id}.json"
        data = json.loads(case_path.read_text(encoding="utf-8"))
        assert data["id"] == case_id
        assert data["workflow"] == workflow
        expected = read(data["expected_output"])
        for phrase in data["must_include"]:
            assert phrase in expected
        for phrase in data["must_not_include"]:
            assert phrase not in expected
