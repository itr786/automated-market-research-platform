from decimal import Decimal

import pytest

from research.services.evidence import score_evidence
from research.services.quota import QuotaService
from research.services.segmentation import normalize_segments


def test_evidence_score_is_bounded_and_weighted():
    assert score_evidence(1, 1, 1) == Decimal("1.0")
    assert score_evidence(0, 0, 0) == Decimal("0.0")


def test_quota_reports_remaining_capacity():
    quota = QuotaService(10)
    assert quota.remaining(7) == 3


def test_quota_rejects_overage():
    with pytest.raises(Exception):
        QuotaService(2).ensure_available(2)


def test_segments_are_normalized_and_deduplicated():
    result = normalize_segments([{"name": "Enterprise"}, {"name": " enterprise "}, {"name": "SMB"}])
    assert [item.name for item in result] == ["Enterprise", "SMB"]
