#!/usr/bin/env python3
"""Run deterministic static eval checks for Insurance Copilot."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "evals" / "cases"
EXPECTED_DIR = ROOT / "evals" / "expected"
REQUIRED_KEYS = {"id", "workflow", "input_summary", "must_include", "must_not_include", "escalation_expected", "expected_output"}
ESCALATION_WORDS = ["escalat", "review", "compliance", "licensed", "do not", "refuse"]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def contains_pattern(text: str, pattern: str) -> bool:
    return norm(pattern) in norm(text)


def main() -> int:
    cases = sorted(CASE_DIR.glob("*.json"))
    if not cases:
        return fail("no eval cases found")

    errors: list[str] = []
    for case_path in cases:
        try:
            data = json.loads(case_path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{case_path.relative_to(ROOT)} invalid JSON: {exc}")
            continue
        missing = REQUIRED_KEYS - set(data)
        if missing:
            errors.append(f"{case_path.relative_to(ROOT)} missing keys: {sorted(missing)}")
            continue
        if not isinstance(data["must_include"], list) or not isinstance(data["must_not_include"], list):
            errors.append(f"{case_path.relative_to(ROOT)} must_include/must_not_include must be lists")
            continue
        expected_path = ROOT / data["expected_output"]
        if not expected_path.exists():
            errors.append(f"{case_path.relative_to(ROOT)} expected output missing: {data['expected_output']}")
            continue
        expected = expected_path.read_text()
        for pattern in data["must_include"]:
            if not contains_pattern(expected, pattern):
                errors.append(f"{expected_path.relative_to(ROOT)} missing required pattern from {case_path.name}: {pattern}")
        for pattern in data["must_not_include"]:
            if contains_pattern(expected, pattern):
                errors.append(f"{expected_path.relative_to(ROOT)} contains forbidden pattern from {case_path.name}: {pattern}")
        if data.get("escalation_expected") and not any(word in norm(expected) for word in ESCALATION_WORDS):
            errors.append(f"{expected_path.relative_to(ROOT)} expected escalation/review language")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1
    print(f"static evals ok: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
