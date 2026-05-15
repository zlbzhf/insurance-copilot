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
    assert "## Practical MVP: How an Agent Uses It" in text
    assert "## Recommended First Session" in text
    assert "workflow router, not a menu bot" in text
    assert "manual-first" in text

    mvp_pos = text.index("## Practical MVP: How an Agent Uses It")
    cron_pos = text.index("## Advanced / Later: Local Connectors and Watchers")
    validate_pos = text.index("## Developer Validation")
    assert mvp_pos < cron_pos < validate_pos

    early = text[:cron_pos]
    assert "cronjob(" not in early
    assert "Private Dry-Run Deployment Harness" not in early
    assert "Scheduled Watcher" not in early


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
