#!/usr/bin/env python3
"""Validate public institution LLM-wiki knowledge packs."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT = ["PACK.md", "SCHEMA.md", "index.md", "log.md"]
REQUIRED_DIRS = [
    "sources",
    "raw",
    "entities",
    "products",
    "concepts",
    "comparisons",
    "queries",
    "contributions",
    "contracts",
    "marketing",
    "underwriting",
    "service-processes",
    "service-processes/claims",
    "service-processes/renewal",
    "regulatory",
    "faqs",
    "source-summaries",
    "templates",
    "templates/sources",
    "templates/pages",
]
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
PUBLIC_ONLY_BAD_CLASSIFICATIONS = {"private", "confidential", "internal", "customer", "secret", "private-customer-data", "private-institution-note"}
PII_PATTERNS = {
    "ssn-like": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit-card-like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "email-like": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone-like": re.compile(r"(?<!\d)(?:\+?\d{1,3}[ -]?)?(?:\(?\d{3}\)?[ -]?)\d{3}[ -]?\d{4}(?!\d)"),
}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(errors="ignore")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter not closed")
    fm_text = text[4:end]
    body = text[text.find("\n", end + 4) + 1 :]
    if yaml:
        fm = yaml.safe_load(fm_text) or {}
    else:
        fm = {}
        for line in fm_text.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                fm[key.strip()] = value.strip()
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a mapping")
    return fm, body


def parse_yaml_file(path: Path) -> dict[str, Any]:
    text = path.read_text(errors="ignore")
    if yaml:
        data = yaml.safe_load(text) or {}
    else:
        data = {}
        for line in text.splitlines():
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip().strip('"\'')
    if not isinstance(data, dict):
        raise ValueError("YAML must parse as mapping")
    return data


def load_page_registry() -> dict[str, Any]:
    return parse_yaml_file(ROOT / "standards" / "page-type-registry.yaml")


def load_source_taxonomy() -> dict[str, Any]:
    return parse_yaml_file(ROOT / "standards" / "source-taxonomy.yaml")


def slug_for(path: Path) -> str:
    return path.stem


def markdown_pages(pack: Path) -> list[Path]:
    skip_names = {"PACK.md", "SCHEMA.md", "index.md", "log.md", "README.md"}
    skip_dirs = {"raw", "sources", "contributions", "templates"}
    pages = []
    for p in pack.rglob("*.md"):
        rel = p.relative_to(pack)
        if p.name in skip_names:
            continue
        if any(part in skip_dirs for part in rel.parts):
            continue
        if p.name == "README.md":
            continue
        pages.append(p)
    return sorted(pages)


def source_records(pack: Path) -> list[Path]:
    src = pack / "sources"
    return sorted(list(src.glob("*.yaml")) + list(src.glob("*.yml")))


def source_type_allowed(source_type: str, taxonomy: dict[str, Any]) -> bool:
    source_types = taxonomy.get("source_types", {})
    if source_type in source_types:
        return True
    for cfg in source_types.values():
        if isinstance(cfg, dict) and source_type in cfg.get("aliases", []):
            return True
    return False


def page_required_sections(page_type: str, registry: dict[str, Any]) -> list[str]:
    cfg = registry.get("page_types", {}).get(page_type, {})
    return cfg.get("required_sections", []) if isinstance(cfg, dict) else []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", type=Path, help="Path to institution pack")
    parser.add_argument("--template", action="store_true", help="Allow template placeholders")
    args = parser.parse_args()
    pack = args.pack.resolve()
    if not pack.exists():
        return fail(f"pack does not exist: {pack}")
    if not pack.is_dir():
        return fail(f"pack is not a directory: {pack}")

    registry = load_page_registry()
    taxonomy = load_source_taxonomy()
    allowed_page_types = set(registry.get("page_types", {}).keys())

    for name in REQUIRED_ROOT:
        if not (pack / name).exists():
            return fail(f"missing {name}")
    for name in REQUIRED_DIRS:
        if not (pack / name).is_dir():
            return fail(f"missing directory {name}/")

    for rel in [
        "templates/sources/product-brochure-source.yaml",
        "templates/sources/policy-contract-source.yaml",
        "templates/sources/marketing-material-source.yaml",
        "templates/pages/product-summary.md",
        "templates/pages/policy-contract-summary.md",
        "templates/pages/marketing-compliance-review.md",
    ]:
        if not (pack / rel).exists():
            return fail(f"missing template {rel}")

    try:
        pack_fm, _ = parse_frontmatter(pack / "PACK.md")
    except Exception as exc:
        return fail(f"PACK.md invalid: {exc}")

    if pack_fm.get("type") != "public-institution-pack":
        return fail("PACK.md type must be public-institution-pack")
    if pack_fm.get("data_classification") != "public":
        return fail("PACK.md data_classification must be public")
    pack_id = pack_fm.get("id")
    if not pack_id:
        return fail("PACK.md missing id")

    index_text = (pack / "index.md").read_text(errors="ignore")
    log_text = (pack / "log.md").read_text(errors="ignore")
    schema_text = (pack / "SCHEMA.md").read_text(errors="ignore")
    for required in ["Required Frontmatter", "Source Record", "Tag Taxonomy", "Confidence", "Source-to-Page Mapping", "Schema Evolution"]:
        if required not in schema_text:
            return fail(f"SCHEMA.md missing section text: {required}")
    if "## [" not in log_text:
        return fail("log.md missing dated entries")

    # Source records
    for src in source_records(pack):
        try:
            data = parse_yaml_file(src)
        except Exception as exc:
            return fail(f"invalid source record {src.relative_to(pack)}: {exc}")
        for key in ["id", "institution", "source_type", "retrieved_at", "public_source", "redistribution"]:
            if key not in data:
                return fail(f"source record {src.relative_to(pack)} missing {key}")
        if str(data.get("institution")) != str(pack_id) and not args.template:
            return fail(f"source record {src.relative_to(pack)} institution mismatch")
        if data.get("public_source") is not True:
            return fail(f"source record {src.relative_to(pack)} must be public_source: true")
        if not source_type_allowed(str(data.get("source_type")), taxonomy):
            return fail(f"source record {src.relative_to(pack)} has unknown source_type: {data.get('source_type')}")

    pages = markdown_pages(pack)
    existing_slugs = {slug_for(p): p for p in pages}
    # Include README-less concept in index via [[slug]].
    for page in pages:
        try:
            fm, body = parse_frontmatter(page)
        except Exception as exc:
            return fail(f"page {page.relative_to(pack)} invalid frontmatter: {exc}")
        for key in ["title", "created", "updated", "type", "institution", "tags", "sources", "confidence", "public_source", "needs_verification"]:
            if key not in fm:
                return fail(f"page {page.relative_to(pack)} missing frontmatter key: {key}")
        page_type = fm.get("type")
        if page_type not in allowed_page_types:
            return fail(f"page {page.relative_to(pack)} has invalid type: {page_type}")
        if str(fm.get("institution")) != str(pack_id) and not args.template:
            return fail(f"page {page.relative_to(pack)} institution mismatch")
        if fm.get("public_source") is not True:
            return fail(f"page {page.relative_to(pack)} must set public_source: true")
        if fm.get("confidence") not in ALLOWED_CONFIDENCE:
            return fail(f"page {page.relative_to(pack)} invalid confidence")
        fm_text = str(fm).lower()
        if any(term in fm_text for term in PUBLIC_ONLY_BAD_CLASSIFICATIONS):
            return fail(f"page {page.relative_to(pack)} contains private/confidential classification")
        if f"[[{page.stem}]]" not in index_text and not args.template:
            return fail(f"index.md missing page link [[{page.stem}]]")
        if len(body.strip()) < 200:
            return fail(f"page too thin: {page.relative_to(pack)}")
        for section in page_required_sections(str(page_type), registry):
            if f"## {section}" not in body:
                return fail(f"page {page.relative_to(pack)} missing required section for {page_type}: {section}")
        for link in WIKILINK.findall(body):
            if link not in existing_slugs and not args.template:
                return fail(f"broken wikilink in {page.relative_to(pack)}: [[{link}]]")

    # PII scan public pack text files.
    for path in pack.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".txt"}:
            continue
        text = path.read_text(errors="ignore")
        # Ignore obvious template placeholders.
        if args.template and "example.com" in text:
            continue
        for label, pattern in PII_PATTERNS.items():
            if pattern.search(text):
                return fail(f"possible {label} PII in {path.relative_to(pack)}")

    print(f"knowledge pack ok: {pack.relative_to(ROOT) if pack.is_relative_to(ROOT) else pack}")
    print(f"pages: {len(pages)}")
    print(f"sources: {len(source_records(pack))}")
    print(f"page_types: {len(allowed_page_types)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
