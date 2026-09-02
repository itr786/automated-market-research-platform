from dataclasses import dataclass
from typing import Callable

from django.db import transaction

from research.models import ResearchBrief


@dataclass(frozen=True)
class ResearchEvent:
    brief_id: int
    status: str
    progress: int
    message: str


class ResearchRunner:
    """Small orchestration layer for a resumable research workflow."""

    STEPS = (
        "source discovery",
        "source retrieval",
        "evidence extraction",
        "claim reconciliation",
        "report assembly",
    )

    def __init__(self, publish: Callable[[ResearchEvent], None] | None = None):
        self.publish = publish or (lambda event: None)

    @transaction.atomic
    def start(self, brief: ResearchBrief) -> ResearchBrief:
        brief.status = ResearchBrief.Status.RUNNING
        brief.progress = 0
        brief.save(update_fields=["status", "progress", "updated_at"])
        self.publish(ResearchEvent(brief.id, brief.status, 0, "Research started"))
        return brief

    def progress(self, brief: ResearchBrief, step_index: int) -> ResearchEvent:
        bounded = max(0, min(step_index, len(self.STEPS)))
        percent = round((bounded / len(self.STEPS)) * 100)
        message = self.STEPS[bounded - 1] if bounded else "queued"
        return ResearchEvent(brief.id, ResearchBrief.Status.RUNNING, percent, message)

    @transaction.atomic
    def complete(self, brief: ResearchBrief) -> ResearchBrief:
        brief.status = ResearchBrief.Status.COMPLETE
        brief.progress = 100
        brief.save(update_fields=["status", "progress", "updated_at"])
        self.publish(ResearchEvent(brief.id, brief.status, 100, "Research complete"))
        return brief
