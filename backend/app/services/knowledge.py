from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = ROOT / "data" / "knowledge"


def search_knowledge(query: str, limit: int = 3) -> list[str]:
    terms = [term for term in query.lower().split() if term]
    results: list[tuple[int, str]] = []
    for path in KNOWLEDGE_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        score = sum(content.lower().count(term) for term in terms) if terms else 0
        if score == 0 and any(ch in content for ch in query[:8]):
            score = 1
        if score > 0:
            snippet = content[:500].strip()
            results.append((score, f"[{path.name}]\n{snippet}"))
    results.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in results[:limit]]
