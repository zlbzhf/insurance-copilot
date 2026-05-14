#!/usr/bin/env python3
"""Internal-only renewal/lapse watcher for local Insurance Copilot inputs."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

VERIFY = "[verify]"


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def parse_date(value: str | None) -> date | None:
    value = (value or "").strip()
    if not value or value == VERIFY or value.upper().startswith("YYYY"):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def normalize(value: Any, default: str = "") -> str:
    value = "" if value is None else str(value)
    value = value.strip()
    return value if value else default


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_input_path(path: Path, workspace: Path | None = None, require_workspace_containment: bool = True) -> tuple[bool, str]:
    if not path.exists():
        return False, f"input file missing: {path}"
    if path.is_symlink() or not path.is_file():
        return False, f"input path must be a regular file: {path}"
    if workspace is not None and require_workspace_containment:
        workspace_resolved = workspace.resolve()
        try:
            resolved = path.resolve(strict=True)
        except OSError:
            return False, f"input path must be a regular file inside workspace: {path}"
        if not is_relative_to(resolved, workspace_resolved):
            return False, f"input path must be a regular file inside workspace: {path}"
    return True, ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({str(key): normalize(value) for key, value in row.items() if key is not None})
    return rows


def read_bundle_rows(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    renewals = data.get("renewals", [])
    if not isinstance(renewals, list):
        return []
    rows: list[dict[str, str]] = []
    for item in renewals:
        if isinstance(item, dict):
            rows.append({str(key): normalize(value) for key, value in item.items()})
    return rows


def classify(row: dict[str, str], as_of: date) -> tuple[str, int, str]:
    due = parse_date(row.get("premium_due_date"))
    grace_end = parse_date(row.get("grace_period_end"))
    status_source = normalize(row.get("status_source"), VERIFY)
    review_flags = normalize(row.get("review_flags"))
    next_action = normalize(row.get("next_action"))
    text = " ".join([status_source, review_flags, next_action]).lower()

    if due is None:
        return "verify-status", 90, "premium due date missing or invalid"

    days_to_due = (due - as_of).days
    if grace_end is not None and as_of > grace_end:
        return "grace-ended", 0, "grace period appears ended; verify carrier status before any statement"
    if grace_end is not None and due < as_of <= grace_end:
        days_to_grace_end = (grace_end - as_of).days
        if days_to_grace_end <= 7:
            return "grace-period-before-end", 1, f"{days_to_grace_end} day(s) before grace period end"
        if days_to_due == -1:
            return "D+1", 2, "1 day after premium due date"
        return "in-grace-period", 5, f"{abs(days_to_due)} day(s) after premium due date"
    if days_to_due == 30:
        return "D-30", 20, "30 days before premium due date"
    if days_to_due == 14:
        return "D-14", 15, "14 days before premium due date"
    if days_to_due == 7:
        return "D-7", 10, "7 days before premium due date"
    if days_to_due == -1:
        return "D+1", 2, "1 day after premium due date"
    if "lapse" in text or "grace" in text or status_source == VERIFY:
        return "verify-status", 50, "status/review flags require verification"
    return "monitor", 100, f"{days_to_due} day(s) to premium due date"


def build_alerts(rows: list[dict[str, str]], as_of: date) -> dict[str, Any]:
    alerts: list[dict[str, str | int]] = []
    for row in rows:
        bucket, priority, reason = classify(row, as_of)
        status_source = normalize(row.get("status_source"), VERIFY)
        alert = {
            "bucket": bucket,
            "priority": priority,
            "reason": reason,
            "customer_ref": normalize(row.get("customer_ref"), "SYN-UNKNOWN-CUSTOMER"),
            "policy_ref": normalize(row.get("policy_ref"), "SYN-UNKNOWN-POLICY"),
            "premium_due_date": normalize(row.get("premium_due_date"), VERIFY),
            "grace_period_end": normalize(row.get("grace_period_end"), VERIFY),
            "status_source": status_source if status_source else VERIFY,
            "status_as_of": normalize(row.get("status_as_of"), VERIFY),
            "next_action": normalize(row.get("next_action"), "verify status before outreach"),
            "review_flags": normalize(row.get("review_flags"), VERIFY),
        }
        alerts.append(alert)
    alerts.sort(key=lambda item: (int(item["priority"]), str(item["policy_ref"])))
    counts: dict[str, int] = {"total": len(alerts)}
    bucket_keys = {
        "D-30": "d_30",
        "D-14": "d_14",
        "D-7": "d_7",
        "D+1": "d_plus_1",
        "grace-period-before-end": "grace_period_before_end",
        "grace-ended": "grace_ended",
        "in-grace-period": "in_grace_period",
        "verify-status": "verify_status",
        "monitor": "monitor",
    }
    for key in bucket_keys.values():
        counts[key] = 0
    for alert in alerts:
        counts[bucket_keys.get(str(alert["bucket"]), "verify_status")] += 1
    return {
        "generated_by": "scripts/renewal_watcher.py",
        "workflow": "Local Renewal Watcher",
        "as_of": as_of.isoformat(),
        "internal_only": True,
        "no_external_writes": True,
        "review_notice": "Draft for licensed/compliance review; internal alert only.",
        "counts": counts,
        "alerts": alerts,
        "verify_before_action": [
            "[verify] carrier policy/payment status before any customer statement.",
            "[verify] grace period and lapse/reinstatement rules with official carrier source.",
            "[verify] approved script source and contact consent before outreach.",
        ],
    }


def render_markdown(bundle: dict[str, Any]) -> str:
    lines = [
        "# Internal Renewal Watcher Alert",
        "",
        "> Draft for licensed/compliance review; internal alert only. Do not send, schedule, or write externally.",
        "",
        "## Scope",
        f"- As of: {bundle['as_of']}",
        "- Mode: internal-only renewal/lapse watcher",
        "- Review owner: servicing agent; supervisor/compliance for lapse, grace-period, vulnerable-customer, complaint, or ambiguous-status items",
        "",
        "## Summary Counts",
    ]
    counts = bundle["counts"]
    for key in ["total", "d_30", "d_14", "d_7", "d_plus_1", "grace_period_before_end", "grace_ended", "verify_status"]:
        lines.append(f"- {key}: {counts.get(key, 0)}")

    lines += ["", "## Alerts"]
    for alert in bundle["alerts"]:
        lines.extend(
            [
                f"- Bucket: {alert['bucket']} / Policy: {alert['policy_ref']} / Customer: {alert['customer_ref']}",
                f"  - Reason: {alert['reason']}",
                f"  - Premium due: {alert['premium_due_date']}",
                f"  - Grace period end: {alert['grace_period_end']}",
                f"  - Status source: {alert['status_source']}",
                f"  - Status as of: {alert['status_as_of']}",
                f"  - Next internal action: {alert['next_action']}",
                f"  - Review flags: {alert['review_flags']}",
            ]
        )
    if not bundle["alerts"]:
        lines.append("- No renewal rows found; verify source configuration.")

    lines += ["", "## Draft Internal Follow-up Language", "> Draft for licensed/compliance review; do not send automatically.", ""]
    lines.append("- Internal note: Verify official carrier/payment status before describing coverage, lapse, grace period, reinstatement, or claim implications to any customer.")
    lines.append("- Customer-language placeholder: After verification and approval only, use a neutral reminder that payment/status should be checked with official carrier records; do not imply active, lapsed, or reinstated status.")

    lines += ["", "## Verify Before Action"]
    for item in bundle["verify_before_action"]:
        lines.append(f"- {item}")

    lines += ["", "## No External Writes", "- This watcher only reads local input and emits an internal alert.", "- It does not send customer messages, update CRM/calendar, contact carriers, file claims, submit applications, or change policies."]
    return "\n".join(lines).rstrip() + "\n"


def infer_csv_workspace(input_path: Path) -> Path | None:
    parts = input_path.parts
    if "renewal-registers" not in parts:
        return None
    idx = parts.index("renewal-registers")
    if idx == 0:
        return None
    return Path(*parts[:idx])


def same_existing_file(a: Path, b: Path) -> bool:
    try:
        return a.exists() and b.exists() and a.samefile(b)
    except OSError:
        return False


def command(args: argparse.Namespace) -> int:
    input_path = args.bundle or args.csv
    workspace = args.workspace.resolve() if args.workspace else None
    ok, msg = validate_input_path(input_path, workspace, require_workspace_containment=args.csv is not None)
    if not ok:
        return fail(msg)
    input_resolved = input_path.resolve()
    if args.bundle:
        rows = read_bundle_rows(input_path)
    else:
        rows = read_csv_rows(input_path)
        if workspace is None:
            workspace = infer_csv_workspace(input_resolved)
    as_of = parse_date(args.as_of)
    if as_of is None:
        return fail(f"invalid --as-of date: {args.as_of}")
    bundle = build_alerts(rows, as_of)
    output = json.dumps(bundle, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(bundle)
    if args.output:
        out = args.output.resolve()
        if out == input_resolved or same_existing_file(out, input_resolved):
            return fail(f"output path must not overwrite input: {out}")
        if workspace is not None and is_relative_to(out, workspace):
            return fail(f"output path must be outside the workspace: {out}")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(output, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Internal-only local renewal/lapse watcher")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--bundle", type=Path, help="JSON bundle from local_file_connectors.py")
    source.add_argument("--csv", type=Path, help="Direct renewal register CSV")
    parser.add_argument("--workspace", type=Path, help="Optional workspace boundary for input/output path safety")
    parser.add_argument("--as-of", required=True, help="As-of date YYYY-MM-DD")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path, help="Optional explicit output file; stdout is default")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return command(args)


if __name__ == "__main__":
    raise SystemExit(main())
