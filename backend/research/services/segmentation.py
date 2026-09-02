from dataclasses import dataclass


@dataclass(frozen=True)
class TargetSegment:
    name: str
    geography: str | None = None
    customer_type: str | None = None


def normalize_segments(raw: list[dict]) -> list[TargetSegment]:
    """Normalize user-selected segments before they reach research execution."""
    result = []
    seen = set()
    for item in raw:
        name = str(item.get("name", "")).strip()
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        result.append(TargetSegment(name, item.get("geography"), item.get("customer_type")))
    return result
