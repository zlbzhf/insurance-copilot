#!/usr/bin/env python3
"""Deterministic public-knowledge ingestion gateway prototype.

This gateway is intentionally conservative. It does not call an LLM by default and does not merge
anything into `knowledge/`. It validates a source record, classifies the source using the active
taxonomy, writes normalized staging artifacts, and emits schema-gap placeholders when the current
standard cannot safely map the material.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "staging"

PII_PATTERNS = {
    "ssn-like": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit-card-like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "email-like": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone-like": re.compile(r"(?<!\d)(?:\+?\d{1,3}[ -]?)?(?:\(?\d{3}\)?[ -]?)\d{3}[ -]?\d{4}(?!\d)"),
}
PRIVATE_TERMS = ["private", "confidential", "internal only", "customer", "客户", "内部", "机密", "保密"]

KEYWORD_CLASSIFIERS = [
    ("regulator-guidance", ["regulator", "regulation", "监管", "金管", "保监", "circular", "guideline"]),
    ("official-terms", ["policy contract", "terms and conditions", "exclusion", "definitions", "条款", "合同", "除外", "保险责任"]),
    ("official-service-guide", ["claim", "claims", "renewal", "lapse", "reinstatement", "premium payment", "理赔", "续保", "复效", "缴费"]),
    ("official-underwriting-guide", ["underwriting", "application", "disclosure", "核保", "投保", "告知"]),
    ("approved-marketing-material", ["campaign", "social post", "sales script", "marketing", "seminar", "营销", "话术", "朋友圈", "海报"]),
    ("official-brochure", ["brochure", "leaflet", "sales aid", "产品宣传", "简介", "单页"]),
    ("official-faq", ["faq", "frequently asked", "help center", "常见问题", "问答"]),
    ("official-product-page", ["product", "benefit", "coverage", "rider", "产品", "保障", "附加险"]),
]


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml:
        data = yaml.safe_load(text) or {}
    else:
        data: dict[str, Any] = {}
        for line in text.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip().strip("'\"")
    if not isinstance(data, dict):
        raise ValueError(f"{path} must parse as a mapping")
    return data


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml:
        text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    else:
        text = json.dumps(data, indent=2, ensure_ascii=False)
    path.write_text(text, encoding="utf-8")


def slug(s: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return value or "source"


def flatten_source_text(source: dict[str, Any], raw_text: str) -> str:
    bits = [str(source.get("id", "")), str(source.get("source_type", "")), str(source.get("source_url", "")), str(source.get("title", "")), raw_text]
    return "\n".join(bits).lower()


def load_taxonomy() -> dict[str, Any]:
    return load_yaml(ROOT / "standards" / "source-taxonomy.yaml")


def load_page_registry() -> dict[str, Any]:
    return load_yaml(ROOT / "standards" / "page-type-registry.yaml")


def canonical_source_type(source: dict[str, Any], raw_text: str, taxonomy: dict[str, Any]) -> tuple[str, list[str], str]:
    source_types = taxonomy.get("source_types", {})
    declared = str(source.get("source_type", "unknown") or "unknown")
    if declared in source_types:
        return declared, [], "high"
    for canonical, cfg in source_types.items():
        aliases = cfg.get("aliases", []) if isinstance(cfg, dict) else []
        if declared in aliases:
            return canonical, [declared], "high"
    haystack = flatten_source_text(source, raw_text)
    scores: list[tuple[int, str]] = []
    for canonical, keywords in KEYWORD_CLASSIFIERS:
        score = sum(1 for kw in keywords if kw.lower() in haystack)
        if score:
            scores.append((score, canonical))
    if scores:
        scores.sort(reverse=True)
        primary = scores[0][1]
        secondary = [item[1] for item in scores[1:3] if item[1] != primary]
        confidence = "medium" if scores[0][0] >= 2 else "low"
        return primary, secondary, confidence
    return "unknown", [], "low"


def recommended_page_types(primary: str, secondary: list[str], taxonomy: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    source_types = taxonomy.get("source_types", {})
    page_types = registry.get("page_types", {})
    rec: list[str] = []
    for stype in [primary] + secondary:
        allowed = source_types.get(stype, {}).get("allowed_page_types", []) if isinstance(source_types.get(stype), dict) else []
        for page_type in allowed:
            if page_type in page_types and page_type not in rec:
                rec.append(page_type)
    return rec


def risk_flags(primary: str, secondary: list[str], taxonomy: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    for stype in [primary] + secondary:
        cfg = taxonomy.get("source_types", {}).get(stype, {})
        if isinstance(cfg, dict):
            for flag in cfg.get("risk_flags", []):
                if flag not in flags:
                    flags.append(flag)
    return flags


def privacy_findings(source: dict[str, Any], raw_text: str) -> list[str]:
    findings: list[str] = []
    text = (json.dumps(source, ensure_ascii=False, default=str) + "\n" + raw_text).lower()
    if source.get("public_source") is not True:
        findings.append("public_source_not_true")
    for key in ["contains_customer_data", "contains_internal_confidential_data"]:
        if source.get(key) is True:
            findings.append(key)
    for term in PRIVATE_TERMS:
        if term.lower() in text:
            # Chinese terms can be legitimate in warnings; still surface for human review instead of hard reject here.
            findings.append(f"private-term:{term}")
    for label, pattern in PII_PATTERNS.items():
        if pattern.search(raw_text):
            findings.append(f"possible-{label}")
    return findings


def build_classification(source: dict[str, Any], raw_text: str) -> dict[str, Any]:
    taxonomy = load_taxonomy()
    registry = load_page_registry()
    primary, secondary, confidence = canonical_source_type(source, raw_text, taxonomy)
    rec_pages = recommended_page_types(primary, secondary, taxonomy, registry)
    findings = privacy_findings(source, raw_text)
    gaps = []
    if primary == "unknown" or not rec_pages:
        gaps.append({
            "gap_id": f"gap-{slug(str(source.get('id', 'unknown')))}-classification",
            "status": "observed",
            "trigger_sources": [source.get("id", "unknown")],
            "problem": "Source could not be safely mapped to an active source type and page type.",
            "recommended_action": "Review the real source and either classify it with an existing type or propose a schema change.",
        })
    return {
        "source_id": source.get("id"),
        "primary_type": primary,
        "secondary_types": secondary,
        "confidence": confidence,
        "public_boundary": {
            "public_source": source.get("public_source") is True,
            "contains_customer_data": source.get("contains_customer_data") is True,
            "contains_internal_confidential_data": source.get("contains_internal_confidential_data") is True,
            "findings": findings,
        },
        "recommended_page_types": rec_pages,
        "risk_flags": risk_flags(primary, secondary, taxonomy),
        "schema_gaps": gaps,
    }


def build_extraction(source: dict[str, Any], classification: dict[str, Any], raw_text: str) -> dict[str, Any]:
    claims = []
    if raw_text.strip():
        # Deterministic placeholder: split into short paragraphs, keep as candidate summary claims.
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", raw_text) if len(p.strip()) >= 40]
        for idx, para in enumerate(paragraphs[:5], start=1):
            claims.append({
                "claim_id": f"claim-{idx:03d}",
                "claim_type": "candidate-summary",
                "text": para[:500],
                "source_locator": f"raw paragraph {idx}",
                "confidence": "low",
                "requires_verification": True,
                "risk_flags": classification.get("risk_flags", []),
            })
    completeness = 1.0 if claims else 0.25
    provenance = 1.0 if claims else 0.0
    return {
        "source_id": source.get("id"),
        "schema_version": str(source.get("schema_version") or load_yaml(ROOT / "standards" / "current.yaml").get("current_schema_version")),
        "segments": [],
        "claims": claims,
        "schema_gaps": classification.get("schema_gaps", []),
        "quality": {
            "provenance_coverage": provenance,
            "required_fields_complete": completeness,
            "human_reviewed": False,
            "notes": "Deterministic gateway prototype. LLM-assisted extraction can replace candidate-summary claims after maintainer-approved processing.",
        },
    }


def render_candidate_page(source: dict[str, Any], classification: dict[str, Any], extraction: dict[str, Any], output_dir: Path) -> list[Path]:
    registry = load_page_registry().get("page_types", {})
    rendered: list[Path] = []
    for page_type in classification.get("recommended_page_types", [])[:2]:
        cfg = registry.get(page_type)
        if not isinstance(cfg, dict):
            continue
        required = cfg.get("required_sections", [])
        directory = cfg.get("directory", "source-summaries")
        title = str(source.get("title") or source.get("id") or "Source")
        page_slug = slug(f"{source.get('id', 'source')}-{page_type}")
        path = output_dir / "proposed-pages" / directory / f"{page_slug}.md"
        sources = [f"sources/{source.get('id')}.yaml"]
        fm = {
            "title": f"{title} — {page_type}",
            "created": str(date.today()),
            "updated": str(date.today()),
            "type": page_type,
            "institution": source.get("institution"),
            "jurisdiction": source.get("jurisdiction", []),
            "language": source.get("language", "unknown"),
            "tags": ["public-source", "needs-verification"],
            "sources": sources,
            "confidence": "low",
            "public_source": True,
            "needs_verification": True,
            "schema_version": extraction.get("schema_version"),
            "human_reviewed": False,
        }
        body = ["---"]
        if yaml:
            body.append(yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip())
        else:
            body.append(json.dumps(fm, indent=2, ensure_ascii=False))
        body.extend(["---", "", f"# {title} — {page_type}", ""])
        body.extend([
            "<!-- Generated by deterministic ingestion gateway. Human review required before merging into knowledge/. -->",
            "",
        ])
        for section in required:
            body.append(f"## {section}")
            if section == "Source Status":
                body.extend([
                    f"- Source record: `{sources[0]}`",
                    f"- Classified source type: `{classification.get('primary_type')}`",
                    f"- Confidence: low",
                    "- Needs verification: yes",
                    "",
                ])
            elif section in {"Related Concepts", "Related Pages", "Sources / Verify"}:
                body.extend(["- [[source-verification]]", "",])
            elif section in {"Open Questions / Verify", "Limits / Verify", "Verify"}:
                body.extend(["- `[verify]` Confirm currentness against official public sources.", "",])
            else:
                claims = extraction.get("claims", [])
                if claims:
                    body.append(f"- `[verify]` Candidate extraction: {claims[0]['text'][:220]}")
                else:
                    body.append("- `[verify]` No validated extraction yet.")
                body.append("")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(body), encoding="utf-8")
        rendered.append(path)
    return rendered


def validation_report(source: dict[str, Any], classification: dict[str, Any], extraction: dict[str, Any], rendered: list[Path]) -> str:
    findings = classification.get("public_boundary", {}).get("findings", [])
    score = 0.0
    if source.get("public_source") is True:
        score += 0.25
    if not findings:
        score += 0.25
    if classification.get("recommended_page_types"):
        score += 0.2
    if extraction.get("quality", {}).get("provenance_coverage", 0) >= 0.8:
        score += 0.2
    if rendered:
        score += 0.1
    status = "pass" if score >= 0.75 and not findings else "review"
    lines = [
        "# Gateway Validation Report",
        "",
        f"- Source ID: `{source.get('id')}`",
        f"- Institution: `{source.get('institution')}`",
        f"- Primary type: `{classification.get('primary_type')}`",
        f"- Recommended page types: {', '.join(classification.get('recommended_page_types', [])) or 'none'}",
        f"- Quality score: {score:.2f}",
        f"- Status: {status}",
        f"- Human review required: yes",
        "",
        "## Public Boundary Findings",
    ]
    if findings:
        lines.extend([f"- {item}" for item in findings])
    else:
        lines.append("- none")
    lines.extend(["", "## Schema Gaps"])
    gaps = classification.get("schema_gaps", []) + extraction.get("schema_gaps", [])
    if gaps:
        for gap in gaps:
            lines.append(f"- `{gap.get('gap_id')}`: {gap.get('problem')}")
    else:
        lines.append("- none")
    lines.extend(["", "## Rendered Candidate Pages"])
    if rendered:
        lines.extend([f"- `{p.relative_to(output_root_for(source))}`" if p.is_relative_to(output_root_for(source)) else f"- `{p}`" for p in rendered])
    else:
        lines.append("- none")
    lines.extend(["", "## Merge Guidance", "", "Do not merge generated staging output directly. Move reviewed content into `knowledge/institutions/<institution>/` only after validator and maintainer review."])
    return "\n".join(lines) + "\n"


def output_root_for(source: dict[str, Any], output_root: Path | None = None) -> Path:
    root = output_root or DEFAULT_OUTPUT_ROOT
    return root / str(source.get("institution", "unknown")) / str(source.get("id", "unknown"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_record", type=Path, help="Path to a source-record YAML file")
    parser.add_argument("--raw-text", type=Path, help="Optional raw text/markdown excerpt for deterministic candidate claims")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Staging output root")
    parser.add_argument("--dry-run", action="store_true", help="Print classification without writing staging files")
    args = parser.parse_args()

    try:
        source = load_yaml(args.source_record)
    except Exception as exc:
        return fail(f"invalid source record: {exc}")

    for key in ["id", "institution", "source_type", "retrieved_at", "public_source", "redistribution"]:
        if key not in source:
            return fail(f"source record missing {key}")
    if source.get("public_source") is not True:
        return fail("source record must set public_source: true")

    raw_text = args.raw_text.read_text(encoding="utf-8", errors="ignore") if args.raw_text else ""
    classification = build_classification(source, raw_text)
    extraction = build_extraction(source, classification, raw_text)

    if args.dry_run:
        print(json.dumps({"classification": classification, "extraction": extraction}, indent=2, ensure_ascii=False))
        return 0

    out = output_root_for(source, args.output_root.resolve())
    out.mkdir(parents=True, exist_ok=True)
    dump_yaml(out / "classification.yaml", classification)
    dump_yaml(out / "extraction.yaml", extraction)
    dump_yaml(out / "schema-gaps.yaml", classification.get("schema_gaps", []) + extraction.get("schema_gaps", []))
    rendered = render_candidate_page(source, classification, extraction, out)
    provenance = {
        "source_id": source.get("id"),
        "source_record": str(args.source_record),
        "raw_text": str(args.raw_text) if args.raw_text else None,
        "generated_pages": [str(p.relative_to(out)) for p in rendered],
        "claim_count": len(extraction.get("claims", [])),
        "human_reviewed": False,
    }
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "validation-report.md").write_text(validation_report(source, classification, extraction, rendered), encoding="utf-8")
    print(f"gateway staging written: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    print(f"classification: {classification['primary_type']} -> {', '.join(classification['recommended_page_types']) or 'no pages'}")
    print("human review required before merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
