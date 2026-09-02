from decimal import Decimal

from research.models import Evidence


def score_evidence(source_quality: float, quote_match: float, freshness: float) -> Decimal:
    """Return a bounded weighted evidence confidence score."""
    values = [max(0.0, min(1.0, value)) for value in (source_quality, quote_match, freshness)]
    score = values[0] * 0.40 + values[1] * 0.40 + values[2] * 0.20
    return Decimal(str(round(score, 2)))


def attach_confidence(evidence: Evidence, source_quality: float, quote_match: float, freshness: float) -> Evidence:
    evidence.confidence = score_evidence(source_quality, quote_match, freshness)
    evidence.save(update_fields=["confidence"])
    return evidence
