#!/usr/bin/env python3
"""Read-only local-file connectors for private Insurance Copilot workspaces.

The connector intentionally does not integrate with CRM, calendar, messaging,
carrier portals, or any network service. It reads local files and emits a Daily
Agent Workbench bundle for Hermes review workflows.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

VERIFY = "[verify]"


@dataclass
class MarkdownRecord:
    path: str
    title: str
    record_type: str
    text: str


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def is_relative_to(path: Path, parent: Path) -> bool:
    """Return True when path is inside parent after symlink resolution."""
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def safe_input_file(path: Path, workspace: Path) -> bool:
    """Accept only regular, non-symlink files whose resolved path stays inside workspace."""
    if path.is_symlink() or not path.is_file():
        return False
    workspace_resolved = workspace.resolve()
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        return False
    return is_relative_to(resolved, workspace_resolved)


def strip_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body_start = text.find("\n", end + 4)
    body = text[body_start + 1 :] if body_start != -1 else ""
    data: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"\'')
        if value.lower() == "true":
            data[key.strip()] = True
        elif value.lower() == "false":
            data[key.strip()] = False
        else:
            data[key.strip()] = value
    return data, body


def first_heading(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def collect_markdown_records(workspace: Path, dirname: str, default_type: str) -> list[MarkdownRecord]:
    directory = workspace / dirname
    if not directory.exists():
        return []
    records: list[MarkdownRecord] = []
    for path in sorted(directory.rglob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        if not safe_input_file(path, workspace):
            continue
        text = read_text(path)
        frontmatter, body = strip_frontmatter(text)
        record_type = str(frontmatter.get("type") or default_type)
        title = first_heading(body, path.stem)
        records.append(
            MarkdownRecord(
                path=str(path.relative_to(workspace)),
                title=title,
                record_type=record_type,
                text=body.strip(),
            )
        )
    return records


def normalize_cell(value: str | None, default: str = "") -> str:
    value = (value or "").strip()
    return value if value else default


def parse_date(value: str | None) -> date | None:
    value = (value or "").strip()
    if not value or value.upper().startswith("YYYY"):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def read_renewals(workspace: Path) -> list[dict[str, str]]:
    directory = workspace / "renewal-registers"
    if not directory.exists():
        return []
    rows: list[dict[str, str]] = []
    for path in sorted(directory.glob("*.csv")):
        if not safe_input_file(path, workspace):
            continue
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                normalized = {key: normalize_cell(value) for key, value in row.items() if key is not None}
                normalized["source_file"] = str(path.relative_to(workspace))
                normalized["customer_ref"] = normalize_cell(normalized.get("customer_ref"), "SYN-UNKNOWN-CUSTOMER")
                normalized["policy_ref"] = normalize_cell(normalized.get("policy_ref"), "SYN-UNKNOWN-POLICY")
                normalized["status_source"] = normalize_cell(normalized.get("status_source"), VERIFY)
                normalized["status_as_of"] = normalize_cell(normalized.get("status_as_of"), VERIFY)
                normalized["next_action"] = normalize_cell(normalized.get("next_action"), "verify status before customer outreach")
                rows.append(normalized)
    rows.sort(key=lambda row: (parse_date(row.get("premium_due_date")) or date.max, parse_date(row.get("grace_period_end")) or date.max, row.get("policy_ref", "")))
    return rows


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def build_bundle(workspace: Path) -> dict[str, Any]:
    renewals = read_renewals(workspace)
    customers = collect_markdown_records(workspace, "clients", "customer")
    # Some teams prefer `customers/`; support it without requiring it.
    customers += collect_markdown_records(workspace, "customers", "customer")
    meetings = collect_markdown_records(workspace, "meetings", "meeting-note")
    policies = collect_markdown_records(workspace, "policies", "policy-summary")
    claims = collect_markdown_records(workspace, "claims", "claim-tracker")
    referrals = collect_markdown_records(workspace, "referrals", "referral-tracker")
    tasks = collect_markdown_records(workspace, "tasks", "task-list")

    high_risk: list[str] = []
    for row in renewals:
        risk_text = " ".join(str(row.get(key, "")) for key in ["review_flags", "next_action", "status_source", "status_as_of"])
        if contains_any(risk_text, ["lapse", "grace", "complaint", "vulnerable", "replacement", "surrender", "[verify]"]):
            high_risk.append(f"Renewal/lapse: {row.get('policy_ref')} for {row.get('customer_ref')} — status {row.get('status_source', VERIFY)}; {row.get('review_flags') or row.get('next_action')}")
    for record in claims:
        high_risk.append(f"Claim support: {record.title} — do not promise coverage or payout; verify carrier instructions.")
    for record in policies:
        if VERIFY in record.text or contains_any(record.text, ["replacement", "surrender", "cash value", "lapse"]):
            high_risk.append(f"Policy review: {record.title} — source/status needs verification before customer statements.")

    priorities: list[str] = []
    if high_risk:
        priorities.append("Review high-risk renewal/lapse, claim, policy-status, or replacement-sensitive items first.")
    if meetings:
        priorities.append(f"Prepare for {len(meetings)} meeting(s) using missing-fact questions before product discussion.")
    if renewals:
        priorities.append(f"Verify {len(renewals)} renewal/payment item(s) against carrier source before outreach.")
    if referrals:
        priorities.append(f"Review {len(referrals)} referral item(s) for consent, incentive, and channel restrictions.")
    if tasks:
        priorities.append(f"Convert {len(tasks)} private task list(s) into reviewed CRM/calendar draft tasks only.")
    if not priorities:
        priorities.append("No dated items found; run Agency Playbook Builder or add synthetic/private workspace records.")

    return {
        "generated_by": "scripts/local_file_connectors.py",
        "workflow": "Daily Agent Workbench",
        "workspace": str(workspace),
        "read_only": True,
        "no_external_writes": True,
        "review_notice": "Draft for licensed/compliance review; do not send, schedule, or write externally.",
        "counts": {
            "renewals": len(renewals),
            "customers": len(customers),
            "meetings": len(meetings),
            "policies": len(policies),
            "claims": len(claims),
            "referrals": len(referrals),
            "tasks": len(tasks),
        },
        "todays_priorities": priorities,
        "high_risk_items": high_risk,
        "renewals": renewals,
        "customers": [asdict(record) for record in customers],
        "meetings": [asdict(record) for record in meetings],
        "policies": [asdict(record) for record in policies],
        "claims": [asdict(record) for record in claims],
        "referrals": [asdict(record) for record in referrals],
        "tasks": [asdict(record) for record in tasks],
        "verify_before_action": [
            "[verify] carrier policy/payment/claim status before any customer statement.",
            "[verify] approved script or practice profile before sending customer-facing copy.",
            "[verify] referral consent and incentive/anti-rebating rules before referral outreach.",
        ],
    }


def render_markdown(bundle: dict[str, Any]) -> str:
    display_workspace = Path(bundle["workspace"]).name
    lines: list[str] = [
        "# Daily Agent Workbench Connector Bundle",
        "",
        "> Draft for licensed/compliance review; do not send, schedule, or write externally.",
        "",
        "## Scope",
        f"- Workspace: `{display_workspace}`",
        "- Connector mode: read-only local files",
        "- Review owner: licensed agent; compliance reviewer for customer-facing/high-risk items",
        "",
        "## Today's Priorities",
    ]
    for idx, item in enumerate(bundle["todays_priorities"], 1):
        lines.append(f"{idx}. {item}")

    lines += ["", "## High-Risk Items"]
    if bundle["high_risk_items"]:
        for item in bundle["high_risk_items"]:
            lines.append(f"- {item}")
    else:
        lines.append("- None detected from local files; still apply practice profile and review gates.")

    lines += ["", "## Renewal / Lapse Items"]
    if bundle["renewals"]:
        for row in bundle["renewals"]:
            lines.extend(
                [
                    f"- Policy: {row.get('policy_ref', VERIFY)} / Customer: {row.get('customer_ref', VERIFY)}",
                    f"  - Premium due: {row.get('premium_due_date') or VERIFY}",
                    f"  - Grace period end: {row.get('grace_period_end') or VERIFY}",
                    f"  - Status source: {row.get('status_source') or VERIFY}",
                    f"  - Next action: {row.get('next_action') or 'verify before outreach'}",
                ]
            )
    else:
        lines.append("- No renewal register rows found.")

    lines += ["", "## Customer / Meeting / Policy Inputs"]
    for label, key in [("Customers", "customers"), ("Meetings", "meetings"), ("Policies", "policies"), ("Claims", "claims"), ("Referrals", "referrals"), ("Tasks", "tasks")]:
        lines.append(f"### {label}")
        records = bundle[key]
        if not records:
            lines.append("- None found.")
            continue
        for record in records:
            lines.append(f"- {record['title']} (`{record['path']}`) — type: {record['record_type']}")

    lines += ["", "## Draft Talk Tracks", "> Draft for licensed/compliance review; do not send automatically.", ""]
    if bundle["renewals"]:
        lines.append("- Renewal reminder draft: Please verify the official carrier/payment status before telling the customer anything about coverage, grace period, or lapse.")
    if bundle["claims"]:
        lines.append("- Claim support draft: I can help organize documents and carrier instructions, but final coverage or payout depends on carrier claim review.")
    if bundle["referrals"]:
        lines.append("- Referral draft: Use only low-pressure opt-out language after consent and incentive rules are verified.")
    if not (bundle["renewals"] or bundle["claims"] or bundle["referrals"]):
        lines.append("- No customer-facing draft needed from current local files.")

    lines += ["", "## Verify Before Action"]
    for item in bundle["verify_before_action"]:
        lines.append(f"- {item}")

    lines += ["", "## CRM/Calendar Task Export Draft"]
    for item in bundle["todays_priorities"]:
        lines.extend(["- Task:", "  - Owner: assigned agent", "  - Due: [verify]", f"  - Notes: {item}", "  - External write allowed: no, draft only."])

    lines += ["", "## No External Writes", "- This connector only reads local files and emits a bundle.", "- It does not send messages, update CRM/calendar, contact carriers, file claims, submit applications, or change policies."]
    return "\n".join(lines).rstrip() + "\n"


def command_daily_workbench(args: argparse.Namespace) -> int:
    workspace = args.workspace.resolve()
    if not workspace.exists() or not workspace.is_dir():
        return fail(f"workspace directory missing: {workspace}")
    workspace_resolved = workspace.resolve()
    bundle = build_bundle(workspace)
    if args.format == "json":
        output = json.dumps(bundle, ensure_ascii=False, indent=2)
    else:
        output = render_markdown(bundle)
    if args.output:
        out = args.output.resolve()
        if is_relative_to(out, workspace_resolved):
            return fail(f"output path must be outside the workspace: {out}")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(output, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only local-file connectors for Insurance Copilot private workspaces")
    sub = parser.add_subparsers(dest="command", required=True)
    daily = sub.add_parser("daily-workbench", help="Build a Daily Agent Workbench bundle from a local workspace")
    daily.add_argument("--workspace", required=True, type=Path, help="Private or synthetic agent workspace root")
    daily.add_argument("--format", choices=["markdown", "json"], default="markdown")
    daily.add_argument("--output", type=Path, help="Optional explicit output file; stdout is used by default")
    daily.set_defaults(func=command_daily_workbench)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
