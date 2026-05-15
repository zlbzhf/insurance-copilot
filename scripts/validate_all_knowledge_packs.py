#!/usr/bin/env python3
"""Validate every registered public institution knowledge pack.

The registry-driven validator preserves the generic-first architecture: CI checks
all public institution packs declared in `knowledge/registry.json` instead of
hard-coding one seed pack as the generic contract.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "knowledge" / "registry.json"
VALIDATOR = ROOT / "scripts" / "validate_knowledge_pack.py"


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def load_registry() -> dict[str, Any]:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"cannot read registry {REGISTRY.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("registry root must be an object")
    packs = data.get("packs")
    if not isinstance(packs, list):
        raise ValueError("registry must contain a packs list")
    return data


def public_pack_locations(registry: dict[str, Any]) -> list[tuple[str, Path]]:
    locations: list[tuple[str, Path]] = []
    seen_ids: set[str] = set()
    seen_locations: set[Path] = set()
    for index, pack in enumerate(registry.get("packs", [])):
        if not isinstance(pack, dict):
            raise ValueError(f"registry pack #{index} must be an object")
        pack_id = pack.get("id")
        if not isinstance(pack_id, str) or not pack_id.strip():
            raise ValueError(f"registry pack #{index} missing non-empty id")
        if pack_id in seen_ids:
            raise ValueError(f"duplicate registry pack id: {pack_id}")
        seen_ids.add(pack_id)

        if pack.get("type") != "public-institution-pack" or pack.get("data_classification") != "public":
            continue

        location = pack.get("location")
        if not isinstance(location, str) or not location.strip():
            raise ValueError(f"public pack {pack_id} missing non-empty location")
        if location.startswith("/") or ".." in Path(location).parts:
            raise ValueError(f"public pack {pack_id} has unsafe location: {location}")
        path = (ROOT / location).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError as exc:
            raise ValueError(f"public pack {pack_id} location escapes repo: {location}") from exc
        if path in seen_locations:
            raise ValueError(f"duplicate registry pack location: {location}")
        seen_locations.add(path)
        locations.append((pack_id, path))
    return locations


def main() -> int:
    try:
        registry = load_registry()
        locations = public_pack_locations(registry)
    except ValueError as exc:
        return fail(str(exc))

    if not locations:
        return fail("registry has no public institution packs to validate")

    validated: list[str] = []
    for pack_id, path in locations:
        if not path.is_dir():
            return fail(f"registered public pack missing directory: {path.relative_to(ROOT)}")
        cmd = [sys.executable, str(VALIDATOR), str(path.relative_to(ROOT))]
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if proc.returncode != 0:
            print(proc.stdout, end="")
            return fail(f"knowledge pack validation failed for {pack_id}: {path.relative_to(ROOT)}")
        validated.append(pack_id)

    print(f"validated public institution packs: {', '.join(validated)}")
    print(f"count: {len(validated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
