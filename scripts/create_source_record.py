#!/usr/bin/env python3
"""Create a public institution-pack source record."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "source"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--institution", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-type", default="official-product-page")
    parser.add_argument("--jurisdiction", action="append", default=[])
    parser.add_argument("--language", default="zh-Hans")
    parser.add_argument("--product-line", action="append", default=[])
    parser.add_argument("--submitted-by", default="unknown")
    parser.add_argument("--redistribution-mode", default="link-only", choices=["link-only", "summary-allowed", "full-text-allowed"])
    args = parser.parse_args()

    pack = ROOT / "knowledge" / "institutions" / args.institution
    outdir = pack / "sources"
    outdir.mkdir(parents=True, exist_ok=True)
    sid = f"{args.institution}-{date.today().isoformat()}-{slugify(args.title)}"
    path = outdir / f"{sid}.yaml"
    content = f"""id: {sid}
institution: {args.institution}
jurisdiction: {args.jurisdiction}
language: {args.language}
source_type: {args.source_type}
source_url: {args.url}
retrieved_at: {date.today().isoformat()}
public_source: true
redistribution:
  mode: {args.redistribution_mode}
  notes: "Generated source record. Verify redistribution before copying source text."
product_lines: {args.product_line}
status: queued
submitted_by: {args.submitted_by}
notes: "{args.title}"
"""
    path.write_text(content)
    print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
