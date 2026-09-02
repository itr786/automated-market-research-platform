from collections import defaultdict

from research.models import Evidence, ResearchBrief


SECTION_ORDER = (
    "executive_summary",
    "market_overview",
    "market_sizing",
    "competitive_landscape",
    "risks_and_opportunities",
    "strategic_recommendations",
)


def build_report_outline(brief: ResearchBrief) -> dict:
    """Create a deterministic report structure from persisted evidence."""
    evidence = Evidence.objects.filter(brief=brief).order_by("-confidence", "-captured_at")
    grouped = defaultdict(list)
    for item in evidence:
        grouped["sources"].append({
            "url": item.source,
            "quote": item.quote,
            "confidence": float(item.confidence),
        })
    return {
        "brief_id": brief.id,
        "market": brief.market.name,
        "sections": [{"key": key, "sources": grouped["sources"][:10]} for key in SECTION_ORDER],
    }
