from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from .models import Evidence, ResearchBrief


@dataclass(frozen=True)
class ProgressEvent:
    status: str
    progress: int
    message: str


class ResearchWorkflow:
    """Application service for progressing a long-running research brief."""

    STAGES = (
        (15, "Research brief accepted"),
        (35, "Discovering relevant sources"),
        (60, "Collecting supporting evidence"),
        (80, "Synthesizing findings"),
        (100, "Research complete"),
    )

    @staticmethod
    @transaction.atomic
    def start(brief: ResearchBrief) -> list[ProgressEvent]:
        brief.status = ResearchBrief.Status.RUNNING
        brief.progress = 0
        brief.save(update_fields=["status", "progress", "updated_at"])
        return [ProgressEvent(ResearchBrief.Status.RUNNING, progress, message) for progress, message in ResearchWorkflow.STAGES]

    @staticmethod
    @transaction.atomic
    def complete(brief: ResearchBrief) -> ResearchBrief:
        brief.status = ResearchBrief.Status.COMPLETE
        brief.progress = 100
        brief.save(update_fields=["status", "progress", "updated_at"])
        return brief

    @staticmethod
    def add_evidence(brief: ResearchBrief, source: str, quote: str, confidence: Decimal) -> Evidence:
        return Evidence.objects.create(
            brief=brief,
            source=source,
            quote=quote,
            confidence=max(Decimal("0"), min(Decimal("1"), confidence)),
        )
