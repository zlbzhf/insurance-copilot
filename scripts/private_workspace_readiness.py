#!/usr/bin/env python3
"""Generate a deterministic private-workspace readiness report.

This validator is intentionally read-only. It checks whether a local agent
workspace is structurally and operationally ready for a future script-only
renewal watcher deployment. It does not create cron jobs, send messages, write
CRM/calendar records, contact carriers, or mutate the workspace.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

REQUIRED_DIRS = [
    "clients",
    "meetings",
    "policies",
    "claims",
    "referrals",
    "tasks",
    "renewal-registers",
]
REQUIRED_FILES = ["README.md"]
RETENTION_FILES = ["RETENTION.md", "retention.md", "AUDIT.md", "audit.md"]
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".yaml", ".yml"}
RENEWAL_REQUIRED_FIELDS = {
    "customer_ref",
    "policy_ref",
    "carrier",
    "product_category",
    "premium_due_date",
    "grace_period_end",
    "status_source",
    "status_as_of",
    "last_contact",
    "next_action",
    "review_flags",
}
PII_PATTERNS = {
    "ssn-like": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit-card-like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "email-like": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
}


@dataclass
class Check:
    id: str
    status: str
    detail: str


@dataclass
class Risk:
    id: str
    severity: str
    detail: str


def fail(msg: str) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return 2


def parse_date(value: str, label: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"invalid {label} date: {value}") from exc


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def safe_relative(path: Path, workspace: Path) -> str:
    try:
        return str(path.relative_to(workspace))
    except ValueError:
        return str(path)


def workspace_files(workspace: Path) -> list[Path]:
    return sorted(p for p in workspace.rglob("*") if p.is_file() and not p.is_symlink())


def assert_output_safe(workspace: Path, output: Path | None) -> tuple[bool, str]:
    if output is None:
        return True, "stdout"
    output_abs = output.expanduser().resolve()
    if is_relative_to(output_abs, workspace):
        return False, f"output path must be outside workspace: {output_abs}"
    if output.exists():
        for source in workspace_files(workspace):
            try:
                if output.samefile(source):
                    return False, f"output path must not overwrite workspace file: {output_abs}"
            except FileNotFoundError:
                continue
    return True, str(output_abs)


def safe_required_dir(workspace: Path, name: str, risks: list[Risk]) -> bool:
    path = workspace / name
    if not path.exists():
        risks.append(Risk("missing-required-directory", "blocker", f"missing directory: {name}/"))
        return False
    if path.is_symlink():
        risks.append(Risk("symlinked-workspace-path", "blocker", f"required directory must not be a symlink: {name}/"))
        return False
    if not path.is_dir():
        risks.append(Risk("missing-required-directory", "blocker", f"required path is not a directory: {name}/"))
        return False
    resolved = path.resolve(strict=True)
    if not is_relative_to(resolved, workspace):
        risks.append(Risk("path-outside-workspace", "blocker", f"required directory resolves outside workspace: {name}/"))
        return False
    return True


def safe_required_file(workspace: Path, name: str, risks: list[Risk]) -> bool:
    path = workspace / name
    if not path.exists():
        risks.append(Risk("missing-required-file", "blocker", f"missing file: {name}"))
        return False
    if path.is_symlink():
        risks.append(Risk("symlinked-workspace-path", "blocker", f"required file must not be a symlink: {name}"))
        return False
    if not path.is_file():
        risks.append(Risk("missing-required-file", "blocker", f"required path is not a file: {name}"))
        return False
    resolved = path.resolve(strict=True)
    if not is_relative_to(resolved, workspace):
        risks.append(Risk("path-outside-workspace", "blocker", f"required file resolves outside workspace: {name}"))
        return False
    return True


def iter_text_files(workspace: Path) -> Iterable[Path]:
    for path in sorted(workspace.rglob("*")):
        if path.is_symlink():
            continue
        if not path.is_file():
            continue
        try:
            resolved = path.resolve(strict=True)
        except FileNotFoundError:
            continue
        if not is_relative_to(resolved, workspace):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def find_renewal_registers(workspace: Path) -> list[Path]:
    root = workspace / "renewal-registers"
    if not root.exists() or root.is_symlink() or not root.is_dir():
        return []
    registers: list[Path] = []
    for p in root.glob("*.csv"):
        if p.is_symlink() or not p.is_file():
            continue
        try:
            resolved = p.resolve(strict=True)
        except FileNotFoundError:
            continue
        if is_relative_to(resolved, workspace):
            registers.append(p)
    return sorted(registers)


def read_register_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    return rows, fields


def check_structure(workspace: Path, checks: list[Check], risks: list[Risk]) -> None:
    before = len(risks)
    for name in REQUIRED_DIRS:
        safe_required_dir(workspace, name, risks)
    for name in REQUIRED_FILES:
        safe_required_file(workspace, name, risks)
    if len(risks) > before:
        checks.append(Check("required-structure", "fail", "missing, invalid, or symlinked required workspace paths"))
    else:
        checks.append(Check("required-structure", "pass", "required workspace directories and README.md are present as regular in-workspace paths"))


def first_safe_policy_file(workspace: Path) -> Path | None:
    for name in RETENTION_FILES:
        path = workspace / name
        if not path.exists() or path.is_symlink() or not path.is_file():
            continue
        try:
            resolved = path.resolve(strict=True)
        except FileNotFoundError:
            continue
        if is_relative_to(resolved, workspace):
            return path
    return None


def check_retention_audit(workspace: Path, checks: list[Check], risks: list[Risk], actions: list[str]) -> None:
    found = first_safe_policy_file(workspace)
    log = workspace / "log.md"
    log_found = log.exists() and not log.is_symlink() and log.is_file() and is_relative_to(log.resolve(strict=True), workspace)
    if found and log_found:
        text = found.read_text(errors="ignore").lower()
        needed = ["retention", "audit"]
        if all(term in text for term in needed):
            checks.append(Check("retention-audit-policy", "pass", f"retention/audit policy present: {found.name}; log.md present"))
            return
    checks.append(Check("retention-audit-policy", "fail", "retention/audit policy and log.md must exist before scheduled monitoring"))
    risks.append(Risk("missing-retention-audit-policy", "blocker", "missing regular in-workspace RETENTION.md/AUDIT.md with retention and audit guidance, or missing regular in-workspace log.md"))
    actions.append("Add retention/audit policy with owner, log location, review cadence, and deletion/escalation rules.")


def check_privacy(workspace: Path, checks: list[Check], risks: list[Risk], synthetic_mode: bool) -> None:
    hits: list[str] = []
    for path in iter_text_files(workspace):
        text = path.read_text(errors="ignore")
        for label, pattern in PII_PATTERNS.items():
            if pattern.search(text):
                hits.append(f"{path.relative_to(workspace)}:{label}")
    if hits:
        severity = "blocker" if synthetic_mode else "warning"
        checks.append(Check("privacy-pii-scan", "fail" if synthetic_mode else "warn", f"possible PII patterns found: {len(hits)}"))
        for hit in hits[:20]:
            risks.append(Risk("possible-pii", severity, f"possible PII pattern in {hit}"))
        if len(hits) > 20:
            risks.append(Risk("possible-pii", severity, f"{len(hits) - 20} additional possible PII hits omitted"))
    else:
        checks.append(Check("privacy-pii-scan", "pass", "no basic PII-like patterns detected in text files"))


def add_unique_action(actions: list[str], action: str) -> None:
    if action not in actions:
        actions.append(action)


def row_ref(register: Path, workspace: Path, row: dict[str, str], index: int) -> str:
    policy = (row.get("policy_ref") or "[missing-policy-ref]").strip()
    return f"{safe_relative(register, workspace)} row {index} policy {policy}"


def check_renewal_freshness(workspace: Path, as_of: date, max_stale_days: int, checks: list[Check], risks: list[Risk], actions: list[str]) -> None:
    registers = find_renewal_registers(workspace)
    if not registers:
        checks.append(Check("renewal-register", "fail", "no regular in-workspace renewal register CSV found"))
        risks.append(Risk("missing-renewal-register", "blocker", "renewal-registers/*.csv is required before scheduled renewal watcher deployment"))
        add_unique_action(actions, "Add or export a renewal register CSV before enabling the scheduled watcher.")
        return

    total_rows = 0
    latest_status: date | None = None
    malformed: list[str] = []
    missing_dates: list[str] = []
    stale_rows: list[str] = []
    future_rows: list[str] = []
    for register in registers:
        try:
            rows, fields = read_register_rows(register)
        except Exception as exc:
            malformed.append(f"{safe_relative(register, workspace)} unreadable: {exc}")
            continue
        missing_fields = sorted(RENEWAL_REQUIRED_FIELDS.difference(fields))
        if missing_fields:
            malformed.append(f"{safe_relative(register, workspace)} missing fields: {', '.join(missing_fields)}")
        total_rows += len(rows)
        for index, row in enumerate(rows, start=2):
            raw = (row.get("status_as_of") or "").strip()
            ref = row_ref(register, workspace, row, index)
            if not raw:
                missing_dates.append(f"{ref} has blank status_as_of")
                continue
            try:
                parsed = parse_date(raw, "status_as_of")
            except ValueError:
                malformed.append(f"{ref} invalid status_as_of: {raw}")
                continue
            latest_status = parsed if latest_status is None else max(latest_status, parsed)
            age = (as_of - parsed).days
            if age < 0:
                future_rows.append(f"{ref} status_as_of {parsed} is after as-of {as_of}")
            elif age > max_stale_days:
                stale_rows.append(f"{ref} status_as_of {parsed} is {age} days old; max allowed is {max_stale_days}")

    if malformed:
        checks.append(Check("renewal-register", "fail", "renewal register schema/date issues found"))
        for item in malformed[:20]:
            risks.append(Risk("invalid-renewal-register", "blocker", item))
        add_unique_action(actions, "Fix renewal register schema and date values before enabling scheduled monitoring.")
    if total_rows == 0:
        checks.append(Check("renewal-register", "fail", "renewal register contains no rows"))
        risks.append(Risk("empty-renewal-register", "blocker", "renewal register CSV has headers but no rows"))
        add_unique_action(actions, "Export a non-empty renewal register or intentionally disable the renewal watcher.")
        return
    if missing_dates:
        checks.append(Check("renewal-register-freshness", "fail", f"{len(missing_dates)} renewal row(s) lack status_as_of freshness evidence"))
        for item in missing_dates[:20]:
            risks.append(Risk("missing-renewal-status-date", "blocker", item))
        add_unique_action(actions, "Refresh renewal register with current carrier/payment status timestamps.")
    if stale_rows:
        checks.append(Check("renewal-register-freshness", "fail", f"{len(stale_rows)} renewal row(s) exceed max stale days"))
        for item in stale_rows[:20]:
            risks.append(Risk("stale-renewal-register-row", "blocker", item))
        add_unique_action(actions, "Refresh renewal register from the carrier/agency source before scheduled monitoring.")
    if future_rows:
        checks.append(Check("renewal-register-freshness", "fail", f"{len(future_rows)} renewal row(s) have future status_as_of dates"))
        for item in future_rows[:20]:
            risks.append(Risk("future-renewal-register-date", "blocker", item))
        add_unique_action(actions, "Fix future-dated renewal register timestamps before scheduled monitoring.")
    if not malformed and not missing_dates and not stale_rows and not future_rows:
        if latest_status is None:
            checks.append(Check("renewal-register-freshness", "fail", "no status_as_of values found"))
            risks.append(Risk("stale-renewal-register", "blocker", "renewal register has no status_as_of values to prove freshness"))
            add_unique_action(actions, "Refresh renewal register with current carrier/payment status timestamps.")
        else:
            max_age = (as_of - latest_status).days
            checks.append(Check("renewal-register-freshness", "pass", f"all {total_rows} renewal row(s) have status_as_of within {max_stale_days} day(s); latest {latest_status}; newest age {max_age} day(s)"))


def build_report(workspace: Path, as_of: date, max_stale_days: int, synthetic_mode: bool) -> dict:
    checks: list[Check] = []
    risks: list[Risk] = []
    actions: list[str] = []

    check_structure(workspace, checks, risks)
    check_renewal_freshness(workspace, as_of, max_stale_days, checks, risks, actions)
    check_privacy(workspace, checks, risks, synthetic_mode)
    check_retention_audit(workspace, checks, risks, actions)

    checks.append(Check("output-boundary", "pass", "report output is stdout by default and explicit --output must be outside workspace and not same-file/hardlink any workspace file"))
    checks.append(Check("no-external-writes", "pass", "validator performs no network, customer-message, CRM, calendar, carrier, claim, application, or policy-change actions"))

    blocker_count = sum(1 for r in risks if r.severity == "blocker")
    warning_count = sum(1 for r in risks if r.severity == "warning")
    ready = blocker_count == 0
    if not ready and not actions:
        actions.append("Resolve blocker risks before creating a Hermes scheduled watcher job.")
    if ready:
        actions.append("Run one private dry run with no delivery before creating a live scheduled watcher.")
        actions.append("Confirm schedule, timezone, reviewer, and data retention owner before deployment.")

    return {
        "ready_for_cron": ready,
        "internal_only": True,
        "no_external_writes": True,
        "summary": {
            "workspace": str(workspace),
            "as_of": as_of.isoformat(),
            "max_stale_days": max_stale_days,
            "synthetic_mode": synthetic_mode,
            "blockers": blocker_count,
            "warnings": warning_count,
        },
        "checks": [asdict(c) for c in checks],
        "risks": [asdict(r) for r in risks],
        "recommended_next_actions": actions,
    }


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    verdict = "READY for private dry-run gate" if report["ready_for_cron"] else "NOT READY for scheduled watcher deployment"
    lines = [
        "# Private Workspace Readiness Report",
        "",
        "Draft for licensed/compliance/operations review.",
        "",
        "## Readiness Verdict",
        f"- Verdict: **{verdict}**",
        f"- Workspace: `{summary['workspace']}`",
        f"- As of: `{summary['as_of']}`",
        f"- Blockers: {summary['blockers']}",
        f"- Warnings: {summary['warnings']}",
        "- Internal only: true",
        "- No External Writes: true",
        "",
        "## Workspace Structure",
    ]
    for check in report["checks"]:
        if check["id"] in {"required-structure", "renewal-register", "renewal-register-freshness"}:
            lines.append(f"- {check['id']}: {check['status']} — {check['detail']}")
    lines.extend(["", "## Renewal Register Freshness"])
    for check in report["checks"]:
        if check["id"].startswith("renewal-register"):
            lines.append(f"- {check['status']}: {check['detail']}")
    lines.extend(["", "## Privacy / PII Scan"])
    for check in report["checks"]:
        if check["id"] == "privacy-pii-scan":
            lines.append(f"- {check['status']}: {check['detail']}")
    lines.extend(["", "## Output Boundary"])
    for check in report["checks"]:
        if check["id"] in {"output-boundary", "no-external-writes"}:
            lines.append(f"- {check['status']}: {check['detail']}")
    lines.extend([
        "",
        "## Retention / Audit Checklist",
        "- Confirm data retention owner and review cadence.",
        "- Confirm audit log location and reviewer/owner.",
        "- Confirm deletion/escalation rules for stale or unnecessary private data.",
    ])
    for check in report["checks"]:
        if check["id"] == "retention-audit-policy":
            lines.append(f"- {check['status']}: {check['detail']}")
    lines.extend(["", "## Risks"])
    if report["risks"]:
        for risk in report["risks"]:
            lines.append(f"- {risk['severity']} / {risk['id']}: {risk['detail']}")
    else:
        lines.append("- No blocker risks detected by deterministic checks.")
    lines.extend([
        "",
        "## Scheduled Watcher Deployment Gate",
        "- Do not create a live Hermes cron job until blockers are resolved and reviewer/schedule/timezone/data policy are approved.",
        "- Run one private dry run with no delivery before live delivery.",
        "- Keep renewal/lapse output internal-only and preserve `[verify]` markers.",
        "",
        "## Recommended Next Actions",
    ])
    for action in report["recommended_next_actions"]:
        lines.append(f"- {action}")
    lines.extend([
        "",
        "## Safety Boundary",
        "- This readiness report does not send customer messages, write CRM/calendar tasks, contact carriers, file claims, submit applications, or change policies.",
        "- No External Writes.",
    ])
    return "\n".join(lines) + "\n"


def write_or_print(content: str, output: Path | None) -> None:
    if output is None:
        print(content, end="")
    else:
        output_abs = output.expanduser().resolve()
        output_abs.parent.mkdir(parents=True, exist_ok=True)
        output_abs.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate private workspace readiness for scheduled renewal watcher deployment.")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--max-stale-days", type=int, default=7)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--synthetic-mode", action="store_true", help="Treat PII-like hits as blockers for synthetic/template workspaces.")
    args = parser.parse_args()

    workspace_input = args.workspace.expanduser()
    if workspace_input.is_symlink():
        return fail(f"workspace path must not be a symlink: {workspace_input}")
    workspace = workspace_input.resolve()
    if not workspace.exists() or not workspace.is_dir():
        return fail(f"workspace missing: {workspace}")
    try:
        as_of = parse_date(args.as_of, "--as-of")
    except ValueError as exc:
        return fail(str(exc))
    ok, msg = assert_output_safe(workspace, args.output)
    if not ok:
        return fail(msg)

    report = build_report(workspace, as_of, args.max_stale_days, args.synthetic_mode)
    if args.format == "json":
        content = json.dumps(report, indent=2, sort_keys=True) + "\n"
    else:
        content = render_markdown(report)
    write_or_print(content, args.output)
    return 0 if report["ready_for_cron"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
